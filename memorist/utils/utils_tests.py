from utils.utils import is_sentence


def test_distinction_word_or_sentence():
    assert is_sentence('word') is False
    assert is_sentence('seal off') is False
    assert is_sentence('i am a boy') is True
    assert is_sentence('오늘은 토요일이야.') is True
