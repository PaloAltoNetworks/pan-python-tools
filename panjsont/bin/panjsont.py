#!/usr/bin/env python

#
# Copyright (c) 2012 Kevin Steves <kevin.steves@pobox.com>
#
# Permission to use, copy, modify, and distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
#

from __future__ import print_function

import sys
import os
import getopt
import json
import pprint

libpath = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(libpath, os.pardir, 'lib')]
import jsontemplate
import formatters

def main():
    options = parse_opts()
    if options['json_template'] is None:
        print('No JSON template', file=sys.stderr)
        usage()
        sys.exit(1)
    if options['json'] is None:
        print('No JSON object', file=sys.stderr)
        usage()
        sys.exit(1)

    template = read_file(options['json_template'])
    json_object = read_file(options['json'])
    try:
        json_dict = json.loads(json_object)
    except ValueError as e:
        print('Invalid JSON: %s' % e, file=sys.stderr)
        sys.exit(1)

    if options['debug']:
        print(template, end='', file=sys.stderr)
        print(json_object, end='', file=sys.stderr)
        print(json_dict, end='', file=sys.stderr)

    fmt = formatters.Fmt()

    # XXX exceptions?
    jt = jsontemplate.FromString(template,
                                 more_formatters=fmt.formatters())
    s = jt.expand(json_dict)
    print(s, end='')

def parse_opts():
    options = {
        'json_template': None,
        'json': None,
        'debug': 0,
        }

    short_options = ''
    long_options = ['help', 'debug=',
                    'jt=', 'json=',
                    ]

    try:
        opts, args = getopt.getopt(sys.argv[1:],
                                   short_options,
                                   long_options)
    except getopt.GetoptError as error:
        print(error, file=sys.stderr)
        usage()
        sys.exit(1)

    for opt, arg in opts:
        if opt == '--jt':
            options['json_template'] = arg
        elif opt == '--json':
            options['json'] = arg
        elif opt == '--debug':
            try:
                options['debug'] = int(arg)
                if options['debug'] < 0:
                    raise ValueError
            except ValueError:
                print('Invalid debug:', arg, file=sys.stderr)
                sys.exit(1)
            if options['debug'] > 3:
                print('Maximum debug level is 3', file=sys.stderr)
                sys.exit(1)
        elif opt == '--help':
            usage()
            sys.exit(0)
        else:
            assert False, 'unhandled option %s' % opt

    return options

def read_file(path):
    if path == '-':
        lines = sys.stdin.readlines()
    else:
        try:
            f = open(path)
        except IOError as msg:
            print('open %s: %s' % (path, msg), file=sys.stderr)
            sys.exit(1)
        lines = f.readlines()
        f.close()

    return ''.join(lines)

def usage():
    usage = '''%s [options]
    --jt template         path to JSON template
    --json dict           path to JSON dictionary or '-' for stdin
    --debug level         enable debug level up to 3
    --help                display usage
'''
    print(usage % os.path.basename(sys.argv[0]), end='', file=sys.stderr)

if __name__ == '__main__':
    main()
