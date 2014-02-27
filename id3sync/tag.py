#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, division, absolute_import
from __future__ import print_function

__all__ = [
        ]

import six
from mutagen.id3 import ID3, TDRC, TALB, TRCK, TPE1, TIT2, TCON

from . import id3v1
from . import charset


def fix_tag_encoding(tag):
    if tag.encoding == 0:
        # most likely it's NOT a Latin-1 encoded string (ideally even a
        # Latin-1 string should be stored as UTF-8), try to guess the encoding
        success, enc, result = charset.guess_encoding(tag.text[0])
        if success:
            # construct a UTF-8 tag
            new_tag = type(tag)(encoding=3, text=result)
            return new_tag

    return tag


def fix_text_tag(tag_name, tags_v2, tag_klass, fallback_value):
    if tag_name in tags_v2:
        # correct encoding
        return fix_tag_encoding(tags_v2[tag_name])
    else:
        # construct from fallback, most likely from ID3v1
        return tag_klass(encoding=3, text=fallback_value)


def calculate_ID3v2_tags(tags_v2, tags_v1):
    result = {}

    # Title
    result['TIT2'] = fix_text_tag('TIT2', tags_v2, TIT2, tags_v1['title'])

    # Artist
    result['TPE1'] = fix_text_tag('TPE1', tags_v2, TPE1, tags_v1['artist'])

    # Album
    result['TALB'] = fix_text_tag('TALB', tags_v2, TALB, tags_v1['album'])

    # Year
    result['TDRC'] = fix_text_tag(
            'TDRC',
            tags_v2,
            TDRC,
            six.u(str(tags_v1['year'])),
            )

    # Genre
    result['TCON'] = fix_text_tag('TCON', tags_v2, TCON, tags_v1['genre'])

    return result


def sync_tags(filename, enc='gb18030'):
    tags_v2 = ID3(filename)
    maybe_tags_v1 = id3v1.parse_ID3v1_file(filename, enc)
    if maybe_tags_v1 is None:
        tags_v1 = {
                'title': '',
                'album': '',
                'year': 0,
                'track': 0,
                'artist': '',
                'genre': '',
                }
    else:
        tags_v1 = maybe_tags_v1

    new_tags = calculate_ID3v2_tags(tags_v2, tags_v1)

    for name, tag in six.iteritems(new_tags):
        tags_v2.delall(name)
        tags_v2.add(tag)

    return tags_v2.save()


# vim:set ai et ts=4 sw=4 sts=4 fenc=utf-8:
