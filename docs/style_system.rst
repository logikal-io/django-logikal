.. role:: css(code)
    :language: css

Style System
============
The ``django-logikal`` components are based on a flexible style system, which can be modified to
the needs of any project. Development will typically start with adjusting the typography and colors
to follow the appropriate brand guidelines. The default values for the layout variables should
already be sufficient for most projects, however, adjustments can be made when necessary.

.. tip:: Remember that you can always override any style in your own style sheets. However, the
   standard values are a result of a meticulous design process, so make sure to do any adjustments
   with great care for usability and a relentless focus on good design principles.

Typography
----------

Font Families
~~~~~~~~~~~~~
A font family is typically a collection of fonts, often organized by weight (e.g. light, regular,
bold, heavy) and style (e.g. italic, regular). The style system ships with the following default
font families:

.. jinja:autocssvars:: django_logikal/static/django_logikal/css/variables.css
    :section: Typography / Font families
    :open:

Font Theme
~~~~~~~~~~
The font theme defines the individual semantic font roles that can be used during development,
including the size, leading, weight and style of a font in a given role.

.. important:: Font sizing and leading variables should only be used in the definition of the
    semantic font roles – they should never be used directly in CSS declarations.

For reference, the style system's default font sizing and leading definitions and semantic font
roles are as follows:

.. jinja:autocssvars:: django_logikal/static/django_logikal/css/variables.css
    :section: Typography / Font sizing

.. jinja:autocssvars:: django_logikal/static/django_logikal/css/variables.css
    :section: Typography / Font metric corrections

.. jinja:autocssvars:: django_logikal/static/django_logikal/css/variables.css
    :section: Typography / Font theme
    :open:

Color
-----

Color Palette
~~~~~~~~~~~~~
The color palette is the set of colors available in a given project.

The ``django-logikal`` component system comes with a standard light and dark color palette based on
our company design system, however, projects will typically want to use their own color palette,
and overwrite the color theme declarations as necessary.

.. important:: The individual colors should never be used directly in a design – instead, they
   should be assigned to a semantic role (via the :ref:`color theme <style_system:Color Theme>`),
   and the semantic role should be used in the actual CSS declarations.

For reference, the color palette shipping with the component system is as follows:

.. jinja:autocssvars:: django_logikal/static/django_logikal/css/themes/standard-light.css
    :section: Color palette (light mode)

.. jinja:autocssvars:: django_logikal/static/django_logikal/css/themes/standard-dark.css
    :section: Color palette (dark mode)

Color Theme
~~~~~~~~~~~
A color theme assigns the color palette colors to semantic roles. The standard roles of the
component system are as follows:

.. jinja:autocssvars:: django_logikal/static/django_logikal/css/themes/standard-light.css
    :section: Color theme (light mode)
    :open:

.. jinja:autocssvars:: django_logikal/static/django_logikal/css/themes/standard-dark.css
    :section: Color theme (dark mode)

Layout
------
Consistency in padding and margin values is paramount in good web application design. Appropriate
spacing helps the user conceptually separate different areas in a user interface, which in turn
makes the user interface easier to use.

Spacing & Splits
~~~~~~~~~~~~~~~~
The style system comes with the following semantic spacing and splitting elements:

.. jinja:autocssvars:: django_logikal/static/django_logikal/css/variables.css
    :section: Layout / Spacing
    :open:

.. jinja:autocssvars:: django_logikal/static/django_logikal/css/variables.css
    :section: Layout / Splits
    :open:

Text Margins
~~~~~~~~~~~~
The style system generally aligns the space before and after headings according to the golden
ratio, and uses multiples of body leading as the total height to achieve baseline consistency in
multi-column text arrangements. For subheadings we switch to using an equal spacing, as the
difference between the golden ratio major and minor segments at that scale is too subtle to be
interpreted as an intentional design choice.

.. jinja:autocssvars:: django_logikal/static/django_logikal/css/variables.css
    :section: Layout / Text margins / Heading heights
    :open:

.. jinja:autocssvars:: django_logikal/static/django_logikal/css/variables.css
    :section: Layout / Text margins / Margin components

.. jinja:autocssvars:: django_logikal/static/django_logikal/css/variables.css
    :section: Layout / Text margins / Margins
    :open:

Elements
~~~~~~~~
The element sizes defined by the style system are as follows:

.. jinja:autocssvars:: django_logikal/static/django_logikal/css/variables.css
    :section: Layout / Elements
    :open:
