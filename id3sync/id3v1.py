#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, division, absolute_import
from __future__ import print_function

__all__ = [
        'ID3V1_GENRE_LIST',
        'parse_ID3v1',
        'parse_ID3v1_file',
        ]

import six

ID3V1_GENRE_LIST = [
        # 0-19
        'Blues', 'Classic Rock', 'Country', 'Dance', 'Disco',
        'Funk', 'Grunge', 'Hip-Hop', 'Jazz', 'Metal',
        'New Age', 'Oldies', 'Other', 'Pop', 'R&B',
        'Rap', 'Reggae', 'Rock', 'Techno', 'Industrial',
        # 20-39
        'Alternative', 'Ska', 'Death Metal', 'Pranks', 'Soundtrack',
        'Euro-Techno', 'Ambient', 'Trip-Hop', 'Vocal', 'Jazz+Funk',
        'Fusion', 'Trance', 'Classical', 'Instrumental', 'Acid',
        'House', 'Game', 'Sound Clip', 'Gospel', 'Noise',
        # 40-59
        'AlternRock', 'Bass', 'Soul', 'Punk', 'Space',
        'Meditative', 'Instrumental Pop', 'Instrumental Rock', 'Ethnic',
        'Gothic',
        'Darkwave', 'Techno-Industrial', 'Electronic', 'Pop-Folk',
        'Eurodance',
        'Dream', 'Southern Rock', 'Comedy', 'Cult', 'Gangsta Rap',
        # 60-79
        'Top 40', 'Christian Rap', 'Pop / Funk', 'Jungle', 'Native American',
        'Cabaret', 'New Wave', 'Psychedelic', 'Rave', 'Showtunes',
        'Trailer', 'Lo-Fi', 'Tribal', 'Acid Punk', 'Acid Jazz',
        'Polka', 'Retro', 'Musical', 'Rock & Roll', 'Hard Rock',
        # 80-99
        'Folk', 'Folk-Rock', 'National Folk', 'Swing', 'Fast',
        'Bebob', 'Latin', 'Revival', 'Celtic', 'Bluegrass',
        'Avantgarde', 'Gothic Rock', 'Progressive Rock', 'Psychedelic Rock',
        'Symphonic Rock',
        'Slow Rock', 'Big Band', 'Chorus', 'Easy Listening', 'Acoustic',
        # 100-119
        'Humour', 'Speech', 'Chanson', 'Opera', 'Chamber Music',
        'Sonata', 'Symphony', 'Booty Bass', 'Primus', 'Porn Groove',
        'Satire', 'Slow Jam', 'Club', 'Tango', 'Samba',
        'Folklore', 'Ballad', 'Power Ballad', 'Rhythmic Soul', 'Freestyle',
        # 120-139
        'Duet', 'Punk Rock', 'Drum Solo', 'A Cappella', 'Euro-House',
        'Dance Hall', 'Goa', 'Drum & Bass', 'Club-House', 'Hardcore',
        'Terror', 'Indie', 'BritPop', 'Negerpunk', 'Polsk Punk',
        'Beat', 'Christian Gangsta Rap', 'Heavy Metal', 'Black Metal',
        'Crossover',
        # 140-148
        'Contemporary Christian', 'Christian Rock', 'Merengue', 'Salsa',
        'Thrash Metal',
        'Anime', 'JPop', 'Synthpop', 'Rock/Pop',
        ]


def parse_text(b, enc, errors='replace'):
    '''Parse zero-padded bytes into string, according to the encoding given.

        >>> from __future__ import print_function
        >>> import six
        >>> result = parse_text(
        ...         b'\\x83W\\xa4\\xe9\\xa4\\xcf\\xbd\\xf1\\xa4\\xce'
        ...         b'\\xa4\\xca\\xa4\\xab\\xa4\\xc7\\x00\\x00\\x00\\x00'
        ...         b'\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00',
        ...         'gb18030',
        ...         )
        >>> isinstance(result, six.text_type)
        True
        >>> print(result)
        僕らは今のなかで

    The binary array is also allowed to have no zero bytes:

        >>> from __future__ import print_function
        >>> import six
        >>> result = parse_text(
        ...         b'\\xcf\\xa3\\xcd\\xfb\\xa4\\xcb\\xa4\\xc4\\xa4\\xa4'
        ...         b'\\xa4\\xc6\\xa3\\xaf\\x89\\xf4\\xa4\\xcf\\xba\\xce'
        ...         b'\\xb6\\xc8\\xa4\\xe2\\xc9\\xfa\\xa4\\xde\\xa4\\xec',
        ...         'gb18030',
        ...         )
        >>> isinstance(result, six.text_type)
        True
        >>> print(result)
        希望について／夢は何度も生まれ

    '''

    try:
        idx = b.index(b'\x00')
    except ValueError:
        # Actually this is not needed...
        # raise ValueError('bytes object is not zero-padded')
        idx = None

    content = b if idx is None else b[:idx]
    return content.decode(enc, errors)


def parse_year_field(b):
    '''Parse year into integer. This is just a wrapper of int(), obviously ;-P

        >>> import six
        >>> result = parse_year_field(b'2014')
        >>> isinstance(result, six.integer_types)
        True
        >>> result
        2014

    '''

    return int(b.decode('ascii'))


def parse_genre_byte(b):
    '''Parse the ID3v1 genre byte into the corresponding genre name.

        >>> from __future__ import print_function
        >>> import six
        >>> result = parse_genre_byte(b'\\x91')
        >>> isinstance(result, six.text_type)
        True
        >>> print(result)
        Anime

    Invalid bytes are mapped to the empty string:

        >>> result = parse_genre_byte(b'\\xff')
        >>> len(result)
        0

    '''

    try:
        return ID3V1_GENRE_LIST[ord(b)]
    except IndexError:
        return ''


def parse_track_field(b):
    '''Parse the track number byte, if present.

        >>> parse_track_field(b'\\x00\\x02')
        2
        >>> parse_track_field(b'\\x41\\x00') is None
        True

    '''

    # No track number if comment length exceeds 28, that is b[0] != b'\x00'
    return ord(b[1]) if b[0] == b'\x00' else None


def parse_ID3v1(tag, enc='utf-8', errors='replace'):
    '''Parse ID3v1 metadata.

        >>> from __future__ import print_function
        >>> example1 = parse_ID3v1(
        ...         b'TAG'
        ...         # Title
        ...         b'\\x83W\\xa4\\xe9\\xa4\\xcf\\xbd\\xf1\\xa4\\xce'
        ...         b'\\xa4\\xca\\xa4\\xab\\xa4\\xc7\\x00\\x00\\x00\\x00'
        ...         b'\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00'
        ...         # Artist
        ...         b"\\xa6\\xcc's\\x00\\x00\\x00\\x00\\x00\\x00"
        ...         b'\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00'
        ...         b'\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00'
        ...         # Album, without any zero byte
        ...         b'\\x83W\\xa4\\xe9\\xa4\\xcf\\xbd\\xf1\\xa4\\xce'
        ...         b'\\xa4\\xca\\xa4\\xab\\xa4\\xc7\\x00\\x00\\x00\\x00'
        ...         b'\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00'
        ...         # Year
        ...         b'2013'
        ...         # Comment
        ...         b'\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00'
        ...         b'\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00'
        ...         b'\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00'
        ...         # ID3v1.1: Track number
        ...         b'\\x00\\x01'
        ...         # Genre
        ...         b'\\x91',
        ...         # Encoding
        ...         'gb18030',
        ...         )
        >>> print(example1['title'])
        僕らは今のなかで
        >>> print(example1['artist'])
        μ's
        >>> print(example1['album'])
        僕らは今のなかで
        >>> example1['year']
        2013
        >>> print(example1['comment'])
        <BLANKLINE>
        >>> len(example1['comment'])
        0
        >>> example1['track']
        1
        >>> print(example1['genre'])
        Anime
        >>> example2 = parse_ID3v1(
        ...         b'TAG'
        ...         # Title
        ...         b'\\x89\\xf4\\xa4\\xcf\\xba\\xce\\xb6\\xc8\\xa4\\xe2'
        ...         b'\\xc9\\xfa\\xa4\\xde\\xa4\\xec\\x89\\xe4\\xa4\\xef'
        ...         b'\\xa4\\xeb\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00'
        ...         # Artist
        ...         b'NO NAME\\x00\\x00\\x00'
        ...         b'\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00'
        ...         b'\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00'
        ...         # Album
        ...         b'\\xcf\\xa3\\xcd\\xfb\\xa4\\xcb\\xa4\\xc4\\xa4\\xa4'
        ...         b'\\xa4\\xc6\\xa3\\xaf\\x89\\xf4\\xa4\\xcf\\xba\\xce'
        ...         b'\\xb6\\xc8\\xa4\\xe2\\xc9\\xfa\\xa4\\xde\\xa4\\xec'
        ...         # Year
        ...         b'2012'
        ...         # Comment
        ...         b'\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00'
        ...         b'\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00'
        ...         b'\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00'
        ...         # ID3v1.1: Track number
        ...         b'\\x00\\x02'
        ...         # Genre
        ...         b'\\x91',
        ...         # Encoding
        ...         'gb18030',
        ...         )
        >>> print(example2['title'])
        夢は何度も生まれ変わる
        >>> print(example2['artist'])
        NO NAME
        >>> print(example2['album'])
        希望について／夢は何度も生まれ
        >>> example2['year']
        2012
        >>> print(example2['comment'])
        <BLANKLINE>
        >>> len(example2['comment'])
        0
        >>> example2['track']
        2
        >>> print(example2['genre'])
        Anime

    '''

    if not isinstance(tag, six.binary_type):
        raise ValueError('tag must be binary type')

    if len(tag) != 128:
        raise ValueError('ID3v1 tag length must be 128')

    if not tag.startswith(b'TAG'):
        raise ValueError('invalid ID3v1 tag magic')

    title = parse_text(tag[3:33], enc, errors)
    artist = parse_text(tag[33:63], enc, errors)
    album = parse_text(tag[63:93], enc, errors)
    year = parse_year_field(tag[93:97])

    # although overlapping with track number field in ID3v1.1, this is OK
    # because track number, if present, is always prefixed with a zero byte
    comment = parse_text(tag[97:127], enc, errors)
    track = parse_track_field(tag[125:127])

    genre = parse_genre_byte(tag[127])

    return {
            'title': title,
            'artist': artist,
            'album': album,
            'year': year,
            'comment': comment,
            'track': track,
            'genre': genre,
            }


def parse_ID3v1_file(filename, enc='utf-8', errors='replace'):
    '''Parse ID3v1 tag in a file.'''

    with open(filename, 'rb') as fp:
        fp.seek(-128, 2)
        maybe_tag = fp.read(128)

    try:
        result = parse_ID3v1(maybe_tag, enc, errors)
    except ValueError:
        return None

    return result


# vim:set ai et ts=4 sw=4 sts=4 fenc=utf-8:
