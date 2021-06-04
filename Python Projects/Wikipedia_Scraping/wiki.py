import re

import requests

import pandas as pd
from bs4 import BeautifulSoup


class WikiScraper:
    """A class used for scraping Wikipedia page data. Organizes natural language on page and hyperlinks."""
    def __init__(self, subject=None, link=None, printing=False):
        self.hyperlinks = []
        self.para_list = []
        self.section_headers = []
        if subject is not None:
            self.HTML_LINK = _make_wiki_link(subject)
            self._get_wiki_data(self.HTML_LINK, printing=printing)
            self._get_wiki_df()
        elif link is not None:
            self.HTML_LINK = link
            self._get_wiki_data(self.HTML_LINK, printing=printing)
            self._get_wiki_df()
        else:
            print("Please provide a 'subject' or 'link' argument.")

    def _get_wiki_data(self, HTML_LINK, printing=False):
        """Takes in a Wikipedia link and returns the natural language paragraphs,
        section titles, and hyperlinks found in the document.
        """
        if self.section_headers == []:
            soup = _get_soup_doc(HTML_LINK)
            headers = _get_headers(soup)
            header_strings = [str(h) for h in headers]
            h_indices = _get_indices(soup, header_strings)

            self.subject = _get_title(soup)
            printer_count = 5  # counter in the for loop below
            if printing:
                print("PAGE TITLE:", self.subject)
                printer_count = 0

            for i, head in enumerate(headers):
                self.section_headers.append(head.text)
                paragraphs = _get_raw_paragraphs(soup, h_indices, i)
                hrefs = [_get_hyperlink(p) for p in paragraphs]
                paras = [_remove_HTML(p) for p in paragraphs]
                self.hyperlinks.append(combine(hrefs))
                self.para_list.append(paras)
                if printer_count < 3:  # To limit printing
                    printer_count = printer_count + 1
                    print("\n", "#" * 100, "\n\tSECTION:", head.text)
                    for p in paras:
                        print("\n", _show_some_text(p))
                    print("\nLINKS:", _show_some_text(str(combine(hrefs))))
        else:
            print("Wiki data already scraped.")

    def _get_wiki_df(self):
        """Organizes Wikipedia page data into a Pandas dataframe."""
        wiki_df = pd.DataFrame(
            {
                "section": self.section_headers,
                "hyperlinks": self.hyperlinks,
                "paragraphs": self.para_list,
            }
        )
        wiki_df["words"] = wiki_df.apply(
            lambda row: _get_words_from_paragraphs(row.paragraphs), axis=1
        )
        wiki_df = _add_count_feature(wiki_df, "hyperlinks")
        wiki_df = _add_count_feature(wiki_df, "paragraphs")
        wiki_df = _add_count_feature(wiki_df, "words")
        wiki_df = wiki_df.set_index("section")
        self.df = wiki_df[~(wiki_df.paragraphs_count == 0)]


def _make_wiki_link(subject):
    link = "https://en.wikipedia.org/wiki/" + subject
    return link


def _get_soup_doc(HTML_LINK, parser="html.parser"):
    """Takes in an html link and returns a BeautifulSoup document."""
    response = requests.get(HTML_LINK)
    soup_doc = BeautifulSoup(response.content, "html.parser")
    return soup_doc


def _get_title(soup_doc):
    """Returns the title of the web page."""
    title = soup_doc.find(id="firstHeading").text
    return title


def _get_headers(soup):
    """Returns the header of each section in a Wikipedia page."""
    headers = soup.find_all("span", attrs="mw-headline")
    return headers


def _remove_footnotes(text):
    """Drop footnote superscripts in brackets"""
    text = re.sub(r"\[.*?\]+", "", text)
    return text


def _get_indices(soup, string_elements):
    """Returns the a list of the starting index for each element in a list of strings."""
    soup_string = str(soup)
    indices = [soup_string.index(string) for string in string_elements]
    return indices


def _get_index(text, element):
    """Attempts to get the index of an element. Returns None if not present"""
    try:
        idx = text.index(element)
        return idx
    except:
        return None


def combine(lists):
    """Combines a list of lists into one list to return."""
    combo = []
    for list_ in lists:
        combo.extend(list_)
    return combo


def _collect_pattern_pairs(text, start_char, end_char):
    """Returns a list of all text between sets of start_char and end_char characters."""
    collection = []
    while _get_index(text, start_char) is not None:
        start = _get_index(text, start_char)
        end = _get_index(text[start:], end_char) + start  # make sure end is after start
        collection.append(text[start : end + len(end_char)])
        text = text[end + len(end_char) :]
    return collection


def _get_raw_paragraphs(soup, h_indices, i):
    """Returns unprocessed HTML paragraphs."""
    soup_string = str(soup)
    try:
        raw_text_i = soup_string[h_indices[i] : h_indices[i + 1]]
    except:
        raw_text_i = soup_string[h_indices[i] :]
    paragraphs = _collect_pattern_pairs(raw_text_i, "<p>", "</p>")
    return paragraphs


def _get_paragraphs(soup, h_indices, i):
    """Returns the text paragraphs associated with the section header specified by an index."""
    paragraphs = _get_raw_paragraphs(soup, h_indices, i)
    clean_paragraphs = [_remove_HTML(p) for p in paragraphs]
    return clean_paragraphs


def _remove_pattern_pair(text, start_char, end_char):
    """Removes all text between the start_char and end_char and returns remaining text."""
    while _get_index(text, start_char) is not None:
        start = _get_index(text, start_char)
        end = _get_index(text[start:], end_char) + start  # make sure end is after start
        text = text[:start] + text[end + len(end_char) :]
    return text


def _remove_substrings(text, substring_list):
    """Removes all occurences of all substrings in a list from a text string. Returns new string."""
    for pattern in substring_list:
        text = re.sub(pattern, "", text)
    return text


def _remove_HTML(text):
    """Removes the HTML elements from a substring of an HTML document and returns resulting string."""
    to_remove = ["</a>", "</sup>", "<p>", "</p>"]
    text = _remove_substrings(text, to_remove)
    plain_text = _remove_pattern_pair(text, "<", ">")
    plain_text = _remove_footnotes(plain_text)
    return plain_text


def _clean_wiki_links(hlinks):
    """Completes hyperlinks to other Wikipedia pages."""
    for i, link in enumerate(hlinks):
        if "/wiki/" in link:
            end = link.index('"')
            hlinks[i] = re.sub("/wiki/", "https://en.wikipedia.org/wiki/", link[:end])
    return hlinks


def _remove_internal_links(hlinks):
    """Removes links that reference different parts of the Wikipedia page."""
    internal_links = []
    for link in hlinks:
        if "#" == link[0]:
            hlinks.remove(link)
    return hlinks


def _clean_cite_notes(hlinks):
    """Removes references to links cited at the bottom of the Wikipedia page."""
    cite_notes = []
    for i, link in enumerate(hlinks):
        if "#cite_note-" in link:
            cite_notes.append(hlinks[i])
    for c in cite_notes:
        hlinks.remove(c)
    return hlinks


def _clean_hyperlinks(html_hyperlinks):
    """Removes the HTML markup around hyperlinks and returns a list of hyperlinks"""
    to_remove = ['<a href="', '">']
    hlinks = [_remove_substrings(link, to_remove) for link in html_hyperlinks]
    hlinks = _clean_wiki_links(hlinks)
    hlinks = _clean_cite_notes(hlinks)
    hlinks = _remove_internal_links(hlinks)
    return hlinks


def _get_hyperlink(text):
    """Returns a list of all hyperlinks included in a subsection of an HTML document."""
    html_hyperlinks = _collect_pattern_pairs(text, "<a href=", ">")
    hyperlinks = _clean_hyperlinks(html_hyperlinks)
    return hyperlinks


def _show_some_text(text):
    """Returns first 100 characters in string."""
    return text[:80] + "..."


def _join_strings(string_list, join_char=" \n "):
    """Joins a list of strings into one string."""
    return join_char.join(string_list)


def _get_words_from_paragraphs(p_list):
    """Returns a list of words from a list of paragraphs."""
    paragraph = _join_strings(p_list)
    return paragraph.split(" ")


def _add_count_feature(df, feature):
    """Returns df with new feature that is the length of the list of a different feature."""
    df[feature + "_count"] = df.apply(lambda row: len(row[feature]), axis=1)
    return df


def _remove_punctuation(words):
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


def _get_top_n_strings(str_list, n=3):
    """Finds most popular n strings in a string list. Returns a list of tuples (word, count)."""
    word_df = pd.DataFrame({"words": str_list})
    word_vc = word_df.value_counts()
    top_strings = [(word_vc.index[i][0], word_vc[i]) for i in range(n)]
    return top_strings


def _remove_stop_words(doc, lemmas=False):
    """Removes "stop words" (common words like "is", "but", "and") from list of words."""
    if lemmas:
        # Lemmas are the base form of a word. Ex: the lemma of swimming is swim.
        interesting_words = [token.lemma_ for token in doc if not token.is_stop]
    else:
        interesting_words = [token.text for token in doc if not token.is_stop]
    return interesting_words


def _find_popular_words(nlp, words_list, n=3, lemmas=False):
    """Finds the most popular words that aren't stop words in a list of words."""
    text = _join_strings(words_list, join_char=" ")
    doc = nlp(text.lower())  # make lowercase
    nice_words = _remove_stop_words(doc, lemmas=lemmas)
    actual_nice_words = _remove_punctuation(nice_words)
    popular_words = _get_top_n_strings(actual_nice_words, n=n)
    return popular_words


def find_top_words(nlp, df, n=1, lemmas=False):
    """Adds new feature listing tuples of "n" top words."""
    top_words = df.apply(
        lambda row: _find_popular_words(nlp, row.words, n=n, lemmas=lemmas), axis=1
    )
    return top_words
