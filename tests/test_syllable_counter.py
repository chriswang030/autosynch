import pytest
from mock import mock, patch
from autosynch.syllable_counter import SyllableCounter

@pytest.fixture
def counter():
    return SyllableCounter()

@patch.object(SyllableCounter, '_load_data', return_value=([],{}))
def test_load_data_on_init(mock):
    SyllableCounter()
    assert mock.called

def test_handles_no_lexicon_data():
    sc = SyllableCounter(sba_lexicon_path=None)
    assert sc.lexicon is None
    assert sc.counter is None

def test_sba(counter):
    assert counter._sba('quagmire') == 2
    assert counter._sba('subpoena') == 3
    assert counter._sba('cooperate') == 4
    assert counter._sba('brulée') is None
    assert counter._sba('footstool') == 2
    assert counter._sba('borscht') == 1

def test_build_lyrics(counter):
    assert counter._build_lyrics('hello\nits me') == [[['hello'], ['its', 'me']]]
    assert counter._build_lyrics('[Chorus]\nhello\nits me') == [[['hello'], ['its', 'me']]]
    assert counter._build_lyrics('[Chorus]\nhello\n[Verse]\nits me') == [[['hello']], [['its', 'me']]]
    assert counter._build_lyrics('[Produced by X]\n[Chorus]\nhello\nits me') == [[['hello'], ['its', 'me']]]
    assert counter._build_lyrics('hello\nhy-phen') == [[['hello'], ['hy', 'phen']]]
    assert counter._build_lyrics('hello\nen-dash') == [[['hello'], ['en', 'dash']]]
    assert counter._build_lyrics('hello\nforward/slash') == [[['hello'], ['forward', 'slash']]]

def test_get_syllable_count_word(counter):
    assert counter.get_syllable_count_word('42') == 3
    assert counter.get_syllable_count_word('4200') == 6
    assert counter.get_syllable_count_word('3.14') == 4
    assert counter.get_syllable_count_word('HELLO') == 2
    assert counter.get_syllable_count_word('don\'t~!@#$%^&*()-=_+`|}{":<>?.,/;"}') == 1
    assert counter.get_syllable_count_word('samantha\'s') == 3

def test_get_syllable_count_lyrics(counter):
    assert counter.get_syllable_count_lyrics('hElLO\nit\'s M####e') == [[[2], [1, 1]]]
