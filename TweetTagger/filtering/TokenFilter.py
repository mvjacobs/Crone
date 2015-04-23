__author__ = 'marc'

from BeautifulSoup import BeautifulSoup


def remove_html(html):
    soup = BeautifulSoup(html)
    if soup.a:
        return soup.a.renderContents()
    else:
        return html
