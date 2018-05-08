---
layout: text_page
permalink: /benchmarks/
title: String Benchmarks
---

<div class="container" style="max-width: 1500px; min-width: 700px; margin: auto">
    <h1>String Benchmark Results</h1>
    <br>
    <p>
        The figures below compare the performance of
        <a href="http://user.it.uu.se/~jarst116/norn/">Norn</a>,
        <a href="https://github.com/mtrberzi/z3/tree/develop">Z3str3</a>,
        <a href="https://rise4fun.com/z3/tutorialcontent/sequences">Z3seq</a>,
        and
        <a href="http://cvc4.cs.stanford.edu/web/2017/07/10/cvc4-1-5-released/">CVC4</a>
        on sets of string
        <a href="https://github.com/FedericoAureliano/StringSMTBenchmarks/tree/master/problems">benchmarks</a>
        generated by
        <a href="http://stringfuzz.dmitryblotsky.com/">StringFuzz</a>.
        The full results are available
        <a href="https://github.com/FedericoAureliano/StringSMTBenchmarks/tree/master/results">here</a>
        in csv format.
        The experiments are conducted on an Intel® Core™ i7-7560U CPU @ 2.40GHz × 4
        with 7.7 GiB Memory. See the SMT-LIB-like syntax supported by each solver
        <a href="./syntax.html">here</a>.
    </p>
    <br>
    <hr>
    <div class="row">
        <div class="col-6">
            <object data="{{ "/static/svg/plots/overall_cactus.svg" | relative_url }}" type="image/svg+xml">
                <img src="{{ "/static/svg/plots/overall_cactus.svg" | relative_url }}" />
            </object>
        </div>
        <div class="col-6">
            <object data="{{ "/static/svg/plots/overall_bar.svg" | relative_url }}" type="image/svg+xml">
                <img src="{{ "/static/svg/plots/overall_bar.svg" | relative_url }}" />
            </object>
        </div>
    </div>
    <br>
    <hr>
    <br>
    <div class="row">
        <div class="col-6">
            <object data="{{ "/static/svg/plots/models_dots.svg" | relative_url }}" type="image/svg+xml">
                <img src="{{ "/static/svg/plots/models_dots.svg" | relative_url }}" />
            </object>
        </div>
        <div class="col-6">
            <object data="{{ "/static/svg/plots/models_bars.svg" | relative_url }}" type="image/svg+xml">
                <img src="{{ "/static/svg/plots/models_bars.svg" | relative_url }}" />
            </object>
        </div>
    </div>
    <br>
    <hr>
    <br>

    {% for suite in site.data.problems %}
    <div class="row">
        <div class="col-6">
            <object data="{{
                    "/static/svg/plots/"
                    | append: suite.name
                    | append: "_cactus.svg"
                    | relative_url }}" type="image/svg+xml">
                <img src="{{
                    "/static/svg/plots/"
                    | append: suite.name
                    | append: "_cactus.svg"
                    | relative_url }}" />
            </object>
        </div>
        <div class="col-6">
            <object data="{{
                    "/static/svg/plots/"
                    | append: suite.name
                    | append: "_bar.svg"
                    | relative_url }}" type="image/svg+xml">
                <img src="{{
                    "/static/svg/plots/"
                    | append: suite.name
                    | append: "_bar.svg"
                    | relative_url }}" />
            </object>
        </div>
    </div>
    {% endfor %}

</div>