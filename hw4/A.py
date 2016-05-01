import sys

s = input()
langs = dict()
while len(s) > 0:
    lang, d = s.split()
    for ch in d.lower():
        langs[ch] = lang
    s = input()

try:
    s = input()
except:
    sys.exit(0)
while len(s) > 0:
    text_langs = set()
    for word in s.split():
        word_langs = dict()
        for ch in word.lower():
            if ch in langs:
                lang = langs[ch]
                if lang in word_langs:
                    word_langs[lang] += 1
                else:
                    word_langs[lang] = 1
        if (len(word_langs) > 0):
            text_langs.add(min(word_langs.items(), key=lambda x: (-x[1], x[0]))[0])
    for lang in sorted(text_langs):
        print(lang, end=" ")
    print()
    try:
        s = input()
    except:
        sys.exit(0)
