# -*- coding: utf-8 -*-
import unittest
import doctest


def setUp(test):
    pass


def tearDown(test):
    pass


def load_tests(loader, tests, ignore):
    list_of_doctests = []
    list_of_doctests.append('project.models')

    suite = unittest.TestSuite()
    for t in list_of_doctests:
        tests.addTest(doctest.DocTestSuite(
            __import__(t, globals(), locals(), fromlist=["*"]),
            setUp=setUp, tearDown=tearDown,
            optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
        ))

    return tests

