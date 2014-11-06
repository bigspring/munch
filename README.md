munch
=====

A clever little script which utilises [lunchbox](https://github.com/bigspring/lunchbox) to install WP and dependencies in seconds.

instructions
------------

Run the script from the repo to install munch (sudo required):
```
sudo ./munch.py
```

Thereafter you can simply navigate to your desired directory and run:
```
munch
```
The former command will ALWAYS reinstall.

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
