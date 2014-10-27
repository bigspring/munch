munch
=====

A clever little script for installing WP and dependencies in seconds.

instructions
------------

Run the script from Terminal to install munch:
```
./munch.py
```

Thereafter you can simply navigate to your desired directory and run:
```
munch
```

options
-------

The following command line arguments are available:
```
munch -h (or --help)            Display help (exits script)
munch -n (or --name) NAME       Name project directory
munch -b (or --branch) BRANCH   Specify [Lunchbox](https://github.com/bigspring/lunchbox) branch
```

ACHTUNG!
--------

This script removes the following composer-generated directories/files:
```
vendor/
composer.lock
```
