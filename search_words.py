# coding: utf-8
#!/usr/bin/env python
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def get_driver(url):
    """Return driver after loading url."""
    url="http://www.tudienabc.com/tra-nghia/nhat-anh-viet"
    driver.get(url)
    driver = webdriver.Firefox()
    driver.get(url)

    return driver


def unicode_chars(chars):
    return unicode(chars, "utf8")


def search_browser(word, driver):
    """Input word to search field & click button"""
    input=driver.find_element_by_id("translate_score")
    input.send_keys(word)
    input.send_keys(Keys.RETURN)


def parse_parge(driver):
    """Parse page content and return tuple of word, kana, meanings"""
    # Kana
    reading_sect = driver.find_element_by_class_name("my-default")
    reading_text = reading_sect.text
    open_brack=unicode_chars("【")
    close_brack=unicode_chars("】")
    if open_brack in reading_text and close_brack in reading_text:
        reading_kana = reading_text[reading_text.index(open_brack)+1:reading_text.index(close_brack)]
    else:
        reading_kana = reading_text

    # Meanings
    vi_origin=unicode_chars("Nhật-Việt tổng hợp")
    en_origin=unicode_chars("Nhật-Anh tổng hợp")
    google_origin=unicode_chars("Google Translate")

    translation_sect = driver.find_element_by_id("translate_score")
    rows = translation_sect.find_elements_by_tag_name("tr")
    vi_meaning = None
    en_meaning = None
    go_meaning = None
    for row in rows:
        text = row.text
        if vi_origin in txt and not vi_meaning:
            vi_meaning = first_line(text[:text.index(vi_origin)])
        elif en_origin in txt and not en_meaning:
            en_meaning = first_line(text[:text.index(en_origin)])
        elif en_origin in txt and not go_meaning:
            go_meaning = first_line(text[:text.index(google_origin)])

    return (kana, vi_meaning, en_meaning, go_meaning)

def first_line(line):
    """Return first line from paragraph."""
    if "\n" in line:
        return line[:line.index("\n")]
    return line


def main():
    words = list_words()
