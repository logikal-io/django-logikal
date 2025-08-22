{% extends 'dynamic_site/base.html.j' %}

{% macro __object(name, args='', pre_args='', post_args='', call=false) %}
  <b>{{ name }}{{ pre_args }}</b><i>
    {%- if args %}{% if call %}{{ args|repr }}{% else %}{{ args }}{% endif %}{% endif -%}
  </i><b>{{ post_args }}</b> &ensp;→&ensp;
  {% if call %}
    {% if args %}{{ context()[name](args) }}{% else %}{{ context()[name]() }}{% endif %}
  {% endif %}
{% endmacro %}

{% macro __function(name, args='', call=true) %}
  {{ __object(name, args=args, pre_args='(', post_args=')', call=call) }}
{% endmacro %}

{% macro __filter(value, name) %}
  {{ value|repr }}|<b>{{ name }}</b> &ensp;→&ensp; {{ filters[name](value) }}
{% endmacro %}

{% block subtitle %}Jinja Extensions{% endblock %}
{% block body %}
  <h1>Jinja Extensions</h1>

  <h2>Environment</h2>
  <ul>
    <li>
      {{ __function('context', call=false) }}
      {{ context().keys()|reject('startswith', '__')|sort|join(', ') }}
    </li>
    <li>{{ __object('filters') }}{{ filters.keys()|sort|join(', ') }}</li>
    <li>{{ __object('tests') }}{{ tests.keys()|sort|join(', ') }}</li>
    <li>{{ __object('messages') }}{{ messages|list }}</li>
    <li>{{ __function('static', 'logikal_logo.svg') }}</li>
    <li>{{ __function('include_static', 'logikal_logo.svg') }}</li>
    <li>
      {{ __function('url', "'dynamic_site:jinja', request=request", call=false) }}
      {{ url('dynamic_site:jinja', request=request) }}
    </li>
    <li>{{ __function('url_name', 'request', call=false) }}{{ url_name(request) }}</li>
    <li>{{ __function('language') }}</li>
    <li>{{ __function('format', call=false) }}{{ re.sub(' at 0x[^>]+', '', format()|str) }}</li>
    <li><b>get_context_data:</b> {{ get_context_data }}</li>
    <li><b>extra_template_data:</b> {{ extra_template_data }}</li>
    <li><b>extra_view_data:</b> {{ extra_view_data }}</li>
  </ul>

  <h2>Filters</h2>
  <ul>
    <li>{{ __filter('foo\nbar', 'join_lines') }}</li>
    <li>{{ __filter('Foo & Bar', 'slugify') }}</li>
    <li>{{ __filter('foo-and-bar', 'unslugify') }}</li>
    <li>{{ __filter('Foo bar & baz', 'wrap') }}</li>
    <li>{{ __filter('Foo\nbar & baz', 'nowrap') }}</li>
  </ul>

  <h2>Bibliography</h2>
  {% set bib = bibliography('references') %}
  {% set cite = bib.cite %}
  Citations {{ cite('wilson-ux-interviews') }}{{ cite('right-to-privacy') }}
  {{- cite('django-logikal') }}{{ cite('miller-response-time') }}{{ cite('hrc-comment') }}.

  <h3>References</h3>
  {{ bib.references() }}
{% endblock %}
