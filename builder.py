# coding=utf8
"""
Python builder for Fate SRD
"""
import copy
from os import makedirs, walk
from os.path import join
import re
from urllib.parse import urljoin

import click
from html2text import html2text
from pyquery import PyQuery as pq
import requests
import yaml

from common import FATE_CORE, FATE_ACCELERATED, FATE_TOOLKIT

BASE_URL = 'https://fate-srd.com/'

CORE_PAGES = yaml.load(open('{}.yaml'.format(FATE_CORE)))
FAE_PAGES = yaml.load(open('{}.yaml'.format(FATE_ACCELERATED)))
TOOLKIT_PAGES = yaml.load(open('{}.yaml'.format(FATE_TOOLKIT)))

TITLES = {}

MODULES = (
    {
        'id': 'core',
        "slug": FATE_CORE,
        "pages": CORE_PAGES,
        "title": "Fate Core"
    },
    {
        'id': 'accelerated',
        "slug": FATE_ACCELERATED,
        "pages": FAE_PAGES,
        "title": "Face Accelerated"
    },
    {
        'id': 'toolkit',
        'slug': FATE_TOOLKIT,
        'pages': TOOLKIT_PAGES,
        'title': 'Fate System Toolkit',
    }
)

IDS = list(item['id'] for item in MODULES)

FIND_FATE_FONT = r'(<span class="fate_font">(.*?)</span>)'
FIND_FATE_FONT_BIG = r'(<span class="fate_font big">(.*?)</span>)'
REPLACE_FATE_FONT = r'[span:fate_font]\2[/span]'

FIND_ASPECTS = r'(<span class="aspect">(.*?)</span>)'
REPLACE_ASPECTS = r'[span:aspect]\2[/span]'


def get_content(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text


def find_title(text):
    lines = text.split('\n')
    for line in lines:
        if line.startswith('# '):
            return line.replace('#', '').strip()
    raise Exception("No TITLE!!!! ARGHHH!!!")


def fetch_titles(module):
    titles = {}
    for root, dirs, files in walk(join('markdown', module)):
        for filename in files:
            if filename.endswith('.md'):
                filepath = join(root, filename)
                with open(filepath) as fd:
                    title = find_title(fd.read())
                    titles['{}'.format(root.replace('markdown/', ''))] = title
    return titles


def clean_html(html):
    """
    Clean up HTML oddities.
    """
    html = re.sub(FIND_FATE_FONT, REPLACE_FATE_FONT, html)
    html = re.sub(FIND_FATE_FONT_BIG, REPLACE_FATE_FONT, html)
    html = re.sub(FIND_ASPECTS, REPLACE_ASPECTS, html)
    return html


def clean_text(text):
    text = text.replace('//fate-srd.com', '../..')
    text = text.replace('//fate-\nsrd.com', '../..')
    text = text.replace('. **', '.** ')
    text = text.replace('[span:fate_font]', '<span class="fate_font">')
    text = text.replace('[span:aspect]', '<span class="aspect">')
    text = text.replace('[/span]', '</span>')
    text = text.replace('**Create**** ', '**Create ')
    return text


def get_markdown(page, root):
    url = join(root, page)
    url = urljoin(BASE_URL, url)
    click.echo("Parsing: {} -> {}".format(url, page))

    content = get_content(url)
    parsed = pq(content)
    article = parsed('article.main-content')
    html = article.html()
    html = clean_html(html)
    text = html2text(html)
    title = find_title(text)

    text = clean_text(text)

    headings = '''---
title: "{}"
---
    '''.format(title)
    text = '{}\n{}'.format(headings, text)
    return text, title


def write_page(page, module):
    module_path = join('markdown', module)
    text, title = get_markdown(page, module)
    page_filename = page.replace(r'%E2%80%99', "’")
    makedirs(join(module_path, page_filename), exist_ok=True)
    with open(join(module_path, page_filename, 'index.md'), 'w') as fd:
        fd.write(text)


def write_block(block, module):
    for item in block:
        if not isinstance(item, list):
            write_page(item, module)
        else:
            write_block(item, module)


def menu_block(block, lvl=0):
    for item in block:
        if not isinstance(item, list):
            yield lvl, item
        else:
            for _lvl, _item in menu_block(item, lvl + 1):
                yield _lvl, _item


def setup_module(module):
    module_slug = module['slug']
    module_path = join('markdown', module_slug)
    makedirs(module_path, exist_ok=True)
    return module_path


@click.group(chain=True)
def main():
    pass


@click.command('pages', help="Build Pages")
@click.option('--only', type=click.Choice(IDS))
def pages(only):
    modules = copy.deepcopy(MODULES)
    if only:
        modules = filter(lambda item: item['id'] == only, modules)
    for module in modules:
        module_slug = module['slug']
        block = module['pages']
        module_title = module['title']
        click.echo('Downloading {}'.format(module_title))

        setup_module(module)
        write_block(block, module_slug)


@click.command('indexes', help="Build indexes")
@click.option('--only', type=click.Choice(IDS))
def indexes(only):
    modules = copy.deepcopy(MODULES)
    if only:
        modules = filter(lambda item: item['id'] == only, modules)
    for module in modules:
        module_slug = module['slug']
        block = module['pages']
        module_title = module['title']
        click.echo('Index for {}'.format(module_title))

        module_path = setup_module(module)

        titles = fetch_titles(module_slug)
        # Home page build
        lines = [
            '---',
            'title: {}'.format(module_title),
            '---',
            "# {}".format(module_title),
            ''
        ]
        for lvl, item in menu_block(block):
            item_path = item.replace(r'%E2%80%99', "’")
            menu_item = '{spaces}- [{title}]({item}/)'.format(
                spaces='  ' * lvl,
                item=item_path,
                title=titles['{}/{}'.format(module_slug, item_path)]
            )
            lines.append(menu_item)

        with open(join(module_path, 'index.md'), 'w') as fd:
            fd.write('\n'.join(lines))

    click.echo('General Index')
    lines = [
        '---',
        'title: Fate SRD',
        '---',
        "# Fate SRD", ''
    ]
    for module in MODULES:
        menu_item = '- [{title}]({item}/)'.format(
            item=module['slug'],
            title=module['title'],
        )
        lines.append(menu_item)
    with open(join('markdown', 'index.md'), 'w') as fd:
        fd.write('\n'.join(lines))


if __name__ == '__main__':
    main.add_command(pages)
    main.add_command(indexes)
    main()
