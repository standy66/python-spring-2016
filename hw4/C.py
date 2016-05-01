import sys
import re

regexp = re.compile(r'import (?P<modules>[\w\.]+(?:,\s+[\w\.]+)*)|'
                    r'from\s+(?P<module>[\w\.]+)\s+import.+')

text = sys.stdin.read()
modules = set()
for match in regexp.finditer(text):
    if match.groupdict()['module']:
        modules.add(match.groupdict()['module'])
    if match.groupdict()['modules']:
        mod_list = match.groupdict()['modules']
        results = re.split(r',\s+', mod_list)
        modules = modules.union(set(results))

print(", ".join(sorted(modules)))
