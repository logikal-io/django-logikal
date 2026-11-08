{% extends 'dynamic_site/base.html.j' %}

{% block subtitle %}Account{% endblock %}
{% block main %}
  <div class="spotlight">
    <section class="stack">
      <h1>Account</h1>
      <p>
        <b>Name:</b> {{ request.user.name }}<br>
        <b>Email:</b> {{ request.user.email }}
      </p>

      <form action="{{ url('account_logout') }}" method="post">
        {{ csrf_input }}
        <button type="submit" id="logout" class="active">Log out</button>
      </form>

      <h2>Security</h2>
      {% if not request.user.has_usable_password() %}
        <p>
          You do not have an account password set currently.<br>
          We recommend setting a password.
        </p>
        <p>
          <a id="set-password-link"
             class="button active"
             href="{{ url('account_set_password') }}">Set password</a>
        </p>
      {% else %}
        <p>
          <a id="change-password-link"
             class="button neutral"
             href="{{ url('account_change_password') }}">Change password</a>
        </p>
      {% endif %}

      <h2>Connected Identities</h2>
      {% if social_accounts %}
        <div class="connections">
          {% for account in social_accounts %}
            {% set provider_icon = 'sign-in-with-' + account.provider|lower + '.svg' %}
            <p>{{ include_static('django_logikal/icons/' + provider_icon) }}</p>
            <p>{{ social_providers[account.provider] }}</p>
            <form action="{{ url('socialaccount_connections') }}" method="post">
              {{ csrf_input }}
              <input type="hidden" name="account" value="{{ account.id }}">
              <button type="submit" class="danger">{{ _('Disconnect') }}</button>
            </form>
          {% endfor %}
        </div>
      {% else %}
        <p>There are no connected accounts.</p>
      {% endif %}
    </section>
  </div>
{% endblock %}
