from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import random


def main():
    user = input("Number of words to revise? (1-200 limits) \n")
    word_count = int(user) if user.isnumeric() and 200 > int(user) > 0 else None

    min_length = 0
    max_length = 100
    allow_basic = False
    to_English = True
    example_sentence = True
    note_correct = True
    print_source = False
    _dict = {}
    sentence_dict = {}
    source_dict = {}

    while user.lower() not in ("start", "s") or not word_count:
        if word_count:
            user = input("'[S]tart' to begin the program, '[A]ll' for list of all settings.\n")
            if user.lower() in ('all', 'a'):
                print("""
'[B]asic' to allow/disallow super common words like 'the'. (default disallowed)
'[D]irection' for translation direction. (default: Spanish to English)
'[E]xample for an example sentence using the word. (default enabled)
'[N]ote to note correctly answered words & prevent their repetition. (default enabled)
'[P]rint' to print the Wiki page along with the word. (default disabled)
'[R]eset' to reset correct.txt.
'>' to set a minimum word length. (default none, max 15)
'<' to set a maximum word length. (default 100, min 3)
                        """)
            if user.lower() in ('basic', 'b'):
                allow_basic = not allow_basic
                print(f"Allow basic words: {'on' if allow_basic else 'off'}.\n")
            if user.lower() in ('direction', 'd'):
                to_English = not to_English
                print(f"Translation direction: {'to English' if to_English else 'to Spanish'}.\n")
            if user.lower() in ('example', 'e'):
                example_sentence = not example_sentence
                print(f"Example sentence: {'on' if example_sentence else 'off'}.\n")
            if user.lower() in ('note', 'n'):
                note_correct = not note_correct
                print(f"Note correctly answered: {'on' if note_correct else 'off'}.\n")
            if user.lower() in ('print', 'p'):
                print_source = not print_source
                print(f"Print wiki source: {'on' if print_source else 'off'}.\n")
            if user.lower() in ('reset', 'r'):
                open('correct.txt', 'w').close()
                print("File reset.\n")
            if user == '>':
                user = input("Set minimum word length:\n")
                if user.isnumeric() and max_length > min_length and 15 >= int(user) >= 0:
                    min_length = int(user)
                    print(f"Set to {min_length}.\n")
                else:
                    min_length = 0
                    print("Invalid number, returned to default.\n")
            if user == '<':
                user = input("Set maximum word length:\n")
                if user.isnumeric() and max_length > min_length and 100 >= int(user) >= 3:
                    max_length = int(user)
                    print(f"Set to {max_length}.\n")
                else:
                    max_length = 100
                    print("Invalid number, returned to default.\n")
        else:
            user = input("Invalid number. Try again.\n")
            word_count = int(user) if user.isnumeric() and 200 > int(user) > 0 else None

    if allow_basic:
        basic_words = []
    else:
        with open('basic.txt', 'r') as f:
            basic_words = f.read().splitlines()
    if note_correct:
        with open('correct.txt', 'r') as f:
            revised = f.read().splitlines()[1:]
    else:
        revised = []

    PATH = "C:\Program Files (x86)\chromedriver.exe"
    driver = webdriver.Chrome(PATH)
    header = ''
    found_words = 0
    while found_words < word_count:
        driver.get("https://en.wikipedia.org/wiki/Special:Random")
        while header == driver.find_element_by_id('firstHeading').text:
            pass
        header = driver.find_element_by_id('firstHeading').text
        try:
            ps = driver.find_elements_by_tag_name('p')
            p = random.choice([p for p in ps if p]).text.split(' ')
            word = random.choice([w for w in p if w and w == w.lower() and w.isalpha() and w not in _dict.keys() and w
                  not in basic_words + revised and all(ord(c) < 128 for c in w) and max_length >= len(w) >= min_length])
            driver.get(f"https://www.spanishdict.com/translate/{word}")
            translation = driver.find_element_by_id("quickdef1-en").text.split(' ')
            word = driver.find_element_by_class_name("_1xnuU6l-").text
            if word in list(_dict.keys()) + basic_words:
                continue
            _dict.update({word: translation[1:] if len(translation) > 1 and translation[0] in ('el', 'la', 'los', 'las',
                  'el/la', 'los/las') else ' '.join(translation)})
            if example_sentence:
                English = driver.find_element_by_class_name("_1f2Xuesa").text
                Spanish = driver.find_element_by_class_name("_3WrcYAGx").text
                sentence_dict.update({word: Spanish if to_English else English})
            source_dict.update({word: header})
            found_words += 1
        except (IndexError, NoSuchElementException):
            pass

    driver.quit()

    score = 0
    for e, word in enumerate(_dict, start=1):
        if example_sentence:
            print(sentence_dict[word])
        prompt, answer = _dict[word] if to_English else word, word if to_English else _dict[word]
        user = input(f'{e}) ' + prompt + (f' ({source_dict[word]}):\n' if print_source else ':\n'))
        print(f'{answer} - {"correct" if user.lower() == answer else "incorrect"}\n')
        if user.lower() != answer:
            user = input("Type 'x' to mark as correct, or enter any key.\n")
        if user.lower() == 'x' or user.lower() == answer:
            score += 1
            if note_correct:
                with open('correct.txt', 'a') as f:
                    f.write('\n' + word)

    print(f"{score} out of {len(_dict)} - {int(score / len(_dict) * 100)}%")


if __name__ == '__main__':
    main()
