from os import makedirs, walk
from os.path import join
from string import Template

import markdown
from markdown.extensions.toc import TocExtension
from mdx_gfm import GithubFlavoredMarkdownExtension
from slugify import slugify


def convert_md_source(source):
    "Convert Markdown content into HTML"
    md = markdown.Markdown(
        extensions=[
            'markdown.extensions.meta',
            GithubFlavoredMarkdownExtension(),
            TocExtension(permalink=True, slugify=slugify),
        ]
    )
    html = md.convert(source)
    return html, md.Meta


def get_base_template():
    with open('templates/base.html') as fd:
        template_string = fd.read()
    template = Template(template_string)
    return template


def clean_source(source, level):
    level_path = '/'.join(['..'] * level) if level else '.'
    source = source.replace('](/', ']({}/'.format(level_path))
    return source


def main():
    base_template = get_base_template()
    for dirname, _, filenames in walk('markdown'):
        if dirname == 'markdown/static':
            continue

        for filename in filenames:
            target_dirname = dirname.replace('markdown', 'docs')
            level = target_dirname.count('/')
            makedirs(target_dirname, exist_ok=True)
            with open(join(dirname, filename)) as fd:
                source = fd.read()

            source = clean_source(source, level)
            content, meta = convert_md_source(source)
            if 'title' in meta:
                title = meta.get('title')[0]
            else:
                print("no title", meta, join(dirname, filename))
                title = "NO TITLE"

            data = {
                "title": title,
                "content": content,
                "css_path": '/'.join(['..'] * level) or '.',
            }

            html = base_template.substitute(**data)
            with open(join(target_dirname, 'index.html'), 'w') as fd:
                fd.write(html)


if __name__ == '__main__':
    main()
