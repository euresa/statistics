import re
import requests

import pandas as pd  # type: ignore
from bs4 import BeautifulSoup  # type: ignore

class WikiScraper:
    """A class used for scraping Wikipedia page data. Organizes natural language on
    a Wikipedia page and creates a list of the hyperlinks present on the page."""

    def __init__(self, subject: str="", link: str="", printing: bool=False) -> None:
        self.hyperlinks: list = []
        self.para_list: list = []
        self.section_headers: list = []
        if subject != "":
            self.HTML_LINK: str = _make_wiki_link(subject)
            self._get_wiki_data(self.HTML_LINK, printing=printing)
            self._get_wiki_df()
        elif link != "":
            self.HTML_LINK = link
            self._get_wiki_data(self.HTML_LINK, printing=printing)
            self._get_wiki_df()
        else:
            print("Please provide a 'subject' or 'link' argument.")

    def _get_wiki_data(self, HTML_LINK: str, printing: bool=False) -> None:
        """Takes in a Wikipedia link and returns the natural language paragraphs,
        section titles, and hyperlinks found in the document.
        """
        if self.section_headers == []:
            soup: BeautifulSoup = _get_soup_doc(HTML_LINK)
            headers: list = _get_headers(soup)
            header_strings = [str(h) for h in headers]
            h_indices: list = _get_indices(soup, header_strings)

            self.subject: str = _get_title(soup)
            printer_count = 5  # counter in the for loop below
            if printing:
                print("PAGE TITLE:", self.subject)
                printer_count = 0

            for i, head in enumerate(headers):
                self.section_headers.append(head.text)
                paragraphs: list = _get_raw_paragraphs(soup, h_indices, i)
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


def _make_wiki_link(subject: str) -> str:
    """Takes in a string containing a subject (e.g. Python, Cats, Russia, etc.) and
    returns the related Wikipedia page link to the subject.
    
        example:
        >>> _make_wiki_link('Statistics')
        https://en.wikipedia.org/wiki/Statistics
    """
    link = "https://en.wikipedia.org/wiki/" + subject
    return link


def _get_soup_doc(HTML_LINK: str, parser: str="html.parser") -> BeautifulSoup:
    """Takes in an html link and returns a BeautifulSoup document."""
    response = requests.get(HTML_LINK)
    soup_doc = BeautifulSoup(response.content, "html.parser")
    return soup_doc


def _get_title(soup_doc: BeautifulSoup) -> str:
    """Returns the title of the web page."""
    title = soup_doc.find(id="firstHeading").text
    return title


def _get_headers(soup: BeautifulSoup) -> list:
    """Returns the header of each section in a Wikipedia page."""
    headers = soup.find_all("span", attrs="mw-headline")
    return headers


def _remove_footnotes(text: str) -> str:
    """Drop footnote superscripts in brackets"""
    text = re.sub(r"\[.*?\]+", "", text)
    return text


def _get_indices(soup: BeautifulSoup, string_elements: list) -> list:
    """Returns the a list of the starting index for each element in a list of strings."""
    soup_string = str(soup)
    indices = [soup_string.index(string) for string in string_elements]
    return indices


def _get_index(text: str, element: str) -> int:
    """Attempts to get the index of an element. Returns -1 if not present

        example:
            >>> _get_index("hello world", "w")
            6
            >>> _get_index("hello world", "z")
            -1
    """
    try:
        idx = text.index(element)
        return idx
    except:
        return -1


def combine(lists):
    """Combines a list of lists into one list to return.

        example:
        >>>combine([[1, 2, 3], [4, 5, 6], [7], [8, 9]])
        [1, 2, 3, 4, 5, 6, 7, 8, 9]
    """
    combo = []
    for list_ in lists:
        combo.extend(list_)
    return combo


def _collect_pattern_pairs(text: str, start_char: str, end_char: str) -> list:
    """Returns a list of all text between sets of start_char and end_char characters."""
    collection = []
    while _get_index(text, start_char) != -1:
        start: int = _get_index(text, start_char)
        end: int = _get_index(text[start:], end_char) + start  # make sure end is after start
        collection.append(text[start : end + len(end_char)])
        text = text[end + len(end_char) :]
    return collection


def _get_raw_paragraphs(soup: BeautifulSoup, h_indices: list, i: int) -> list:
    """Returns unprocessed HTML paragraphs."""
    soup_string = str(soup)
    try:
        raw_text_i = soup_string[h_indices[i] : h_indices[i + 1]]
    except:
        raw_text_i = soup_string[h_indices[i] :]
    paragraphs: list = _collect_pattern_pairs(raw_text_i, "<p>", "</p>")
    return paragraphs


def _get_paragraphs(soup: BeautifulSoup, h_indices: list, i: int) -> list:
    """Returns the text paragraphs associated with the section header specified by an index."""
    paragraphs: list = _get_raw_paragraphs(soup, h_indices, i)
    clean_paragraphs = [_remove_HTML(p) for p in paragraphs]
    return clean_paragraphs


def _remove_pattern_pair(text: str, start_char: str, end_char: str) -> str:
    """Removes all text between the start_char and end_char and returns remaining text."""
    while _get_index(text, start_char) != -1:
        start: int = _get_index(text, start_char)
        end: int = _get_index(text[start:], end_char) + start  # make sure end is after start
        text = text[:start] + text[end + len(end_char) :]
    return text


def _remove_substrings(text: str, substring_list: list) -> str:
    """Removes all occurences of all substrings in a list from a text string. Returns new string."""
    for pattern in substring_list:
        text = re.sub(pattern, "", text)
    return text


def _remove_HTML(text: str) -> str:
    """Removes the HTML elements from a substring of an HTML document and returns resulting string."""
    to_remove = ["</a>", "</sup>", "<p>", "</p>"]
    text = _remove_substrings(text, to_remove)
    plain_text: str = _remove_pattern_pair(text, "<", ">")
    plain_text = _remove_footnotes(plain_text)
    return plain_text


def _clean_wiki_links(hlinks: list) -> list:
    """Completes hyperlinks to other Wikipedia pages."""
    for i, link in enumerate(hlinks):
        if "/wiki/" in link:
            end = link.index('"')
            hlinks[i] = re.sub("/wiki/", "https://en.wikipedia.org/wiki/", link[:end])
    return hlinks


def _remove_internal_links(hlinks: list) -> list:
    """Removes links that reference different parts of the Wikipedia page."""
    for link in hlinks:
        if "#" == link[0]:
            hlinks.remove(link)
    return hlinks


def _clean_cite_notes(hlinks: list) -> list:
    """Removes references to links cited at the bottom of the Wikipedia page."""
    cite_notes = []
    for i, link in enumerate(hlinks):
        if "#cite_note-" in link:
            cite_notes.append(hlinks[i])
    for c in cite_notes:
        hlinks.remove(c)
    return hlinks


def _clean_hyperlinks(html_hyperlinks: list) -> list:
    """Removes the HTML markup around hyperlinks and returns a list of hyperlinks"""
    to_remove = ['<a href="', '">']
    hlinks = [_remove_substrings(link, to_remove) for link in html_hyperlinks]
    hlinks = _clean_wiki_links(hlinks)
    hlinks = _clean_cite_notes(hlinks)
    hlinks = _remove_internal_links(hlinks)
    return hlinks


def _get_hyperlink(text: str) -> list:
    """Returns a list of all hyperlinks included in a subsection of an HTML document."""
    html_hyperlinks: list = _collect_pattern_pairs(text, "<a href=", ">")
    hyperlinks: list = _clean_hyperlinks(html_hyperlinks)
    return hyperlinks


def _show_some_text(text: str) -> str:
    """Returns first 100 characters in string."""
    return text[:80] + "..."


def _get_words_from_paragraphs(p_list: list) -> list:
    """Returns a list of words from a list of paragraphs."""
    paragraph: str = " \n ".join(p_list)  # paragraphs are separated by ' \n '
    return paragraph.split(" ")


def _add_count_feature(df: pd.DataFrame, feature: str) -> pd.DataFrame:
    """Returns df with new feature that is the length of the list of a different feature."""
    df[feature + "_count"] = df.apply(lambda row: len(row[feature]), axis=1)
    return df