---
layout: text_page
permalink: /results/
title: Results
---

{% assign results = site.results | sort: 'date' %}

<div class="list-group results-table">
    <a href="latest/" class="list-group-item list-group-item-primary">
        Latest
    </a>
    {% for result in results reversed %}
        <a href="{{ result.url }}" class="list-group-item">{{ result.title }}</a>
    {% endfor %}
</div>
