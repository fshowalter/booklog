def array_to_sentence(words: list[str]) -> str:
    words_connector = ", "
    two_words_connector = " and "
    last_word_connector = ", and "

    match len(words):
        case 0:
            return ""
        case 1:
            return words[0]
        case 2:
            return f"{words[0]}{two_words_connector}{words[1]}"
        case _:
            all_words_but_last = words[:-1]
            last_word = words[-1]
            return f"{words_connector.join(all_words_but_last)}{last_word_connector}{last_word}"
