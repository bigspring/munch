munch
=====

A clever little script which utilises [lunchbox](https://github.com/bigspring/lunchbox) to install WP and dependencies in seconds.

instructions
------------

Run the script from the repo to install munch (sudo usually required as a file is created in `/usr/local/bin`):
```
sudo ./munch.py
```
This will reinstall existing versions of munch also.

Thereafter you can simply navigate to your desired directory and run:
```
munch
```

options
-------

`munch -h` or `munch --help` will display some usage documentation.

`munch -n NAME` or `munch --name NAME` will assign a name to the new project. If left unspecified, the munch process will prompt you anyway.

`munch -b BRANCH` or `munch --branch BRANCH` will force munch to use a [lunchbox](https://github.com/bigspring/lunchbox) branch called 'BRANCH', if one exists.

ACHTUNG!
--------

This script removes the following composer-generated directories/files:
```
vendor/
composer.lock
```
