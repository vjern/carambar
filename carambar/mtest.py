import re
import textwrap
import traceback
from contextlib import contextmanager


"""
Some things can't be tested without a human being there.
A set of tools to run tests with an Oracle (user).

Merely resorts to prompt the user for a test,
describing the test's purpose,
running the behavior,
then asking the user to confirm whether the test has completed succesfully.
"""


def get_default_answer(ans: str) -> str:
    for a in ans:
        if a == a.upper():
            return a


def parse_action(action: str) -> (str, list):

    single_token_rgx = r'!([a-zA-Z0-9_-]+)'
    multi_token_rgx = r'!\{(.*?)\}'

    keywords = []

    keywords.extend((r.group(1), r.span()[0]) for r in re.finditer(single_token_rgx, action))
    keywords.extend((r.group(1), r.span()[0]) for r in re.finditer(multi_token_rgx, action))
    keywords = sorted(keywords, key = lambda pair: pair[1])
    if keywords:
        keywords, _ = zip(*keywords)

    text = action
    text = re.sub(single_token_rgx, r'\1', text)
    text = re.sub(multi_token_rgx, r'\1', text)

    text = textwrap.wrap(text, width=50)
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
    return user_ans

def ask(msg: str):
    assert prompt(msg, 'Yn') == 'Y'


@contextmanager
def Test(action: str, question: str = ''):
    color = '\033[38;2;250;180;40m'
    action, keywords = parse_action(action)
    desc = color + '{ This program will now %s. }\033[m' % action
    if not question:
        question = 'Did the program %s ?' % action
    question = color + '{ %s }\033[m' % question
    name = ' '.join(keywords)
    if not name:
        name = action[:30]
        if len(action) > 30:
            name = name[:29] + '/'
    print('\033[95m{ Oracle Test }\033[m')
    prompt(desc)
    yield
    try:
        ask(question)
    except AssertionError:
        print('\033[91m%s\033[m' % '[ Test { %s } failed. ]' % (name))
        raise
    print('\033[92m%s\033[m' % '[ Test { %s } was a success. ]' % (name))



def test_Test():
    with Test('!{print %s}' % repr('a')):
        print('a')


def run_tests(env):
    # print(env['__file__'], end=' ')
    results = []
    for key, value in env.items():
        if not key.startswith('test_'):
            continue
        try:
            value()
            results += [(key, '.', None)]
        except Exception:
            results += [(key, 'F', traceback.format_exc())]
    print(env['__file__'], '{', len([r for r in results if r[1] == '.']), '/', len(results), '}')
    for name, result, message in results:
        print('- {:30} {}'.format(name, result))
        if message is not None:
            print('\033[97m' + '    ' + message.replace('\n', '\n    ') + '\033[m')
        


if __name__ == "__main__":
    test_Test()