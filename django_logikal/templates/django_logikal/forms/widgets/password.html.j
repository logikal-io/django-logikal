<div class="password-input">
  {% include 'django_logikal/forms/widgets/input.html.j' %}
  <button type="button" class="icon-toggle"
          aria-label="{{ _('Show password') }}" title="{{ _('Show password') }}">
    <span class="inactive" aria-hidden="true">{{ include_static(widget['icon_show']) }}</span>
    <span class="active" aria-hidden="true">{{ include_static(widget['icon_hide']) }}</span>
  </button>
</div>
