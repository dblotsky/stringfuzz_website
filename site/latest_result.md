---
layout: bare
permalink: /results/latest/
---

{% assign results       = site.results | sort: 'date' %}
{% assign latest_result = results | last %}

{% if latest_result %}

<head>
    <meta http-equiv="content-type" content="text/html; charset=utf-8" />
    <meta http-equiv="refresh" content="0;url={{ latest_result.url }}" />
</head>

{% else %}

<head></head>
<body>
    <p>There are no results to show, so there is no latest result.</p>
</body>

{% endif %}
