# random_spanish
Using ~~Selenium~~ BeautifulSoup4, generates a set of words to study by translating to and from English and Spanish.

# NEW BRANCH
I decided for multiple reasons that BS4 might be a better fit for this project, but I will keep the two models separate. This way there is no need for a driver, which is not necessary in any case.

# SITES SCRAPED
Wikipedia (en) random article feature to source words

SpanishDict to translate the words into Spanish

# REQUIREMENTS
Python 3.9

BS4

Urllib

# FILES
main.py - executable file

basic.txt - a preset list of the most common English words - these can be toggled to avoid/allow as target words

correct.txt - as you correctly translate words, you are given the option to avoid repetitions of these words using this file to record them

# FEATURES/COMMANDS
[A]ll: print commands

[B]asic: enable/disable basic.txt filter

[E]xample: enable/disable example (context) sentence for each word

[N]ote: enable/disable correct.txt filter

[P]rint: print the name of the Wikipedia source page for each word

[R]eset: empty correct.txt

'>': set maximum word length

'<': set minimum word length
