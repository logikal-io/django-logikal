{% extends 'dynamic_site/base.html.j' %}

{% block subtitle %}Models{% endblock %}
{% block body %}
  <h1>Models</h1>

  <h2>Projects</h2>
  <table>
    <thead>
      <tr>
        <th>Status</th>
        <th>Name</th>
        <th>Start Date</th>
        <th>End Date</th>
      </tr>
    </thead>
    <tbody>
      {% for project in projects %}
        <tr>
          <td>{{ project.status }}</td>
          <td>{{ project.name }}</td>
          <td>{{ project.start_date }}</td>
          <td>{{ project.end_date or 'open-ended' }}</td>
        </tr>
      {% endfor %}
    </tbody>
  </table>
{% endblock %}
