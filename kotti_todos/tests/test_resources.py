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


class UnitTests(UnitTestBase):

    def test_todos(self):
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

    def test_todoitem_only_pypi_url_provided(self):
        root = get_root()
        todos = Todos()
        root['todos'] = todos

        todoitem = TodoItem(
                pypi_url="http://pypi.python.org/pypi/kotti_todos/json")

        todos['todoitem'] = todoitem

        assert len(todos.values()) == 1

    def test_todoitem_only_github_owner_and_repo_provided(self):
        root = get_root()
        todos = Todos()
        root['todos'] = todos

        todoitem = TodoItem(
                github_owner="geojeff",
                github_repo="kotti_todos")

        todos['todoitem'] = todoitem

        assert len(todos.values()) == 1

    def test_todoitem_github_data(self):
        root = get_root()
        todos = Todos()
        root['todos'] = todos

        todoitem = TodoItem(
                title="kotti_todos Project",
                date_handling_choice="use_github_date",
                desc_handling_choice="use_github_description",
                github_owner="geojeff",
                github_repo="kotti_todos")

        todos['todoitem'] = todoitem

        assert len(todos.values()) == 1

    def test_todoitem_only_bitbucket_owner_and_repo_provided(self):
        root = get_root()
        todos = Todos()
        root['todos'] = todos

        todoitem = TodoItem(
                bitbucket_owner="pypy",
                bitbucket_repo="pypy")

        todos['todoitem'] = todoitem

        assert len(todos.values()) == 1

    def test_todoitem_bitbucket_data(self):
        root = get_root()
        todos = Todos()
        root['todos'] = todos

        todoitem = TodoItem(
                title="kotti_todos Project",
                date_handling_choice="use_bitbucket_date",
                desc_handling_choice="use_bitbucket_description",
                bitbucket_owner="pypy",
                bitbucket_repo="pypy")

        todos['todoitem'] = todoitem

        assert len(todos.values()) == 1

    def test_todoitem_pypi_overwriting(self):
        root = get_root()
        todos = Todos()
        root['todos'] = todos

        todoitem = TodoItem(
                pypi_url="http://pypi.python.org/pypi/Kotti/json",
                overwrite_home_page_url=True,
                overwrite_docs_url=True,
                overwrite_package_url=True,
                overwrite_bugtrack_url=True,
                desc_handling_choice='use_pypi_summary')

        todos['todoitem'] = todoitem

        assert len(todos.values()) == 1

        # desc_handling_choice is an either/or,
        # so also check for description overwriting
        todoitem = TodoItem(
                pypi_url="http://pypi.python.org/pypi/Kotti/json",
                desc_handling_choice='use_pypi_description')


class FunctionalTests(FunctionalTestBase):

    def setUp(self, **kwargs):
        self.settings = {'kotti.configurators': 'kotti_todos.kotti_configure',
                         'sqlalchemy.url': testing_db_url(),
                         'kotti.secret': 'dude',
                         'kotti_todos.todos_settings.pagesize': '5'}
        super(FunctionalTests, self).setUp(**self.settings)

    def test_asset_overrides(self):
        from kotti import main
        self.settings['kotti_todos.asset_overrides'] = 'kotti_todos:hello_world/'
        main({}, **self.settings)

    def test_todos_default_settings(self):
        b_settings = todos_settings()
        assert b_settings['use_batching'] == True
        assert b_settings['pagesize'] == 5
        assert b_settings['use_auto_batching'] == True
        assert b_settings['link_headline_overview'] == True

    def test_todos_change_settings(self):
        settings = get_current_registry().settings
        settings['kotti_todos.todos_settings.use_batching'] = u'false'
        settings['kotti_todos.todos_settings.pagesize'] = u'2'
        settings['kotti_todos.todos_settings.use_auto_batching'] = u'false'
        settings['kotti_todos.todos_settings.link_headline_overview'] = u'false'

        b_settings = todos_settings()
        assert b_settings['use_batching'] == False
        assert b_settings['pagesize'] == 2
        assert b_settings['use_auto_batching'] == False
        assert b_settings['link_headline_overview'] == False

    def test_todos_wrong_settings(self):
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
