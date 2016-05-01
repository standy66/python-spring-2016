import sys
import re

format_1 = re.compile(r'^(?P<day>[0-9]{2})(?P<delim>[\/\.\-])'
                      r'(?P<month>[0-9]{2})'
                      r'(?P=delim)(?P<year>[0-9]{4})$')
format_2 = re.compile(r'^(?P<year>[0-9]{4})(?P<delim>[\/\.\-])'
                      r'(?P<month>[0-9]{2})(?P=delim)(?P<day>[0-9]{2})$')
format_3 = re.compile(r'^(?P<day>\d{1,2})\s*(?P<month>[А-я]+)\s*(?P<year>\d{4})$')

for line in sys.stdin:
    line = line.strip()
    if (format_1.match(line) or format_2.match(line) or format_3.match(line)):
        print('YES')
    else:
        print('NO')
