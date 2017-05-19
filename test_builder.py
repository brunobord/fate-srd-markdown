import re
from builder import FIND_FATE_FONT, REPLACE_FATE_FONT
from builder import FIND_FATE_FONT_BIG


def test_find_fate_font():
    result = re.sub(
        FIND_FATE_FONT,
        REPLACE_FATE_FONT,
        'hello <span class="fate_font">world</span>')
    assert result == 'hello [span:fate_font]world[/span]'

    result = re.sub(
        FIND_FATE_FONT,
        REPLACE_FATE_FONT,
        'hello <span class="fate_font">world</span> toto')
    assert result == 'hello [span:fate_font]world[/span] toto'

    result = re.sub(
        FIND_FATE_FONT,
        REPLACE_FATE_FONT,
        'hello <span class="fate_font">world</span> toto <span class="fate_font">meuh</span>')  # noqa
    assert result == 'hello [span:fate_font]world[/span] toto [span:fate_font]meuh[/span]'  # noqa


def test_find_fate_font_big():
    result = re.sub(
        FIND_FATE_FONT_BIG,
        REPLACE_FATE_FONT,
        'hello <span class="fate_font big">world</span>')
    assert result == 'hello [span:fate_font]world[/span]'

    result = re.sub(
        FIND_FATE_FONT_BIG,
        REPLACE_FATE_FONT,
        'hello <span class="fate_font big">world</span> toto')
    assert result == 'hello [span:fate_font]world[/span] toto'

    result = re.sub(
        FIND_FATE_FONT_BIG,
        REPLACE_FATE_FONT,
        'hello <span class="fate_font big">world</span> toto <span class="fate_font big">meuh</span>')  # noqa
    assert result == 'hello [span:fate_font]world[/span] toto [span:fate_font]meuh[/span]'  # noqa
