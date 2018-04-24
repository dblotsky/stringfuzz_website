import sys
import re

date_pattern = r'(?P<month>\d\d)-(?P<day>\d\d)-(?P<year>\d\d\d\d)'
time_pattern = (
    r'from-' +
    r'(?P<from_hour>\d\d)h(?P<from_minute>\d\d)m(?P<from_second>\d\d)s' +
    r'-to-' +
    r'(?P<to_hour>\d\d)h(?P<to_minute>\d\d)m(?P<to_second>\d\d)s'
)
name_pattern = r'.*' + date_pattern + r'-' + time_pattern + r'.*'

def main():
    name = sys.argv[1]
    match = re.match(name_pattern, name)
    if match is not None:
        print('date: {year}-{month}-{day} {from_hour}:{from_minute}:{from_second}'.format(**match.groupdict()))

if __name__ == '__main__':
    main()
