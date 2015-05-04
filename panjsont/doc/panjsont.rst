..
 Copyright (c) 2012 Kevin Steves <kevin.steves@pobox.com>

 Permission to use, copy, modify, and distribute this software for any
 purpose with or without fee is hereby granted, provided that the above
 copyright notice and this permission notice appear in all copies.

 THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
 WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
 MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
 ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
 WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
 ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
 OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

===========
panjsont.py
===========

-------------------------------------------------
command line program for executing JSON templates
-------------------------------------------------

NAME
====

 panjsont.py - command line program for executing JSON templates

SYNOPSIS
========

 panjsont.py [options]
    --jt template         path to JSON template
    --json dict           path to JSON dictionary or '-' for stdin
    --debug level         enable debug level up to 3
    --help                display usage

DESCRIPTION
===========

 **panjsont.py** is used to execute a *JSON Template* (described
 below) on a JSON dictionary.  It can be used with **panxapi.py** and
 **panconf.py** to create custom reports for portions of PAN-OS XML
 configurations.

 The options are:

 ``--jt`` *template*
  Specify path to JSON template.

 ``--json`` *dict*
  Specify path to JSON dictionary or '-' to read from **stdin**.

  **panconf.py** can be used to convert XML to JSON.

 ``--debug`` *level*
  Enable debugging in **panjsont.py**.  *level* is an integer in the
  range 0-3; 0 specifies no debugging and 3 specifies maximum
  debugging.

 ``--help``
  Display **panjsont.py** command options.

JSON Template
-------------

 *JSON Template* is a minimal but powerful templating language for
 transforming a JSON dictionary to arbitrary text; it is described at
 http://code.google.com/p/json-template/.

 When a node in a PAN-OS XML configuration document is coverted to
 JSON using **panconf.py**, a *JSON Template* can be used to transform
 the JSON dictionary to various custom output formats, including:

 - set format CLI output
 - set format CLI-like output
 - custom text output
 - HTML output
 - something else

 Some of the examples below demonstrate converting the **address** and
 **address-group** XML nodes to their corresponding set format CLI
 output.  Set format CLI output can be displayed on PAN-OS using the
 following: ::

  > set cli config-output-format set
  > configure
  # show address
  # show address-group 

 **panjsont.py** uses the Python **jsontemplate** module of *JSON
 Template* and its ``FromString`` class constructor:
 ::

  import jsontemplate

  jt = jsontemplate.FromString(template,
                               more_formatters=fmt.formatters())
  s = jt.expand(json_dict)
  print(s, end='')

Built-in Custom Formatters
~~~~~~~~~~~~~~~~~~~~~~~~~~

 Several built-in custom formatters are provided for use in *JSON
 templates*.  These are implemented in the ``lib/formatters.py``
 module.

 **NOTE: These are subject to change.**

 *yesno*
  Format bool objects with the strings 'yes' and 'no'.

 *quote*
  Quote a string with double quotes (").

 *quote_space*
  Quote a string with double quotes (") if the string contains a space.

 *c14n*
  Canonicalize a bool or string object using *yesno* and *quote_space*.

 *list*
  Format a list using *c14n* as ``[ item1, item2 ]``.

 *dict*
  Format a dictionary using *c14n* as ``[ key1 value1 ]``.
  Multi-key dictionaries are newline separated:
  ::

   [ key1 value1 ]
   [ key2 value2 ]

User-defined Custom Formatters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

 User-defined custom formatters can be defined by creating a
 **formatters2** module and placing it in Python's module search
 path. See ``lib/formatters2-example.py`` for an example module which
 implements a *dummy* formatter and ``lib/formatters.py`` for the
 module that implements the built-in formatters.

FILES
=====

 ``jsont/``
  Directory of sample JSON templates.

 ``lib/formatters.py``
  Module implementing built-in formatters.

 ``lib/formatters2-example.py``
  User-defined formatters example.


EXIT STATUS
===========

 **panjsont.py** exits with 0 on success and 1 if an error occurs.

EXAMPLES
========

 Convert address entries to JSON with **panconf.py**.
 ::

  $ panconf.py --config config.xml --json \
  > ./devices/entry/vsys/entry/address >address.json

 Convert address-group entries to JSON with **panconf.py**.
 ::

  $ panconf.py --config config.xml --json \
  > ./devices/entry/vsys/entry/address-group >address-group.json

 Print address entries using address CLI template.
 ::

  $ panjsont.py --json address.json --jt ../jsont/address-cli.jsont
  set address net5501 ip-netmask 172.29.9.109/32
  set address net5501 description "ssh gateway"
  set address pa200 ip-netmask 172.29.9.126/32
  set address pa200 description "exterior firewall"
  set address pa500 ip-netmask 172.29.9.125/32
  set address smtp ip-netmask 172.29.9.101/32
  set address "web servers" ip-range 10.1.1.1-10.1.1.5
  set address google fqdn google.com
  # No address-group entries

 Print address-group entries using address CLI template.
 ::

  $ panjsont.py --json address-group.json --jt ../jsont/address-cli.jsont
  # No address entries
  set address-group bastion-hosts [ smtp net5501 ]
  set address-group firewalls [ pa200 pa500 ]

 Display address-cli.jsont template.
 ::

  $ cat ../jsont/address-cli.jsont
  default-formatter: c14n

  {# xpath ./devices/entry/vsys/entry/address}
  {.section address}
    {.repeated section entry}
       {.section ip-netmask}
  set address {name} ip-netmask {ip-netmask}
       {.end}
       {.section fqdn}
  set address {name} fqdn {fqdn}
       {.end}
       {.section ip-range}
  set address {name} ip-range {ip-range}
       {.end}
       {.section description}
  set address {name} description {description}
       {.end}
    {.end}
  {.or}
  # No address entries
  {.end}
  {# xpath ./devices/entry/vsys/entry/address-group}
  {.section address-group}
    {.repeated section entry}
  set address-group {name} {member|list}
    {.end}
  {.or}
  # No address-group entries
  {.end}

 Print predefined applications using **panxapi.py**, **panconf.py** and
 **panjsont.py** in a pipeline.
 ::

  $ panxapi.py -t pa-200 -rxg /config/predefined/application |
  > panconf.py --config - --json | panjsont.py --jt ../jsont/apps.jsont --json -
  120 100bao 5 general-internet file-sharing
  1402 1und1-mail 3 collaboration email
  781 2ch 2 collaboration social-networking
  783 2ch-posting 2 collaboration web-posting
  685 360-safeguard-update 2 business-systems software-update
  350 3pc 1 networking ip-protocol
  572 4shared 4 general-internet file-sharing
  1385 51.com-base 2 collaboration social-networking

 Display apps.jsont template.
 ::

  $ cat ../jsont/apps.jsont
  {# use output from: $ panxapi -rxg /config/predefined/application}
  {.section application}
    {.repeated section entry}
  {id} {name} {risk} {category} {.subcategory?}{subcategory}{.or}_nosubcategory_{.end}
    {.end}
  {.end}

SEE ALSO
========

 panxapi.py
  https://github.com/kevinsteves/pan-python/blob/master/doc/panxapi.rst

 panconf.py
  https://github.com/kevinsteves/pan-python/blob/master/doc/panconf.rst

 JSON Template home
  http://code.google.com/p/json-template/

 JSON Template reference
  http://code.google.com/p/json-template/wiki/Reference

 JSON Template group
  http://groups.google.com/group/json-template

AUTHORS
=======

 Kevin Steves <kevin.steves@pobox.com>
