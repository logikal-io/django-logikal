{% if form.Meta.render_tag %}
  <form action="{{
    url(form.Meta.action_url_name, request=request, kwargs=form.action_url_kwargs)
  }}" method="post" id="{{ form.Meta.id_prefix }}_{{ form.Meta.id }}">
{% endif %}
{% if form.Meta.header %}<h1>{{ form.Meta.header }}</h1>{% endif %}
{% if form.Meta.help_text %}<div class="helptext">{{ form.Meta.help_text }}</div>{% endif %}
{{ csrf_input }}
{{ errors }}
{% if errors and not fields %}
  <div>{% for field in hidden_fields %}{{ field }}{% endfor %}</div>
{% endif %}
{% for field, errors in fields %}
  <div class="input-field{% if field.css_classes() %} {{ classes }}{% endif %}">
    {{ field.as_field_group() }}
    {% if loop.last %}
      {% for field in hidden_fields %}{{ field }}{% endfor %}
    {% endif %}
  </div>
{% endfor %}
{% if not fields and not errors %}
  {% for field in hidden_fields %}{{ field }}{% endfor %}
{% endif %}
{% if form.Meta.action_button_text %}
  {% if form.Meta.back_url_name %}<div class="actions">{% endif %}
  <button>{{ form.Meta.action_button_text }}</button>
  {% if form.Meta.back_url_name %}
    <a href="{{ url(form.Meta.back_url_name, request=request, kwargs=form.back_url_kwargs) }}"
       class="button neutral">{{ form.Meta.back_url_text }}</a>
  {% endif %}
  {% if form.Meta.back_url_name %}</div>{% endif %}
{% endif %}
{% if form.Meta.render_tag %}</form>{% endif %}
