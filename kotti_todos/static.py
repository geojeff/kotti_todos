# -*- coding: utf-8 -*-

from fanstatic import Library
from fanstatic import Resource
from js.jquery_form import jquery_form

library = Library('kotti_todos', 'static')
kotti_todos_js = Resource(
    library,
    'kotti_todos.js',
    minified='kotti_todos.min.js',
    depends=[jquery_form, ]
)
