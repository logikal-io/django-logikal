.. role:: css(code)
    :language: css

Style System
============
The ``django-logikal`` component system comes with a standard light and dark color theme, which is
automatically included when using the :func:`~django_logikal.templates.functions.component_styles`
function.

You may override the standard color theme or define your own custom color theme using the following
CSS variables:

.. jinja:autocssvars:: django_logikal/static/django_logikal/css/themes/standard-light.css :root

In addition to the theme colors, you may also override the style system's other design
characteristics via the following CSS variables:

.. jinja:autocssvars:: django_logikal/static/django_logikal/css/variables.css :root

.. tip:: Remember that you can always override any style in your own stylesheets. However, the
   standard values are a result of a meticulous design process, so make sure to do any adjustments
   with great care for usability and a relentless focus on good design principles.
