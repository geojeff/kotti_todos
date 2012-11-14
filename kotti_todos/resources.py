from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String

from zope.interface import implements

from kotti.resources import IDocument
from kotti.resources import IDefaultWorkflow
from kotti.resources import Document

from kotti_todos import _


class Todos(Document):
    implements(IDocument, IDefaultWorkflow)

    id = Column('id', Integer, ForeignKey('documents.id'), primary_key=True)

    type_info = Document.type_info.copy(
        name=u'Todos',
        title=_(u'Todos'),
        add_view=u'add_todos',
        addable_to=[u'Document'],
        )

    def __init__(self, **kwargs):
        super(Todos, self).__init__(**kwargs)

        self.default_view = 'folder-view'


class Category(Document):
    implements(IDocument, IDefaultWorkflow)

    id = Column('id', Integer, ForeignKey('documents.id'), primary_key=True)

    type_info = Document.type_info.copy(
        name=u'Category',
        title=_(u'Category'),
        add_view=u'add_category',
        addable_to=[u'Todos'],
        )

    def __init__(self, **kwargs):
        super(Category, self).__init__(**kwargs)

        self.default_view = 'folder-view'


class TodoItem(Document):
    implements(IDocument, IDefaultWorkflow)

    id = Column(Integer, ForeignKey('documents.id'), primary_key=True)

    todostate = Column('todostate', String(1000))

    type_info = Document.type_info.copy(
        name=u'TodoItem',
        title=_(u'TodoItem'),
        add_view=u'add_todoitem',
        addable_to=[u'Category'],
        )

    def __init__(self, todostate="pending", **kwargs):
        super(TodoItem, self).__init__(**kwargs)

        self.todostate = todostate
