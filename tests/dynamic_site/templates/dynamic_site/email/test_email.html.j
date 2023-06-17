{% extends 'django_logikal/email/base.html.j' %}

{% block subject %}
  Test Email Subject
{% endblock %}

{% block description %}This is a test email.{% endblock %}

{% block head %}
  <style data-premailer="ignore">
    {{ include_static('email/style_head.css') }}
  </style>
  <style>
    {{ include_static('email/style.css') }}
  </style>
{% endblock %}

{% block body %}
  <script>/* script contents should not appear in markdown */</script>
  <style>/* style contents should not appear in markdown */</style>

  <h1>Test Email</h1>
  <p>A paragraph with <b>bold</b>, <i>italic</i> and <em>emphasized</em> text.</p>
  <p>A paragraph with <span>styled words</span> in the text.</p>
  <blockquote><p>A quote.</p></blockquote>
  <p>A paragraph with <code>code</code> in the text.</p>
  <hr>
  <p>
    A paragraph with a line break<br>
    and an <em>emphasized <em>word</em> inside an emphasis</em>.
  </p>
  <div>A paragraph in a div element.</div>
  <div>Another paragraph in a div element.</div>

  <h2>Lists</h2>

  <h3>Ordered List</h3>
  <ol>
    <li>First item</li>
    <li>Second item</li>
  </ol>

  <h3>Unordered List</h3>
  <ul>
    <li>First item</li>
    <li>Second item</li>
  </ul>

  <h2>Elements</h2>
  <p>Link: <a href='{{ url('dynamic_site:index') }}'>Index</a></p>
  <p>
    Image:
    <img alt="Logikal icon" width="100" height="100" border="0"
         src="{{ image(static_path('favicon.png')) }}">
  </p>
{% endblock %}
