"""
Various functions for performing natural language processing with
spaCy objects.
"""
import pandas  # type: ignore


def _remove_punctuation(words: list) -> list:
    """Removes punctuation and special characters."""
    punc_list = [
        ".",
        ",",
        ")",
        "(",
        "/",
        "]",
        "[",
        "\n",
        " ",
        ";",
        ":",
        '"',
        "'",
        "\n \n ",
        "-",
    ]
    no_punc = [w for w in words if w not in punc_list]
    return no_punc


def _get_top_n_strings(str_list: list, n: int = 3) -> list:
    """Finds most popular n strings in a string list. Returns a list of tuples (word, count)."""
    word_df: pandas.DataFrame = pandas.DataFrame({"words": str_list})
    word_vc = word_df.value_counts()
    top_strings = [(word_vc.index[i][0], word_vc[i]) for i in range(n)]
    return top_strings


def _remove_stop_words(doc, lemmas: bool = False) -> list:
    """Removes "stop words" (common words like "is", "but", "and") from list of words."""
    if lemmas:
        # Lemmas are the base form of a word. Ex: the lemma of swimming is swim.
        interesting_words = [token.lemma_ for token in doc if not token.is_stop]
    else:
        interesting_words = [token.text for token in doc if not token.is_stop]
    return interesting_words


def find_popular_words(nlp, words_list: list, n: int = 3, lemmas: bool = False) -> list:
    """Finds the most popular words that aren't stop words in a list of words."""
    text = " ".join(words_list)
    doc = nlp(text.lower())
    nice_words: list = _remove_stop_words(doc, lemmas=lemmas)
    actual_nice_words: list = _remove_punctuation(nice_words)
    popular_words: list = _get_top_n_strings(actual_nice_words, n=n)
    return popular_words


def find_top_words(nlp, df, n: int = 1, lemmas: bool = False) -> pandas.Series:
    """Returns a pandas.Series object of tuples comprised of the the top 'n' words
    from each row of a pandas.DataFrame already containing a 'words' feature.
    """
    top_words: pandas.Series = df.apply(
        lambda row: find_popular_words(nlp, row.words, n=n, lemmas=lemmas), axis=1
    )
    return top_words
