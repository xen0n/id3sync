#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, division, absolute_import
from __future__ import print_function

__all__ = [
        'guess_encoding',
        ]

# common setting for Chinese otaku using Windows? haha
DEFAULT_GUESSED_ENCODINGS = ['gb18030', 'sjis', ]


def guess_encoding(s, guess_encs=None):
    '''Try to detect wrongly encoded strings and correct them. Default is to
    try GB18030 and Shift-JIS encodings; you can specify a list of encodings
    to try in the :param:`guess_encs` parameter.

    >>> from __future__ import unicode_literals, print_function
    >>> s = '\x83W\xa4\xe9\xa4\xcf\xbd\xf1\xa4\xce\xa4\xca\xa4\xab\xa4\xc7'
    >>> success, enc, corrected = guess_encoding(s)
    >>> success
    True
    >>> print(enc)
    gb18030
    >>> print(corrected)
    僕らは今のなかで

    If all encodings fail to decode the binary, the original string is
    returned, and failure is signaled:

    >>> from __future__ import unicode_literals, print_function
    >>> s = '\x83W\xa4\xe9\xa4\xcf\xbd\xf1\xa4\xce\xa4\xca\xa4\xab\xa4\xc7'
    >>> success, enc, corrected = guess_encoding(s, ['big5', 'sjis'])
    >>> success
    False
    >>> enc is None
    True
    >>> corrected == s
    True

    '''

    encs = guess_encs if guess_encs is not None else DEFAULT_GUESSED_ENCODINGS

    # convert (wrongly decoded) Unicode to binary
    binary = s.encode('latin-1')

    for enc in encs:
        try:
            result = binary.decode(enc)
            return True, enc, result
        except UnicodeDecodeError:
            pass

    return False, None, s


# vim:set ai et ts=4 sw=4 sts=4 fenc=utf-8:
