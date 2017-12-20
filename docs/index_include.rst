.. module:: score.sass
.. role:: confkey
.. role:: confdefault

**********
score.sass
**********

A small module that registers a :class:`score.tpl.Renderer` for scss and sass
file types with :mod:`score.tpl`.


Quickstart
==========

Usually, it is sufficient to add this module to your initialization list:


.. code-block:: ini

    [score.init]
    modules =
        score.tpl
        score.css
        score.sass


API
===

.. autofunction:: init

.. autoclass:: ConfiguredSassModule()

.. autoclass:: SassRenderer()
