---
layout: text_page
permalink: /results/
title: Results
---

{% assign results = site.results | sort: 'date' %}

{% if results.size == 0 %}

<div class="jumbotron">
    <h1>
        There are no experiment results to show.
    </h1>
</div>

{% else %}

<div class="list-group results-table">
    <span class="list-group-item list-group-item-primary disabled active">
        <div class="d-flex justify-content-between">
            <h4 class="mb-1">
                Results
            </h4>
            <small>
                <a href="latest/" class="btn btn-warning btn-sm float-right">
                    Latest
                </a>
            </small>
        </div>
    </span>
    {% for result in results reversed %}
        <a href="{{ result.url }}" class="list-group-item">{{ result.title }}</a>
    {% endfor %}
</div>

{% endif %}
