{% extends 'dynamic_site/base.html.j' %}

{%- macro __object(name, args=none, pre_args='', post_args='', call=false) -%}
  <b>{{ name }}{{ pre_args }}</b><i>
    {%- if args %}{% if call %}{{ args|repr }}{% else %}{{ args }}{% endif %}{% endif -%}
  </i><b>{{ post_args }}</b> &ensp;→&ensp;
  {% if call %}
    {% if args %}{{ context()[name](args) }}{% else %}{{ context()[name]() }}{% endif %}
  {% endif %}
{% endmacro %}

{% macro __function(name, args=none, call=true) %}
  {{ __object(name, args=args, pre_args='(', post_args=')', call=call) }}
{% endmacro %}

{%- macro __function_args(args=none, kwargs=none) -%}
  {%- for arg in args or [] -%}{%- if not loop.first %}, {% endif %}{{ arg|repr }}{%- endfor -%}
  {%- if kwargs -%}
    {%- if args -%}, {% endif %}{% for key, value in kwargs.items() -%}
      {%- if not loop.first -%}, {% endif %}{{ key }}={{ value|repr }}
    {%- endfor -%}
  {%- endif -%}
{%- endmacro -%}

{% macro __filter(value, name, args=none, kwargs=none) %}
  {{ value|repr }}|{{ __object(
    name=name,
    args=__function_args(args=args, kwargs=kwargs),
    pre_args='(' if (args or kwargs),
    post_args=')' if (args or kwargs),
    call=false,
  ) }}{{ filters[name](value, *(args or []), **(kwargs or {})) }}
{% endmacro %}

{% block subtitle %}Templates{% endblock %}
{% block main %}
  <article class="text">
    <hgroup>
      <h1>Templates</h1>
      <p><b>Subpath:</b> {{ arg }}</p>
    </hgroup>

    <h2>Environment</h2>

    <h3>Objects</h3>
    <ul>
      <li>{{ __object('messages') }}{{ messages|list }}</li>
      <li>{{ __object('filters') }}{{ filters.keys()|sort|join(', ') }}</li>
      <li>{{ __object('tests') }}{{ tests.keys()|sort|join(', ') }}</li>
    </ul>

    <h3>Functions</h3>
    <ul>
      <li>
        {{ __function('context', call=false) }}
        {{ context().keys()|reject('startswith', '__')|sort|join(', ') }}
      </li>
      <li>{{ __function('static', 'logikal_logo.svg') }}</li>
      <!-- Note: static_path() is excluded as it is non-determinstic -->
      <li>{{ __function('include_static', 'logikal_logo.svg') }}</li>
      <li>
        {{ __function(
          'url', "'dynamic_site:templates', kwargs={'arg': 'extensions'}, request=request",
          call=false,
        ) }}
        {{ url('dynamic_site:templates', kwargs={'arg': 'extensions'}, request=request) }}
      </li>
      <li>{{ __function('url_name', 'request', call=false) }}{{ url_name(request) }}</li>
      <li>{{ __function('language') }}</li>
      <li>{{ __function('format', call=false) }}{{ re.sub(' at 0x[^>]+', '', format()|str) }}</li>
      <!-- Note: cwd() is excluded as it is non-deterministic -->
      <li>{{ __function('now') }}</li>
    </ul>

    <h3>Context</h3>
    <ul>
      <li><b>class_get_context_data:</b> {{ class_get_context_data }}</li>
      <li><b>class_get_context_data_request:</b> {{ class_get_context_data_request }}</li>
      <li><b>template_extra_context:</b> {{ template_extra_context }}</li>
      <li><b>template_path_extra_context:</b> {{ template_path_extra_context }}</li>
    </ul>

    <h2>Filters</h2>
    <ul>
      <li>{{ __filter('foo bar', 'upper_first') }}</li>
      <li>{{ __filter('foo\nbar', 'join_lines') }}</li>
      <li>{{ __filter('Foo & Bar', 'slugify') }}</li>
      <li>{{ __filter('foo-and-bar', 'unslugify') }}</li>
      <li>{{ __filter('Foo bar & baz', 'wrap') }}</li>
      <li>{{ __filter('Foo\nbar & baz', 'nowrap') }}</li>
      <li>{{ __filter('Foo bar baz', 'truncate', kwargs={'length': 5}) }}</li>
      <li>{{ __filter(['foo', 'bar', 'baz'], 'exclude', args=['bar']) }}</li>
    </ul>

    <h2>Bibliography</h2>
    {% set bib = bibliography('references') %}
    {% set cite = bib.cite %}
    Citations {{ cite('wilson-ux-interviews') }}{{ cite('right-to-privacy') }}
    {{- cite('django-logikal') }}{{ cite('miller-response-time') }}{{ cite('hrc-comment') }}.

    <h3>References</h3>
    {{ bib.references() }}
  </article>
{% endblock %}
