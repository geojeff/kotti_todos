import datetime
from dateutil.tz import tzutc

from sqlalchemy import func

import colander
from colander import Invalid

import logging

from deform.widget import CheckboxWidget
from deform.widget import DateTimeInputWidget
from deform.widget import SelectWidget
from deform.widget import RadioChoiceWidget

from kotti.views.form import AddFormView
from kotti.views.form import EditFormView

from kotti.views.edit import DocumentSchema

from kotti_todos import todos_settings
from kotti_todos.resources import Todos
from kotti_todos.resources import Topic
from kotti_todos.resources import TodoItem
from kotti_todos.static import kotti_todos_js
from kotti_todos import _

from kotti.security import has_permission
from kotti.views.util import template_api

from kotti import DBSession

from plone.batching import Batch

from pyramid.view import view_config
from pyramid.view import view_defaults
from pyramid.renderers import get_renderer

log = logging.getLogger(__name__)


class TodosSchema(DocumentSchema):
    pass


class TopicSchema(DocumentSchema):
    pass


class TodoItemSchema(DocumentSchema):
    pass


class AddTodoItemFormView(AddFormView):
    item_type = _(u"TodoItem")
    item_class = TodoItem

    def schema_factory(self):

        return TodoItemSchema()

    def add(self, **appstruct):

        return self.item_class(
            title=appstruct['title'],
            description=appstruct['description'],
            body=appstruct['body'],
            tags=appstruct['tags'],
            )


class EditTodoItemFormView(EditFormView):

    def schema_factory(self):

        return TodoItemSchema()

    def edit(self, **appstruct):

        if appstruct['title']:
            self.context.title = appstruct['title']

        if appstruct['description']:
            self.context.description = appstruct['description']

        if appstruct['body']:
            self.context.body = appstruct['body']

        if appstruct['tags']:
            self.context.tags = appstruct['tags']


class AddTodosFormView(AddFormView):
    item_type = _(u"Todos")
    item_class = Todos

    def schema_factory(self):

        return TodosSchema()

    def add(self, **appstruct):

        return self.item_class(
            title=appstruct['title'],
            description=appstruct['description'],
            body=appstruct['body'],
            tags=appstruct['tags'],
            default_view='folder-view',
            )


class EditTodosFormView(EditFormView):

    def schema_factory(self):

        return TodosSchema()

    def edit(self, **appstruct):

        if appstruct['title']:
            self.context.title = appstruct['title']

        if appstruct['description']:
            self.context.description = appstruct['description']

        if appstruct['body']:
            self.context.body = appstruct['body']

        if appstruct['tags']:
            self.context.tags = appstruct['tags']


class AddTopicFormView(AddFormView):
    item_type = _(u"Topic")
    item_class = Topic

    def schema_factory(self):

        return TopicSchema()

    def add(self, **appstruct):

        return self.item_class(
            title=appstruct['title'],
            description=appstruct['description'],
            body=appstruct['body'],
            tags=appstruct['tags'],
            default_view='folder-view',
            )


class EditTopicFormView(EditFormView):

    def schema_factory(self):

        return TopicSchema()

    def edit(self, **appstruct):

        if appstruct['title']:
            self.context.title = appstruct['title']

        if appstruct['description']:
            self.context.description = appstruct['description']

        if appstruct['body']:
            self.context.body = appstruct['body']

        if appstruct['tags']:
            self.context.tags = appstruct['tags']


@view_defaults(permission='view')
class BaseView(object):

    def __init__(self, context, request):

        self.context = context
        self.request = request

        if has_permission("edit", self.context, self.request):
            kotti_todos_js.need()


@view_defaults(context=TodoItem,
               permission='view')
class TodoItemView(BaseView):

    @view_config(renderer='kotti_todos:templates/todoitem-view.pt')
    def view(self):

        return {}


@view_defaults(context=Topic,
               permission='view')
class TopicView(BaseView):

    @view_config(
             renderer="kotti_todos:templates/topic-view.pt")
    def view(self):

        session = DBSession()

        query = session.query(TodoItem).filter(
                TodoItem.parent_id == self.context.id)

        items = query.all()

        page = self.request.params.get('page', 1)

        settings = todos_settings()

        if settings['use_batching']:
            items = Batch.fromPagenumber(items,
                          pagesize=settings['pagesize'],
                          pagenumber=int(page))

        return {
            'api': template_api(self.context, self.request),
            'macros': get_renderer('templates/macros.pt').implementation(),
            'items': items,
            'settings': settings,
            }


@view_defaults(context=Todos,
               permission='view')
class TodosView(BaseView):

    @view_config(
             renderer="kotti_todos:templates/todos-view.pt")
    def view(self):

        session = DBSession()

        query = session.query(Topic).filter(
                Topic.parent_id == self.context.id)

        items = query.all()

        modification_dates_and_items = []
        for item in items:
            if item.children:
                sorted_todoitems = sorted(item.children, 
                                      key=lambda x: x.modification_date,
                                      reverse=True)
                modification_dates_and_items.append(
                        (sorted_todoitems[0].modification_date, sorted_todoitems[0], item))
            else:
                modification_dates_and_items.append(
                        (item.modification_date, item, item))

        items = sorted(modification_dates_and_items)

        page = self.request.params.get('page', 1)

        settings = todos_settings()

        if settings['use_batching']:
            items = Batch.fromPagenumber(items,
                          pagesize=settings['pagesize'],
                          pagenumber=int(page))

        return {
            'api': template_api(self.context, self.request),
            'macros': get_renderer('templates/macros.pt').implementation(),
            'items': items,
            'settings': settings,
            }


def includeme_edit(config):

    config.add_view(
        EditTodosFormView,
        context=Todos,
        name='edit',
        permission='edit',
        renderer='kotti:templates/edit/node.pt',
        )

    config.add_view(
        AddTodosFormView,
        name=Todos.type_info.add_view,
        permission='add',
        renderer='kotti:templates/edit/node.pt',
        )

    config.add_view(
        EditTopicFormView,
        context=Topic,
        name='edit',
        permission='edit',
        renderer='kotti:templates/edit/node.pt',
        )

    config.add_view(
        AddTopicFormView,
        name=Topic.type_info.add_view,
        permission='add',
        renderer='kotti:templates/edit/node.pt',
        )

    config.add_view(
        EditTodoItemFormView,
        context=TodoItem,
        name='edit',
        permission='edit',
        renderer='kotti:templates/edit/node.pt',
        )

    config.add_view(
        AddTodoItemFormView,
        name=TodoItem.type_info.add_view,
        permission='add',
        renderer='kotti:templates/edit/node.pt',
        )


def includeme_view(config):

    config.add_static_view('static-kotti_todos', 'kotti_todos:static')


def includeme(config):

    settings = config.get_settings()

    if 'kotti_todos.asset_overrides' in settings:
        asset_overrides = \
                [a.strip()
                 for a in settings['kotti_todos.asset_overrides'].split()
                 if a.strip()]
        for override in asset_overrides:
            config.override_asset(to_override='kotti_todos',
                                  override_with=override)

    config.scan("kotti_todos")

    includeme_edit(config)
    includeme_view(config)
