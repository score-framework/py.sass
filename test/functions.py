from .init import init_score
import unittest.mock
import re


def test_function_call():
    score = init_score(finalize=False)
    loader = unittest.mock.Mock()
    loader.load.return_value = (False, 'body { color: foo();}')
    loader.is_valid.return_value = True
    score.tpl.filetypes['text/css'].add_global('foo', lambda: 'white')
    score.tpl.loaders['scss'].append(loader)
    score._finalize()
    output = score.tpl.render('test.scss')
    assert re.sub(r'\s+', '', output) == 'body{color:white}'


def test_invalid_function():
    score = init_score(finalize=False)
    loader = unittest.mock.Mock()
    loader.load.return_value = (False, 'body { color: bar();}')
    loader.is_valid.return_value = True
    score.tpl.filetypes['text/css'].add_global('foo', lambda: 'white')
    score.tpl.loaders['scss'].append(loader)
    score._finalize()
    output = score.tpl.render('test.scss')
    assert re.sub(r'\s+', '', output) == 'body{color:bar()}'
