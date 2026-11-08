<div class="password-input">
  {% include 'django_logikal/forms/widgets/input.html.j' %}
  <button type="button"
          class="icon toggle"
          {%- if widget.attrs.get('id') %} id="{{ widget.attrs.id }}-toggle"{% endif %}
          title="{{ _('Show password') }}"
          aria-label="{{ _('Show password') }}"
          data-active-title="{{ _('Hide password') }}"
          data-active-aria-label="{{ _('Hide password') }}">
    <span class="inactive" aria-hidden="false">{{ include_static(widget['icon_show']) }}</span>
    <span class="active" aria-hidden="true">{{ include_static(widget['icon_hide']) }}</span>
  </button>
</div>
