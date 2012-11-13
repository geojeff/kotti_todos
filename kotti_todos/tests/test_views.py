# -*- coding: utf-8 -*-

import os
import kotti
import plone
from kotti.resources import get_root
from kotti.testing import DummyRequest
from kotti.testing import UnitTestBase
from kotti_todos.resources import Todos
from kotti_todos.resources import TodoItem
from kotti_todos.views import TodoItemView
from kotti_todos.views import TodosView

here = os.path.abspath(os.path.dirname(__file__))


class ViewsTests(UnitTestBase):

    def test_todoitem_view(self):

        root = get_root()
        todoitem = root['todoitem'] = TodoItem()

        view = TodoItemView(todoitem, DummyRequest()).view()

        assert view is not None

    def test_todos_view_adding_todoitem(self):

        root = get_root()
        todos = root['todos'] = Todos()
        view = TodosView(root['todos'],
                                      DummyRequest()).view()
        todoitem = todos['todoitem'] = TodoItem()

        assert todoitem is not None

        assert view is not None

        assert ('items' in view)
        
        batch = view['items']

        assert type(batch) is plone.batching.batch.BaseBatch

        assert ('api' in view) \
                and (type(view['api']) is kotti.views.util.TemplateAPI)

        assert ('settings' in view) \
                 and ('use_batching' in view['settings']) \
                 and (view['settings']['use_batching'] is True)
        assert ('settings' in view) \
                and ('pagesize' in view['settings']) \
                and (view['settings']['pagesize'] == 5)
        assert ('settings' in view) \
                and ('use_auto_batching' in view['settings']) \
                and (view['settings']['use_auto_batching'] is True)
        assert ('settings' in view) \
                and ('link_headline_overview' in view['settings']) \
                and (view['settings']['link_headline_overview'] is True)

    def test_todos_view_no_todoitem(self):

        root = get_root()
        todos = root['todos'] = Todos()
        view = TodosView(root['todos'],
                                      DummyRequest()).view()

        assert view is not None

        assert ('items' in view) and (len(view['items']) == 0)

        assert ('settings' in view) \
                 and ('use_batching' in view['settings']) \
                 and (view['settings']['use_batching'] is True)
        assert ('settings' in view) \
                and ('pagesize' in view['settings']) \
                and (view['settings']['pagesize'] == 5)
        assert ('settings' in view) \
                and ('use_auto_batching' in view['settings']) \
                and (view['settings']['use_auto_batching'] is True)
        assert ('settings' in view) \
                and ('link_headline_overview' in view['settings']) \
                and (view['settings']['link_headline_overview'] is True)
        assert (('settings' in view) \
                 and ('use_batching' in view['settings']) \
                 and (view['settings']['use_batching'] is True))
