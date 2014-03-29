#!/usr/bin/env python
# -----------------------------------------------------------------------------
# Copyright (c) 2013--, scikit-bio development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
# -----------------------------------------------------------------------------
from __future__ import division

from skbio.parse.clustal import (is_clustal_seq_line,
                                 last_space, delete_trailing_number,
                                 MinimalClustalParser)
from skbio.core.exception import RecordError

from unittest import TestCase, main


class ClustalTests(TestCase):

    """Tests of top-level functions."""

    def test_is_clustal_seq_line(self):
        """is_clustal_seq_line should reject blanks and 'CLUSTAL'"""
        ic = is_clustal_seq_line
        assert ic('abc')
        assert ic('abc  def')
        assert not ic('CLUSTAL')
        assert not ic('CLUSTAL W fsdhicjkjsdk')
        assert not ic('  *   *')
        assert not ic(' abc def')
        assert not ic('MUSCLE (3.41) multiple sequence alignment')

    def test_last_space(self):
        """last_space should split on last whitespace"""
        self.assertEqual(last_space('a\t\t\t  b    c'), ['a b', 'c'])
        self.assertEqual(last_space('xyz'), ['xyz'])
        self.assertEqual(last_space('  a b'), ['a', 'b'])

    def test_delete_trailing_number(self):
        """Should delete the trailing number if present"""
        dtn = delete_trailing_number
        self.assertEqual(dtn('abc'), 'abc')
        self.assertEqual(dtn('a b c'), 'a b c')
        self.assertEqual(dtn('a \t  b  \t  c'), 'a \t  b  \t  c')
        self.assertEqual(dtn('a b 3'), 'a b')
        self.assertEqual(dtn('a b c \t 345'), 'a b c')


class MinimalClustalParserTests(TestCase):

    """Tests of the MinimalClustalParser class"""

    def test_null(self):
        """Should return empty dict and list on null input"""
        result = MinimalClustalParser([])
        self.assertEqual(result, ({}, []))

    def test_minimal(self):
        """Should handle single-line input correctly"""
        result = MinimalClustalParser([MINIMAL])  # expects seq of lines
        self.assertEqual(result, ({'abc': ['ucag']}, ['abc']))

    def test_two(self):
        """Should handle two-sequence input correctly"""
        result = MinimalClustalParser(TWO)
        self.assertEqual(result, ({'abc': ['uuu', 'aaa'], 'def': ['ccc',
                                   'ggg']}, ['abc', 'def']))

    def test_real(self):
        """Should handle real Clustal output"""
        data, labels = MinimalClustalParser(REAL)
        self.assertEqual(labels, ['abc', 'def', 'xyz'])
        self.assertEqual(data, {
            'abc':
            ['GCAUGCAUGCAUGAUCGUACGUCAGCAUGCUAGACUGCAUACGUACGUACGCAUGCAUCA',
             'GUCGAUACGUACGUCAGUCAGUACGUCAGCAUGCAUACGUACGUCGUACGUACGU-CGAC',
             'UGACUAGUCAGCUAGCAUCGAUCAGU'
             ],
            'def':
            ['------------------------------------------------------------',
             '-----------------------------------------CGCGAUGCAUGCAU-CGAU',
             'CGAUCAGUCAGUCGAU----------'
             ],
            'xyz':
            ['------------------------------------------------------------',
             '-------------------------------------CAUGCAUCGUACGUACGCAUGAC',
             'UGCUGCAUCA----------------'
             ]
        })

    def test_bad(self):
        """Should reject bad data if strict"""
        result = MinimalClustalParser(BAD, strict=False)
        self.assertEqual(result, ({}, []))
        # should fail unless we turned strict processing off
        self.assertRaises(RecordError, MinimalClustalParser, BAD)

    def test_space_labels(self):
        """Should tolerate spaces in labels"""
        result = MinimalClustalParser(SPACE_LABELS)
        self.assertEqual(result, ({'abc': ['uca'], 'def ggg': ['ccc']},
                                  ['abc', 'def ggg']))


MINIMAL = 'abc\tucag'
TWO = 'abc\tuuu\ndef\tccc\n\n    ***\n\ndef ggg\nabc\taaa\n'.split('\n')

REAL = """CLUSTAL W (1.82) multiple sequence alignment


abc             GCAUGCAUGCAUGAUCGUACGUCAGCAUGCUAGACUGCAUACGUACGUACGCAUGCAUCA 60
def             ------------------------------------------------------------
xyz             ------------------------------------------------------------


abc             GUCGAUACGUACGUCAGUCAGUACGUCAGCAUGCAUACGUACGUCGUACGUACGU-CGAC 11
def             -----------------------------------------CGCGAUGCAUGCAU-CGAU 18
xyz             -------------------------------------CAUGCAUCGUACGUACGCAUGAC 23
                                                         *    * * * *    **

abc             UGACUAGUCAGCUAGCAUCGAUCAGU 145
def             CGAUCAGUCAGUCGAU---------- 34
xyz             UGCUGCAUCA---------------- 33
                *     ***""".split('\n')

BAD = ['dshfjsdfhdfsj', 'hfsdjksdfhjsdf']

SPACE_LABELS = ['abc uca', 'def ggg ccc']


if __name__ == '__main__':
    main()
