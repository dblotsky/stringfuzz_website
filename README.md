Introduction
============

This repository contains the source code for the StringFuzz website.

Installation
============

This section describes how to install the dependencies needed to generate this website. A Unix-like environment with Make is assumed.

The website uses two programming languages: Python 3 and Ruby 2. Python 3 installation instructions are [here][python_install]. Ruby 2 installation instructions are [here][ruby_install]. **Note**: macOS 10.7+ (Lion) already has Ruby 2, and Ubuntu 14.04+ already has Python 3.

To check that Python 3 is installed, run:

    python3 --version

To check that Ruby 2 is installed, run:

    ruby --version

Now that the languages are installed, the packages that the website requires can be installed. To install the them, run (possibly with `sudo`):

    make install

The website also needs StringFuzz to generate the problem suites. StringFuzz installation instructions are [here][stringfuzz_install].

Finally, the website needs a link to a directory of experiment results. To create a new one, run:

    make link_results RESULTS_DIR={path to the directory where experiment results are stored}

The format of the results is specified in the [Results Format](#results-format) section.

Usage
=====

To build the site, run:

    make build

To serve the site locally on port 4000, run:

    make serve

To only generate the problem suites, run:

    make suites

Deployment
==========

Right now deployment by anyone other than me (Dmitry Blotsky) is unsupported because this site is hosted on a server I own.

Results Format
==============

The results directory contains experiment results: one directory per experiment. The format of each experiment directory's name and contents is as follows:

| Directory | Name Format | Contents |
| --------- | ----------- | -------- |
| Root | `YEAR`-`MONTH`-`DAY`-from-`HOUR`h`MINUTE`m`SECOND`s-to-`HOUR`h`MINUTE`m`SECOND`s | Graphs and Results (optional) directories |
| Graphs | `graphs` | Cactus and Versus directories |
| Results (optional) | `results` | Results files (JSON/CSV), one for each unique tuple: (solver, problem set) |
| Cactus | `cactus` | Cactus plot images, one for each problem set |
| Versus | `versus` | Versus plot images, one for each unique triple of: (solver A, solver B, problem set) |

Here is an example experiment directory:

    2018-01-24-from-08h25m36s-to-10h39m06s
        graphs
            cactus
                concats-balanced-cactus.png
                concats-big-cactus.png
                ...
                regex-small-cactus.png
            versus
                concats-balanced-cvc4-vs-norn.png
                concats-balanced-cvc4-vs-z3str2.png
                concats-balanced-cvc4-vs-z3str3.png
                concats-balanced-norn-vs-cvc4.png
                concats-balanced-norn-vs-z3str2.png
                concats-balanced-norn-vs-z3str3.png
                concats-balanced-z3str2-vs-cvc4.png
                concats-balanced-z3str2-vs-norn.png
                concats-balanced-z3str2-vs-z3str3.png
                concats-balanced-z3str3-vs-cvc4.png
                concats-balanced-z3str3-vs-norn.png
                concats-balanced-z3str3-vs-z3str2.png
                concats-big-cvc4-vs-norn.png
                concats-big-cvc4-vs-z3str2.png
                concats-big-cvc4-vs-z3str3.png
                concats-big-norn-vs-cvc4.png
                concats-big-norn-vs-z3str2.png
                concats-big-norn-vs-z3str3.png
                concats-big-z3str2-vs-cvc4.png
                concats-big-z3str2-vs-norn.png
                concats-big-z3str2-vs-z3str3.png
                concats-big-z3str3-vs-cvc4.png
                concats-big-z3str3-vs-norn.png
                concats-big-z3str3-vs-z3str2.png
                ...
                regex-small-cvc4-vs-norn.png
                regex-small-cvc4-vs-z3str2.png
                regex-small-cvc4-vs-z3str3.png
                regex-small-norn-vs-cvc4.png
                regex-small-norn-vs-z3str2.png
                regex-small-norn-vs-z3str3.png
                regex-small-z3str2-vs-cvc4.png
                regex-small-z3str2-vs-norn.png
                regex-small-z3str2-vs-z3str3.png
                regex-small-z3str3-vs-cvc4.png
                regex-small-z3str3-vs-norn.png
                regex-small-z3str3-vs-z3str2.png
        results
            concats-balanced-cvc4.json
            concats-balanced-norn.json
            concats-balanced-z3str2.json
            concats-balanced-z3str3.json
            concats-big-cvc4.json
            concats-big-norn.json
            concats-big-z3str2.json
            concats-big-z3str3.json
            ...
            regex-small-cvc4.json
            regex-small-norn.json
            regex-small-z3str2.json
            regex-small-z3str3.json

[python_install]: https://www.python.org/downloads/
[ruby_install]: https://www.ruby-lang.org/en/documentation/installation/
[stringfuzz_install]: https://github.com/dblotsky/stringfuzz#installing
