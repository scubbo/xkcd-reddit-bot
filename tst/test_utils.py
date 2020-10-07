import src.utils
from collections import namedtuple

FakeComment = namedtuple('FakeComment', ['body'])


def test_fails():
    for test_case in [
        ('', None),
        ('a', None),
        ('xkcd.com', None),
        ('xkcd.com/must-be-numeric', None),
        ('xkcd.com/123', '123'),
        ('www.xkcd.com/234', '234'),
        ('http://www.xkcd.com/345', '345'),
        ('https://www.xkcd.com/456', '456')
    ]:
        output = src.utils.xkcd_linked_in_comment(_build_comment_with_body(test_case[0]))
        assert output == test_case[1], f'Failed on {test_case}, actual output {output}'


def _build_comment_with_body(body: str):
    return FakeComment(body=body)
