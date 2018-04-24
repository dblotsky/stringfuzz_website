Introduction
============

This repository contains the source code for the StringFuzz website.

Installation
============

To build and serve the website locally, some things need to be installed. To install the base dependencies, run (you might need `sudo`):

    make install

It also needs StringFuzz to generate the problem suite. StringFuzz installation instructions are [here][stringfuzz_install].

Finally, it needs a directory of experiment results. To create a new one, run:

    make link_results RESULTS_DIR={path to the directory where experiment results are stored}

Usage
=====

To build the site, run:

    make build

To serve the site locally on port 4000, run:

    make serve

To only generate the problem suite, run:

    make problems

Deployment
==========

Right now deployment by anyone other than me (Dmitry Blotsky) is unsupported because this site is hosted on a server I own.

[stringfuzz_install]: https://github.com/dblotsky/stringfuzz#installing
