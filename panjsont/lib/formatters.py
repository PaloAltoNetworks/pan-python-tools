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

import pprint

try:
    basestring
except NameError:
    # Python 3
    basestring = str
try:
    import formatters2
except ImportError:
    pass

_formatters = {}

class Fmt:
    def __init__(self):

        fmt_default = {
            'yesno': f_yesno,
            'quote': f_quote,
            'quote_space': f_quote_space,
            'c14n': f_c14n, # canonical form (canonicalization)
            'list': f_list,
            'dict': f_dict,
            }

        global _formatters
        try:
            formatters2.formatters
            _formatters = dict(list(fmt_default.items()) +
                               list(formatters2.formatters.items()))
        except NameError:
            _formatters = fmt_default
 
        self._formatters = _formatters

    def formatters(self):
        return self._formatters

def f_yesno(o):
    if type(o) != type(True):
        return o

    if o:
        return 'yes'
    else:
        return 'no'

def f_quote(o):
    if isinstance(o, basestring):
        return '"%s"' % o
    else:
        return o

def f_quote_space(o):
    if isinstance(o, basestring) and ' ' in o:
        return f_quote(o)
    else:
        return o

def f_c14n(o):
    if isinstance(o, basestring):
        return f_quote_space(o)
    elif type(o) == type(True):
        return f_yesno(o)
    else:
        return o

def _f_list(o, c14n=False):
    if type(o) != type([]):
        return pprint.pformat(o)

    if c14n:
        s = ' '.join(map(f_c14n, o))
    else:
        s = ' '.join(o)
    return '[ %s ]' % s

def f_list(o):
    return _f_list(o, True)

def _f_dict(o, c14n=False):
    if type(o) != type({}):
        return pprint.pformat(o)

    keys = o.keys()
    l = []
    for key in keys:
        if c14n:
            s = '[ %s %s ]' % (f_c14n(key), f_c14n(o[key]))
        else:
            s = '[ %s %s ]' % (key, o[key])
        l.append(s)
    return '\n'.join(l)

def f_dict(o):
    return _f_dict(o, True)
