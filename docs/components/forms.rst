Forms
=====
All forms come with a set of standard styles for common form elements.

Input Fields
------------
.. jinja:example::

    <form>
      <div class="input-field">
        <label for="form-example-text">Text field</label>
        <input type="text" id="form-example-text" placeholder="Placeholder">
      </div>

      <div class="input-field">
        <label for="form-example-disabled">Disabled field</label>
        <input type="text" id="form-example-disabled" value="Disabled" disabled>
      </div>

      <div class="input-field">
        <label for="form-example-read-only">Read-only field</label>
        <input type="text" id="form-example-read-only" value="Read-only" readonly>
      </div>
    </form>

Password Field
--------------
.. jinja:example::

    <form>
      <div class="input-field">
        <label for="form-example-password">Password</label>
        <div class="password-input">
          <input name="password" type="password" id="form-example-password">
          <button type="button"
                  class="icon toggle"
                  id="form-example-password-toggle"
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
        </div>
        <div class="helptext" id="form-example-password-helptext">
          <a href="/account/password/reset/">{{ _('Forgot your password?') }}</a>
        </div>
      </div>
    </form>

Errors
------
The standard styles make sure that regular Django form errors render just fine.

.. jinja:example::

    <form>
      <h1>Log in</h1>

      <ul class="errors nonfield">
        <li>Invalid password!</li>
        <li>A password must be provided.</li>
      </ul>

      <div class="input-field">
        <label for="form-auth-email">Email address</label>
        <input name="email" type="email" placeholder="email@example.com" id="form-auth-email">
        <ul class="errors">
          <li>Invalid email address!</li>
          <li>The email address must be provided.</li>
        </ul>
      </div>

      <button type="submit" id="form-auth-action" class="active">Next</button>
    </form>
