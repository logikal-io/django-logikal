Common Elements
===============

Layout
------
Our guiding principle is that components are responsible for their own internal layout, and should
therefore avoid specifying external layout characteristics (such as for example margins on the
component itself). Components can and should arrange the elements inside them (using for example
margins or gaps), but should optimally not prescribe or interfere with layouts described on higher
levels.

Pages
~~~~~
The default page layout requires a ``<body>`` element, which should contain a ``<main>`` element as
its direct descendant. Additionally, the ``<header>``, ``<aside>`` and ``<footer>`` optional
elements are also supported (in any combination). The rendering typically follows the `holy grail
layout <https://en.wikipedia.org/wiki/Holy_grail_(web_design)>`_, with the ``<aside>`` element
placed to the right according to the `golden ratio <https://en.wikipedia.org/wiki/Golden_ratio>`_.

Navigation
~~~~~~~~~~
A standard navigation layout is provided with support for a logo, a menu (we recommend using the
`desktop menu <#jinja-macro-commons-desktop_menu>`_ and `mobile menu
<#jinja-macro-commons-mobile_menu>`_ macros), and an optional ``<aside>`` element.

.. jinja:example::

    {% import 'django_logikal/components/commons.html.j' as commons %}

    {% set menu_items = [
      menu_item(title=_('Home'), view_name='main:home'),
      menu_item(title=_('About'), view_name='main:about'),
      menu_item(title=_('Contact'), view_name='main:contact'),
    ] %}

    <nav>
      <a href="{{ url('main:home') }}" class="button logo">
        {{ include_static('django_logikal/images/logikal_logo.svg') }}
      </a>

      {{ commons.desktop_menu(menu_items, request=request|default(none)) }}

      <aside>
        <a class="button active">{{ _('Log in') }}</a>
      </aside>

      {{ commons.mobile_menu(menu_items, request=request|default(none)) }}
    </nav>

.. note:: The breakpoint at which the design switches from the desktop layout to the mobile layout
   needs to be specified explicitly in each project’s own style sheets. The switching can be done
   using an approach similar to the following declarations:

    .. code-block:: text

        @media (width <= 68.75rem) {
          nav {
            grid-template: 'logo menu-icon' / 1fr auto;
            & > menu.desktop { display: none; }
            & > aside { display: none; }
            & > .menu-mobile-container { display: block; }
          }
        }

Buttons
-------

Text Buttons
~~~~~~~~~~~~
.. jinja:example::

    <div class="button-group">
      <!-- Links -->
      <div class="button-group horizontal">
        <a class="button">{{ _('Button') }}</a>
        <a class="button disabled">{{ _('Disabled') }}</a>
        <a class="button active">{{ _('Active') }}</a>
        <a class="button neutral">{{ _('Neutral') }}</a>
        <a class="button danger">{{ _('Danger') }}</a>
      </div>

      <!-- Buttons -->
      <div class="button-group horizontal">
        <button type="button">{{ _('Button') }}</button>
        <button type="button" class="disabled">{{ _('Disabled') }}</button>
        <button type="button" class="active">{{ _('Active') }}</button>
        <button type="button" class="neutral">{{ _('Neutral') }}</button>
        <button type="button" class="danger">{{ _('Danger') }}</button>
      </div>
    </div>

Icon Buttons
~~~~~~~~~~~~
.. jinja:example::

    <div class="button-group horizontal">
      <!-- Icon-only button -->
      <button type="button" class="icon">
        {{ include_static('django_logikal/icons/x.svg') }}
      </button>

      <!-- Icon-only toggle -->
      <button type="button"
              class="icon toggle"
              title="{{ _('Show password') }}"
              aria-label="{{ _('Show password') }}"
              data-active-title="{{ _('Hide password') }}"
              data-active-aria-label="{{ _('Hide password') }}">
        <span class="inactive" aria-hidden="false">
          {{ include_static('django_logikal/icons/eye-off.svg') }}
        </span>
        <span class="active" aria-hidden="true">
          {{ include_static('django_logikal/icons/eye.svg') }}
        </span>
      </button>

      <!-- Icon and text button -->
      <button type="button" class="icon text">
        {{ include_static('django_logikal/icons/x.svg') }}
        <span>{{ _('Close') }}</span>
      </button>
    </div>

Icon Link Buttons
~~~~~~~~~~~~~~~~~
.. jinja:example::

    <div class="button-group horizontal">
      <!-- Icon-only button -->
      <a class="button icon">{{ include_static('django_logikal/icons/settings.svg') }}</a>

      <!-- Icon and text button -->
      <a class="button icon text">
        {{ include_static('django_logikal/icons/user-round.svg') }}
        <span>{{ _('Account') }}</span>
      </a>
    </div>

Dialogs
-------

Popover
~~~~~~~
.. jinja:example::

    <div class="example-page example-section">
      <div class="popover">Popover</div>
    </div>

Component Macros
----------------
.. jinja:automodule:: django_logikal/templates/django_logikal/components/commons.html.j

.. automodule:: django_logikal.components.commons
