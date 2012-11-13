===========
kotti_todos
===========

This is an extension to the Kotti CMS that adds a discussion todos to a site,
or more than one todos.

`Find out more about Kotti`_

Setting up kotti_todos
======================

This Addon adds three new Content Types to your Kotti site.
To set up the content types add ``kotti_todos.kotti_configure``
to the ``kotti.configurators`` setting in your ini file::

    kotti.configurators = kotti_todos.kotti_configure

Now you can create a todos and add topics and todoitems.

There are different settings to adjust the behavior of the
software.

You can select if the todoitems in the todos overview
should be batched. If you set 
``kotti_todos.todos_settings.use_batching`` to ``true``
(the default value) the todoitems will be shown on separate
pages. If you set it to ``false`` all todoitems are shown
all together on one page::

    kotti_todos.todos_settings.use_batching = false

If you use batching you can choose how many todoitems are
shown on one page. The default value for 
``kotti_todos.todos_settings.pagesize`` is 5::

    kotti_todos.todos_settings.pagesize = 10

You can use auto batching where the next page of the todoitems
is automatically loaded when scrolling down the overview page instead
of showing links to switch the pages. The default for
``kotti_todos.todos_settings.use_auto_batching`` is ``true``::

    kotti_todos.todos_settings.use_auto_batching = false

With ``kotti_todos.todos_settings.link_headline_overview`` you
can control whether the headline of a todoitem in the
todos overview is linked to the todoitem or not. This
setting defaults to ``true``::

    kotti_todos.todos_settings.link_headline_overview = false

Parts of kotti_todos can be overridden with the setting
``kotti_todos.asset_overrides``. Have a look to the 
`Kotti documentation about the asset_overrides setting`_, which is the
same as in ``kotti_todos``.

Be warned: This addon is in alpha state. Use it at your own risk.

Using kotti_todos
====================

Add a todos to your site, then to that add topics, and to those, todoitems.

Work in progress
================

``kotti_todos`` is considered alpha software, not yet suitable for use in
production environments.  The current state of the project is in no way feature
complete nor API stable.  If you really want to use it in your project(s), make
sure to pin the exact version in your requirements.  Not doing so will likely
break your project when future releases become available.

Development
===========

Contributions to ``kotti_todos`` are very welcome.
Just clone its `GitHub repository`_ and submit your contributions as pull requests.

Note that all development is done on the ``develop`` branch. ``master`` is reserved
for "production-ready state".  Therefore, make sure to always base development work
on the current state of the ``develop`` branch.

This follows the highly recommended `A successful Git branching model`_ pattern,
which is implemented by the excellent `gitflow`_ git extension.

Testing
-------

|build status|_

``kotti_todos`` has 100% test coverage.
Please make sure that you add tests for new features and that all tests pass before
submitting pull requests.  Running the test suite is as easy as running ``py.test``
from the source directory (you might need to run ``python setup.py dev`` to have all
the test requirements installed in your virtualenv).


.. _Find out more about Kotti: http://pypi.python.org/pypi/Kotti
.. _Kotti documentation about the asset_overrides setting: http://kotti.readthedocs.org/en/latest/configuration.html?highlight=asset#adjust-the-look-feel-kotti-asset-overrides
.. _GitHub repository: https://github.com/geojeff/kotti_todos
.. _gitflow: https://github.com/nvie/gitflow
.. _A successful Git branching model: http://nvie.com/todoitems/a-successful-git-branching-model/
x.x. |build status| image:: https://secure.travis-ci.org/geojeff/kotti_todos.png?branch=master
x.x. _build status: http://travis-ci.org/geojeff/kotti_todos
