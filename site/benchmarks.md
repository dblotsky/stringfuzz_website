---
layout: text_page
permalink: /benchmarks/
title: String Benchmarks
---

# String Benchmark Results

The figures below compare the performance of [Norn][Norn], [Z3str3][Z3str3],
[Z3seq][Z3seq], and [CVC4][CVC4] on sets of string [instances][instances]
generated by [StringFuzz][stringfuzz]. The full results are available
[here][csv_results] in CSV format.
The experiments are conducted on an Intel® Core™ i7-7560U CPU @ 2.40GHz × 4
with 7.7 GiB Memory. See the SMT-LIB-like syntax supported by each solver
[here][syntax].

***

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

***

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

<!-- links -->
[norn]:   http://user.it.uu.se/~jarst116/norn/
[z3seq]:  https://github.com/mtrberzi/z3/tree/develop
[z3str3]: https://rise4fun.com/z3/tutorialcontent/sequences
[cvc4]:   http://cvc4.cs.stanford.edu/web/2017/07/10/cvc4-1-5-released/

{% capture root_link %}{% link index.md %}{% endcapture %}
{% capture instances_link %}{% link suites/generated.md %}{% endcapture %}
{% capture csv_link %}{% link benchmark_csvs.md %}{% endcapture %}
{% capture syntax_link %}{% link syntax.md %}{% endcapture %}

[stringfuzz]:  {{ root_link | relative_url }}
[instances]:   {{ instances_link | relative_url }}
[csv_results]: {{ csv_link | relative_url }}
[syntax]:      {{ syntax_link | relative_url }}
