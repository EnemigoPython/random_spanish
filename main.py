from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
import random


def new_soup(url):
    client = urlopen(url)
    html_page = client.read()
    client.close()
    page_soup = soup(html_page, "html.parser")
    return page_soup


def main():
    user = input("Number of words to revise? (1-200 limits) \n")
    word_count = int(user) if user.isnumeric() and 200 >= int(user) > 0 else None

    min_length = 0
    max_length = 100
    allow_basic = False
    to_English = True
    example_sentence = True
    note_correct = True
    print_source = False
    save_incorrect = True
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
'[I]ncorrect' to save words answered incorrectly to incorrect.txt. (default enabled)
'[N]ote to note correctly answered words & prevent their repetition. (default enabled)
'[P]rint' to print the Wiki page along with the word. (default disabled)
'[R]eset' to reset correct.txt & incorrect.txt.
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
            if user.lower() in ('incorrect', 'i'):
                save_incorrect = not save_incorrect
                print(f"Save incorrect answers: {'on' if save_incorrect else 'off'}.\n")
            if user.lower() in ('note', 'n'):
                note_correct = not note_correct
                print(f"Note correctly answered: {'on' if note_correct else 'off'}.\n")
            if user.lower() in ('print', 'p'):
                print_source = not print_source
                print(f"Print wiki source: {'on' if print_source else 'off'}.\n")
            if user.lower() in ('reset', 'r'):
                open('correct.txt', 'w').close()
                open('incorrect.txt', 'w').close()
                print("Files reset.\n")
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
    if save_incorrect:
        with open('incorrect.txt', 'r') as f:
            repeat = f.read().splitlines()[1:]
    else:
        repeat = []

    header = ''
    found_words = 0
    print("Working...\n")
    for word in repeat[:min(word_count, len(repeat))]:
        page_soup = new_soup(f"https://www.spanishdict.com/translate/{word}")
        translation = page_soup.find(id="quickdef1-en").text.split(' ')
        _dict.update({word: translation[1] if len(translation) > 1 and translation[0] in ('el', 'la', 'los', 'las',
              'el/la', 'los/las') else ' '.join(translation)})
        source_dict.update({word: header})
        if example_sentence:
            English = page_soup.find(class_="_1f2Xuesa").text
            Spanish = page_soup.find(class_="_3WrcYAGx").text
            sentence_dict.update({word: Spanish if to_English else English})
        found_words += 1
        print(f'{found_words}/{word_count}')
    while found_words < word_count:
        page_soup = new_soup("https://en.wikipedia.org/wiki/Special:Random")
        while header == page_soup.find(id='firstHeading').text:
            pass
        header = page_soup.find(id='firstHeading').text
        try:
            ps = page_soup.findAll('p')
            p = random.choice([p for p in ps if p]).text.split(' ')
            word = random.choice([w for w in p if w and w == w.lower() and w.isalpha() and w not in _dict.keys() and w
                  not in basic_words + revised and all(ord(c) < 128 for c in w) and max_length >= len(w) >= min_length])
            page_soup = new_soup(f"https://www.spanishdict.com/translate/{word}")
            translation = page_soup.find(id="quickdef1-en").text.split(' ')
            word = page_soup.find(class_="_1xnuU6l-").text
            if word in list(_dict.keys()) + basic_words:
                continue
            _dict.update({word: translation[1] if len(translation) > 1 and translation[0] in ('el', 'la', 'los', 'las',
                  'el/la', 'los/las') else ' '.join(translation)})
            source_dict.update({word: header})
            if example_sentence:
                English = page_soup.find(class_="_1f2Xuesa").text
                Spanish = page_soup.find(class_="_3WrcYAGx").text
                sentence_dict.update({word: Spanish if to_English else English})
            found_words += 1
            print(f'{found_words}/{word_count}')
        except (IndexError, AttributeError):
            pass

    print("\nFinished\n")
    score = 0
    for e, word in enumerate(_dict, start=1):
        try:
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
                if save_incorrect and word in repeat:
                    repeat.remove(word)
                    with open('incorrect.txt', 'w') as f:
                        for w in repeat:
                            f.write('\n' + w)
            elif save_incorrect and word not in repeat:
                with open('incorrect.txt', 'a') as f:
                    f.write('\n' + word)
        except KeyError:
            pass

    print(f"{score} out of {len(_dict)} - {int(score / len(_dict) * 100)}%")


if __name__ == '__main__':
    main()
