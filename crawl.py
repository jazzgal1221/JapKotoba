# coding: utf-8
#!/usr/bin/env python
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import random

from selenium.webdriver.common.proxy import *

#myProxy = "localhost:1080"

#proxy = Proxy({
#    'proxyType': ProxyType.MANUAL,
#    'socksProxy': myProxy,
#    'noProxy': '' # set this value as desired
#    })

#driver = webdriver.Firefox(proxy=proxy)
class Word(object):
    """Represent a word. """
    japanese = ""
    kana = ""
    en = ""
    vi = ""
    go = ""
    combo = ""
    raw_str = None

    def __repr__(self):
        return "< %r %r %r %r %r>" % (self.japanese, self.kana, self.vi,
                                   self.en, self.combo)

def get_driver(url, use_proxy=False):
    """Return driver after loading url."""
    if use_proxy:
        myProxy = "localhost:1080"

        proxy = Proxy({
            'proxyType': ProxyType.MANUAL,
            'socksProxy': myProxy,
            'noProxy': '' # set this value as desired
            })

        driver = webdriver.Firefox(proxy=proxy)
    else:
        driver = webdriver.Firefox()
    driver.get(url)

    return driver


def list_words(file_name=None):
    """Return list of wrds to be looked up."""
    data = []
    if not file_name:
        file_name = "inputs.txt"
    with open(file_name, "rb") as f:
        raw_data = f.readlines()
        data = []
        for d in raw_data:
            if d:
                data.extend(d.split(", "))


    words = []
    bracket_open = unicode_chars('「')
    bracket_close = unicode_chars('」')
    space = unicode_chars('～')
    dot = unicode_chars('…')
    for i in data:
        # Process input word
        word = Word()
        word.raw_str = i
        i = unicode_chars(i)
        if bracket_open in i and bracket_close in i:
            # Make combination word
            combine_part = i[i.index(bracket_open)+1: i.index(bracket_close)]
            jap_word = i[:i.index(bracket_open)].replace(space, '')
            jap_word = jap_word.replace(dot, '')
            if space in combine_part:
                # Replace ~ sign with actual word
                word.combo = combine_part.replace(space, jap_word)
            else:
                # Add word + combine_part
                word.combo = jap_word + combine_part
        else:
            jap_word = i.replace(space, '')
            jap_word = jap_word.replace(dot, '')

        word.japanese = jap_word
        words.append(word)

    return words


def unicode_chars(chars):
    return unicode(chars, "utf8")


def search_browser(word, driver):
    """Input word to search field & click button"""
    while True:
        try:
            input = driver.find_element_by_id("search_text")
            input.send_keys(word)
            input.send_keys(Keys.RETURN)
            return
        except Exception as ex:
            driver.refresh()
            time.sleep(5)



def parse_page(driver):
    """Parse page content and return tuple of word, kana, meanings"""
    # Kana
    while True:
        try:
            reading_sect = driver.find_element_by_class_name("my-default")
            break
        except Exception as ex:
            time.sleep(2)
    reading_text = reading_sect.text
    open_brack=unicode_chars("【")
    close_brack=unicode_chars("】")
    if open_brack in reading_text and close_brack in reading_text:
        kana = reading_text[reading_text.index(open_brack)+1:reading_text.index(close_brack)]
    else:
        kana = reading_text

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
        if vi_origin in text and not vi_meaning:
            vi_meaning = first_line(text[:text.index(vi_origin)])
        elif en_origin in text and not en_meaning:
            en_meaning = first_line(text[:text.index(en_origin)])
        elif google_origin in text and not go_meaning:
            go_meaning = first_line(text[:text.index(google_origin)])

    return kana, vi_meaning, en_meaning, go_meaning

def first_line(line):
    """Return first line from paragraph."""
    if "\n" in line:
        return line[:line.index("\n")]
    return line

def search_and_parse(driver, word):
    t = random.randint(1, 4)
    print "Sleep", t
    time.sleep(t)
    search_browser(word, driver)
    kana, vi, en, go = parse_page(driver)
    return word, kana, vi, en, go


def main(file_name=None):
    words = list_words(file_name)
    url="http://www.tudienabc.com/tra-nghia/nhat-anh-viet"
    driver = get_driver(url)
    results = []
    for w in words:
        w.japanese, w.kana, w.vi, w.en, w.go =                 search_and_parse(driver, w.japanese)
        results.append(w)
        if w.combo:
            new_word = Word()
            new_word.japanese, new_word.kana, new_word.vi, new_word.en, new_word.go =                     search_and_parse(driver, w.combo)
            results.append(new_word)

    return results

def clean_results(results):
    for w in results:
        if not w.kana:
            w = "null"
        if not w.vi:
            w.vi = "null"
        if not w.en:
            w.en = "null"
        if not w.go:
            w.go = "null"


def crawl_file(number):
    file_name = "%d.txt" % number
    results = main(file_name)
    clean_results(results)

    with open("%d_results.txt" % number, "wb") as f:
        for w in results:
            f.write('"%s", "%s", "%s", "%s", "%s"' % (w.japanese.encode("utf8"), w.kana.encode("utf8"), w.vi.encode("utf8"), w.en.encode("utf8"), w.go.encode("utf8")))
            f.write("\n")


