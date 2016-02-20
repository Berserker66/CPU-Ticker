import english
import german

from __init__ import check

langs = german, english

complete = True
for lang in langs:
    missing = check(english, lang)
    for item in missing:
        print(lang.__name__ + ".py", "misses", item)
        complete = False

if not complete:
    import sys
    sys.exit(1)
