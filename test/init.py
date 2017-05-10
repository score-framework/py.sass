from score.init import init
import os


def init_score(extra=None, *, finalize=True):
    conf = {
        'score.init': {
            'modules': [
                'score.tpl',
                'score.sass',
            ],
        },
        'tpl': {
            'rootdir': os.path.join(os.path.dirname(__file__), 'templates')
        }
    }
    if extra:
        for key in extra:
            conf[key] = extra[key]
    return init(conf, finalize=finalize)


def test_empty():
    score = init_score()
    assert score.tpl.render('empty.sass') == ''


def test_almost_empty():
    score = init_score()
    assert score.tpl.render('almost-empty.scss') == ''
