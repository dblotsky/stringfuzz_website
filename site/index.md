---
layout: text_page
---

<div class="container">
    <div class="front">
        <h1>StringFuzz</h1>
        <p class="lead">
            An extensible fuzzer for automatically generating and transforming SMT-LIB string constraints, aimed at testing SMT string solvers.
        </p>
    </div>
</div>
<br>

StringFuzz is a problem instance generator and fuzzer for SMT string solvers like [CVC][cvc4], [Z3][z3str3], and [norn][norn]. It is useful for string solver **developers** and **testers**, and can help expose **bugs** and **performance issues**. It can be installed [here][install].

### Strings

Make an **UNSAT** string instance:

```bash
> stringfuzzg overlaps --num-vars 1 --length-of-consts 10
```
```scheme
(set-logic QF_S)
(declare-fun var0 () String)
(assert (= (str.++ "NR5x$!PCZJ" var0) (str.++ var0 "-r#hAhc<w'")))
(check-sat)
```

solve it with CVC4:

```bash
> stringfuzzg overlaps --num-vars 1 --length-of-consts 10 | cvc4 --lang smt
unsat
```

### Regexes

Make a **SAT** regex instance:

```bash
> stringfuzzg -m regex --literal-type increasing --depth 2 --num-terms 2
```
```scheme
(set-logic QF_S)
(declare-fun var0 () String)
(assert (str.in.re var0 (re.++ (re.+ (re.+ (str.to.re "00"))) (re.union (re.+ (str.to.re "11")) (re.+ (str.to.re "22"))))))
(check-sat)
(get-model)
```

solve it with Z3:

```bash
> stringfuzzg -m regex --literal-type increasing --depth 2 --num-terms 2 | z3str3 smt.string_solver=z3str3 -in
sat
(model
  (define-fun var0 () String
    "00000000000000000000000000000000001111")
)
```

### Try It

Explore further by looking at the other generators:

```bash
> stringfuzzg --help
```

and transformers:

```bash
> stringfuzzx --help
```

[cvc4]:    http://cvc4.cs.stanford.edu/web/
[z3str3]:  https://sites.google.com/site/z3strsolver/
[norn]:    http://user.it.uu.se/~jarst116/norn/
[install]: https://github.com/dblotsky/stringfuzz/blob/master/README.md#installing
