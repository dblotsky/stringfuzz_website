---
layout: text_page
permalink: /syntax/
title: String and Sequence Syntax
---

<style type="text/css">
    .no {
        color: red;
    }
</style>

<div class="container">
    <h2>SMT-LIB-Like String and Sequence Syntax Support (In Progress)</h2>
    {% for theory in site.data.smt_lib_support %}
    <br>
    <h3>{{ theory.name }}</h3>
    <table class="table table-hover table-sm">
        <thead>
            <tr>
                {% for heading in theory.header %}
                <th scope="col">{{ heading }}</th>
                {% endfor %}
            </tr>
        </thead>
        <tbody>
            {% for row in theory.expressions %}
            <tr>
                {% for column in row %}
                    {% if forloop.first == true %}
                        <th scope="row">{{ column }}</th>
                    {% elsif column == true %}
                        <td><span class="yes">&check;</span></td>
                    {% elsif column == false %}
                        <td><span class="no">&cross;</span></td>
                    {% else %}
                        <td>{{ column }}</td>
                    {% endif %}
                {% endfor %}
            </tr>
            {% endfor %}
        </tbody>
    </table>
    {% endfor %}
</div>
