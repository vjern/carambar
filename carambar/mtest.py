import re
import textwrap
from contextlib import contextmanager


"""
A set of tools to run tests with an observer.
"""


def get_default_answer(ans: str) -> str:
    for a in ans:
        if a == a.upper():
            return a


def parse_action(action: str):

    single_token_rgx = r'!([a-zA-Z0-9_-]+)'
    multi_token_rgx = r'!\{(.*?)\}'

    keywords = []

    keywords.extend((r.group(1), r.span()[0]) for r in re.finditer(single_token_rgx, action))
    keywords.extend((r.group(1), r.span()[0]) for r in re.finditer(multi_token_rgx, action))
    keywords = sorted(keywords, key = lambda pair: pair[1])
    keywords, _ = zip(*keywords)

    text = action
    text = re.sub(single_token_rgx, r'\1', text)
    text = re.sub(multi_token_rgx, r'\1', text)

    text = textwrap.wrap(text, width=50)
    print(text)
    text = '\n  '.join(text)

    return text, keywords


def prompt(msg: str, ans: str = '') -> str:
    user_msg = ' '.join((msg, '(%s)' % ''.join(ans) if bool(ans) else '(Press Enter to continue)')) + ' '
    user_ans = input(user_msg).strip()
    if not ans:
        return
    default_answer = get_default_answer(ans)
    if default_answer is not None and not user_ans:
        return default_answer
    while len(user_ans) != 1 or user_ans not in ans:
        user_ans = input(user_msg)
        if default_answer is not None and not user_ans:
            return default_answer


def ask(msg: str):
    assert prompt(msg, 'Yn') == 'Y'


@contextmanager
def Test(action: str):
    action, keywords = parse_action(action)
    desc = '\033[38;5;207m{ This program will now %s. }\033[m' % action
    question = '\033[38;5;207m{ Did the program %s ? }\033[m' % action
    name = ' : '.join(keywords)
    if not name:
        name = action[:30]
        if len(action) > 30:
            name = name[:29] + '/'
    prompt(desc)
    yield
    try:
        ask(question)
    except AssertionError:
        print('\033[91m%s\033[m' % '[ Test \033[95m{ %s }\033[91m failed. ]' % (name))
        raise
    print('\033[92m%s\033[m' % '[ Test \033[95m{ %s }\033[92m was a success. ]' % (name))


def test_Test():
    with Test('!{print %s}' % repr('a')):
        print('a')

if __name__ == "__main__":
    test_Test()