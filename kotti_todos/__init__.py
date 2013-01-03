from pyramid.i18n import TranslationStringFactory
from kotti.util import extract_from_settings
from js.jquery_infinite_ajax_scroll import (
    jquery_infinite_ajax_scroll,
    jquery_infinite_ajax_scroll_css,
)

_ = TranslationStringFactory('kotti_todos')


def kotti_configure(settings):
    settings['pyramid.includes'] += ' kotti_todos.views'
    settings['kotti.available_types'] += \
            ' kotti_todos.resources.Todos'
    settings['kotti.available_types'] += \
            ' kotti_todos.resources.Category'
    settings['kotti.available_types'] += \
            ' kotti_todos.resources.TodoItem'


def check_true(value):
    if value == u'true':
        return True
    return False


TODOS_DEFAULTS = {
    'use_batching': 'true',
    'pagesize': '10',
    'use_auto_batching': 'true',
    'link_headline_overview': 'true',
    }


def todos_settings(name=''):
    prefix = 'kotti_todos.todos_settings.'
    if name:
        prefix += name + '.'  # pragma: no cover
    settings = TODOS_DEFAULTS.copy()
    settings.update(extract_from_settings(prefix))
    settings['use_batching'] = check_true(settings['use_batching'])
    try:
        settings['pagesize'] = int(settings['pagesize'])
    except ValueError:
        settings['pagesize'] = 10
    settings['use_auto_batching'] = check_true(settings['use_auto_batching'])
    settings['link_headline_overview'] = \
            check_true(settings['link_headline_overview'])
    return settings
