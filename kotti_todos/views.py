import datetime
from dateutil.tz import tzutc

from sqlalchemy import func
from sqlalchemy import desc

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
from kotti_todos.resources import Category
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


class CategorySchema(DocumentSchema):
    pass


class TodoItemSchema(DocumentSchema):
    choices = (('', '- Select -'),
               ('done', 'done'),
               ('pending', 'pending'),
               ('in progress', 'in progress'),
               ('deferred', 'deferred'),
               ('abandoned', 'abandoned'))
    todostate = colander.SchemaNode(
        colander.String(),
        default=_(u'in progress'),
        missing=_(u'in progress'),
        title=_(u'State'),
        widget=SelectWidget(values=choices))


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
            todostate=appstruct['todostate'],
            )

def todoitem_validator(form, value):
    pass


#@view_config(name='edit',
#             context=MediaFile, permission='edit',
#             renderer='kotti:templates/edit/node.pt')
class EditTodoItemFormView(EditFormView):

    def schema_factory(self):

        return TodoItemSchema(validator=todoitem_validator)

    def edit(self, **appstruct):

        if appstruct['title']:
            self.context.title = appstruct['title']

        if appstruct['description']:
            self.context.description = appstruct['description']

        if appstruct['body']:
            self.context.body = appstruct['body']

        if appstruct['tags']:
            self.context.tags = appstruct['tags']

        if appstruct['todostate']:
            self.context.todostate = appstruct['todostate']


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


class AddCategoryFormView(AddFormView):
    item_type = _(u"Category")
    item_class = Category

    def schema_factory(self):

        return CategorySchema()

    def add(self, **appstruct):

        return self.item_class(
            title=appstruct['title'],
            description=appstruct['description'],
            body=appstruct['body'],
            tags=appstruct['tags'],
            default_view='folder-view',
            )


class EditCategoryFormView(EditFormView):

    def schema_factory(self):

        return CategorySchema()

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

        settings = todos_settings()

        return {
            'api': template_api(self.context, self.request),
            'macros': get_renderer('templates/macros.pt').implementation(),
            'settings': settings,
            }


@view_defaults(context=Category,
               permission='view')
class CategoryView(BaseView):

    @view_config(
             renderer="kotti_todos:templates/category-view.pt")
    def view(self):

        session = DBSession()

        query = (session.query(TodoItem)
                .filter(TodoItem.parent_id == self.context.id)
                .order_by(TodoItem.todostate)
                .order_by(TodoItem.modification_date.desc())
                )

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

        query = session.query(Category).filter(
                Category.parent_id == self.context.id)

        items = query.all()

        todos_data = {}
        todos_data['Done'] = 0
        todos_data['Total'] = 0
        todos_data['Pending'] = 0
        todos_data['In Progress'] = 0
        todos_data['Deferred'] = 0
        todos_data['Abandoned'] = 0

        modification_dates_and_items = []

        for item in items:
            if item.children:
                category_done_count = 0
                for todo in item.children:
                    if todo.todostate == 'done':
                        todos_data['Done'] += 1
                        category_done_count += 1
                    if todo.todostate == 'pending':
                        todos_data['Pending'] += 1
                    if todo.todostate == 'in progress':
                        todos_data['In Progress'] += 1
                    if todo.todostate == 'Deferred':
                        todos_data['Deferred'] += 1
                    if todo.todostate == 'Abandoned':
                        todos_data['Abandoned'] += 1

                todos_data['Total'] += len(item.children)

                sorted_todoitems = sorted(item.children, 
                                      key=lambda x: x.modification_date,
                                      reverse=True)
                modification_dates_and_items.append(
                        (sorted_todoitems[0].modification_date,
                         sorted_todoitems[0],
                         category_done_count,
                         item))
            else:
                modification_dates_and_items.append(
                        (item.modification_date, item, 0, item))

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
            'todos_data': todos_data,
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
        EditCategoryFormView,
        context=Category,
        name='edit',
        permission='edit',
        renderer='kotti:templates/edit/node.pt',
        )

    config.add_view(
        AddCategoryFormView,
        name=Category.type_info.add_view,
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
