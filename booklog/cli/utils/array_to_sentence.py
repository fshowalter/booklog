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
            return "{0}{1}{2}".format(words[0], two_words_connector, words[1])
        case _:
            return "{0}{1}{2}".format(
                words_connector.join(words[:-1]), last_word_connector, words[-1]
            )
