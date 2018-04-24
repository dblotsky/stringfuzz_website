---
permalink: /results/latest/
---

<!DOCTYPE html>
<html>
<head>
{% assign results       = site.results | sort: 'date' %}
{% assign latest_result = results | last %}
<meta http-equiv="content-type" content="text/html; charset=utf-8" />
<meta http-equiv="refresh" content="0;url={{ latest_result.url }}" />
</head>
</html>
