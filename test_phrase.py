def test_phrase_less_15_symbols():
    phrase = input('Set a phrase, less than 15 symbols: ')
    assert len(phrase) <= 15, f'Your phrase is not less than 15 symbols, it is {len(phrase)} symbols'
