__author__ = 'marc'

import re


def extract_all_url(tweet):
    result = []

    p = re.compile(r'https?://[^\s]+')

    for url in p.finditer(tweet):
        new_link = {'start': url.start(), 'end': url.end()}
        result.append(new_link)

    return result

