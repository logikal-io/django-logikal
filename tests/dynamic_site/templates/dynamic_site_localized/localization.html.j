{% extends 'dynamic_site/base.html.j' %}

{% block subtitle %}{% trans %}Localization{% endtrans %}{% endblock %}
{% block body %}
  <h1>{% trans %}Localization{% endtrans %}</h1>
  {# Translators: This is a template test comment for translators #}
  <h2>{% trans %}Language & Region{% endtrans %}</h2>
  <ul>
    {% for language_code, language_name in settings.LANGUAGES %}
      <li>
        {% if language_code == language() %}
          {{ language_name }}
        {% else %}
          {% language language_code %}
            <a href="{{ url('dynamic_site_localized:localization') }}">{{ language_name }}</a>
          {% endlanguage %}
        {% endif %}
      </li>
    {% endfor %}
  </ul>
  <h2>{% trans %}Translations{% endtrans %}</h2>
  <p>
    {% for cake in range(1, 3) %}
      {% trans 'course' count=cake %}
        There is {{ count }} cake with amazing flavors.
      {% pluralize %}
        There are {{ count }} cakes with amazing flavors.
      {% endtrans %}
      {# Translators: This is an ngettext template test comment for translators #}
      ({{ ngettext('%(num)d color', '%(num)d colors', cake) }})
      {% if not loop.last %}<br>{% endif %}
    {% endfor %}
  </p>
  <p>
    {% trans %}
      This is a long localized text containing multiple sentences that spans more than one line in
      the source file and also in the message file.
    {% endtrans %}
  </p>
  {# Translators: This is a long gettext template test comment for translators that spans more than
one line in the source file and also in the message file #}
  <p>{{ _('The word &ldquo;%(word)s&rdquo; has been localized.', word=_('marvelous')) }}</p>
  <p><b>View data: </b>{{ localized_view_data() }}</p>
  <h2>Formatting</h2>
  <p>
    {% set fmt = format() %}
    <b>Date:</b> {{ fmt.date(date) }}<br>
    <b>Timestamp:</b> {{ fmt.datetime(timestamp, format='long') }}<br>
    {# Note: if you change the following line, make sure to update the docstring of the
    django_logikal.templates.functions.format function as well! #}
    {% language 'en-gb' %}
    {% timezone 'Europe/London' %}
    <b>Timestamp (</b><i>en_GB, Europe/London</i><b>): </b>
      {{ format().datetime(timestamp, format='long') }}<br>
    {% endtimezone %}
    {% endlanguage %}
    <b>Number:</b> {{ fmt.decimal(number) }}<br>
    <b>Currency (</b><i>USD</i><b>):</b> {{ fmt.currency(currency, 'USD') }}<br>
    <b>Currency (</b><i>GBP</i><b>):</b> {{ fmt.currency(currency, 'GBP') }}
  </p>
{% endblock %}
