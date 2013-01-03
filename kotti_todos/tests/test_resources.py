# -*- coding: utf-8 -*-

from pyramid.threadlocal import get_current_registry

from kotti.resources import get_root

from kotti.testing import DummyRequest
from kotti.testing import UnitTestBase
from kotti.testing import FunctionalTestBase
from kotti.testing import testing_db_url

from kotti_todos import todos_settings
from kotti_todos.resources import Todos
from kotti_todos.resources import TodoItem

from fixtures import test_todos

def test_todos(db_session):
    root = get_root()
    todos = Todos()
    assert todos.type_info.addable(root, DummyRequest()) is True
    root['todos'] = todos

    todoitem = TodoItem()

    assert len(todos.values()) == 0

    # there are no children of type TodoItem yet, the UI should present the add link
    assert todoitem.type_info.addable(todos, DummyRequest()) is True

    todos['todoitem'] = todoitem

    assert len(todos.values()) == 1

def test_todoitems(db_session):
    root = get_root()
    todos = Todos()
    root['todos'] = todos

    for cat in test_todos:
        todos[cat] = Category(cat)
        for title in test_todos[cat]:
            todos[cat][title] = TodoItem(title=title,
                                         todostate=test_todos[cat][title])

    assert len(todos.values()) == len(test_todos)

    for cat in test_todos:
        assert len(todos[cat].values()) == len(test_todos[cat])


#class FunctionalTests(FunctionalTestBase):
#
#    def setUp(self, **kwargs):
#        self.settings = {'kotti.configurators': 'kotti_todos.kotti_configure',
#                         'sqlalchemy.url': testing_db_url(),
#                         'kotti.secret': 'dude',
#                         'kotti_todos.todos_settings.pagesize': '5'}
#        super(FunctionalTests, self).setUp(**self.settings)
#
#    def test_asset_overrides(self):
#        from kotti import main
#        self.settings['kotti_todos.asset_overrides'] = 'kotti_todos:hello_world/'
#        main({}, **self.settings)

def test_todos_default_settings(db_session):
    b_settings = todos_settings()
    assert b_settings['use_batching'] == True
    assert b_settings['pagesize'] == 5
    assert b_settings['use_auto_batching'] == True
    assert b_settings['link_headline_overview'] == True

def test_todos_change_settings(db_session):
    settings = get_current_registry().settings
    settings['kotti_todos.todos_settings.use_batching'] = u'false'
    settings['kotti_todos.todos_settings.pagesize'] = u'2'
    settings['kotti_todos.todos_settings.use_auto_batching'] = u'false'
    settings['kotti_todos.todos_settings.link_headline_overview'] = u'false'

    b_settings = todos_settings(db_session)
    assert b_settings['use_batching'] == False
    assert b_settings['pagesize'] == 2
    assert b_settings['use_auto_batching'] == False
    assert b_settings['link_headline_overview'] == False

def test_todos_wrong_settings(db_session):
    settings = get_current_registry().settings
    settings['kotti_todos.todos_settings.use_batching'] = u'blibs'
    settings['kotti_todos.todos_settings.pagesize'] = u'blabs'
    settings['kotti_todos.todos_settings.use_auto_batching'] = u'blubs'
    settings['kotti_todos.todos_settings.link_headline_overview'] = u'blobs'

    b_settings = todos_settings()
    assert b_settings['use_batching'] == False
    assert b_settings['pagesize'] == 5
    assert b_settings['use_auto_batching'] == False
    assert b_settings['link_headline_overview'] == False

