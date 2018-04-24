---
layout: text_page
permalink: /problems/
title: Problem Sets
---

<div class="alert alert-info" role="alert">
    All problems in one archive can be found here:
    <a href="{{ "/static/zip/problems.zip" }}">problems.zip</a>.
</div>

<table class="table table-bordered">
    <thead>
        <tr>
            <th scope="col">Name</th>
            <th scope="col">Sample Instances</th>
            <th scope="col"># of Instances</th>
            <th scope="col">SAT/UNSAT</th>
            <th scope="col">Description</th>
        </tr>
    </thead>
    <tbody>
        {% for suite in site.data.problems %}
        <tr>
            <th scope="row">
                <a href="{{ "/static/zip/" | append: suite.name | append: ".zip" | relative_url }}">
                    {{ suite.name }}
                </a>
            </th>
            <td>
                <a href="{{ "/static/txt/samples/"
                    | append: suite.name
                    | append: "-first.smt20.txt"
                    | relative_url }}">first.smt20</a>
                <br/>
                <a href="{{ "/static/txt/samples/"
                    | append: suite.name
                    | append: "-first.smt25.txt"
                    | relative_url }}">first.smt25</a>
                <br/>
                <a href="{{ "/static/txt/samples/"
                    | append: suite.name
                    | append: "-last.smt20.txt"
                    | relative_url }}">last.smt20</a>
                <br/>
                <a href="{{ "/static/txt/samples/"
                    | append: suite.name
                    | append: "-last.smt25.txt"
                    | relative_url }}">last.smt25</a>
            </td>
            <td>{{ suite.count | times: suite.count_each }}</td>
            <td>{{ suite.answer }}</td>
            <td>{{ suite.description | markdownify }}</td>
        </tr>
        {% endfor %}
    </tbody>
</table>
