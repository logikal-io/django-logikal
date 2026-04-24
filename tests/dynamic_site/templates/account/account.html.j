{% extends 'dynamic_site/base.html.j' %}

{% block subtitle %}Account{% endblock %}
{% block main %}
  <div class="spotlight">
    <section class="text center">
      <h1>Account</h1>
      <p>
        <b>Name:</b> {{ request.user.name }}<br>
        <b>Email:</b> {{ request.user.email }}
      </p>

      <h2>Security</h2>
      {% if not request.user.has_usable_password() %}
        <p>
          You do not have an account password set currently.<br>
          We recommend setting a password.
        </p>
        <p><a href="{{ url('account_set_password') }}" class="button inline">Set password</a></p>
      {% else %}
        <p>
          <a href="{{ url('account_change_password') }}" class="button inline">Change password</a>
        </p>
      {% endif %}

      <h2>Connected Identities</h2>
      {% if social_accounts %}
        {% for account in social_accounts %}
          <form action="{{ url('socialaccount_connections') }}" method="post">
            {{ csrf_input }}
            <input type="hidden" name="account" value="{{ account.id }}">
            <p>{{ settings.ALLAUTH_SOCIAL_PROVIDERS[account.provider] }}
              &ensp; <button class="inline neutral">Disconnect</button></p>
          </form>
        {% endfor %}
      {% else %}
        <p>There are no connected accounts.</p>
      {% endif %}

      <h2>Actions</h2>
      <form action="{{ url('account_logout') }}" method="post">
        {{ csrf_input }}
        <p><button>Log out</button></p>
      </form>
    </section>
  </div>
{% endblock %}
