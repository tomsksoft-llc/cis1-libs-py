import sys
import requests
import httplib2
import re
from bs4 import BeautifulSoup, SoupStrainer
from urllib.parse import urlparse

class Link:
    def __init__(self, link, valid, parent_url, status, external):
        self.valid = valid
        self.parent_url = parent_url
        self.link = link
        self.status = status
        self.external = external


def link_check(url, depth, main_links_check):
    external_links, internal_links = get_links(url)
    if internal_links:
        for link in internal_links:
            if depth != 0:
                if url.external:
                    new_url = Link(
                        link, None,
                        url.link, None,
                        False

                    )
                else:
                    new_url = Link(
                        link, None,
                        url.parent_url, None,
                        False
                    )
                urls.append(new_url)
                link_check(new_url, depth - 1, False)

    if external_check and external_links:
        for link in external_links:
            if depth != 0:
                new_url = Link(
                    link, None,
                    url.link, None,
                    True
                )
                urls.append(new_url)
                link_check(new_url, depth - 1, False)

    if main_links_check:
        complete_check()


def complete_check():
    print(len(urls))
    print('Web site: {0} has invalid URLs:'.format(main_link.link))
    for url in urls:
        if not url.valid:
            print('{0} on parent url {1} ({2})'.format(url.link, url.parent_url, url.status))
    print('URLs on {0} checked, all links work.Valid URLs:'.format(main_link.link))
    for url in urls:
        if url.valid:
            print(url.link)


def link_search(response, tag, attribute):
    added_links = []
    for link in BeautifulSoup(response, "html.parser",
                              from_encoding="iso-8859-1",
                              parse_only=SoupStrainer(tag)):
        if link.has_attr(attribute):
            added_links.append(link[attribute])
    return added_links


def get_links(url):
    try:
        http = httplib2.Http()
        status, response = http.request(url.link)
        url.valid = True
        external_links = []
        internal_links = []
        added_links = link_search(response, 'a', 'href') \
                      + link_search(response, 'link', 'href') \
                      + link_search(response, 'script', 'src') \
                      + link_search(response, 'source', 'srcset') \

        for link in added_links:
            if (link not in check_links) and ((url.parent_url + link) not in check_links):
                check_links.append(link)
                if re.match(regex, link):
                    external_links.append(link)
                else:
                    if url.external:
                        parsed_uri = urlparse(url.link)
                        external_url = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
                        internal_links.append(external_url + link)
                    else:
                        internal_links.append(url.parent_url + link)
        return external_links, internal_links

    except Exception as error:
        url.valid = False
        url.status = type(error).__name__

        return None, None


def usage():
    print('''
usage:

link_check <url> <depth_to_check> <check_only_internal>
url - url from which to start checking
depth_to_check 1,2,3,.. - depth checking
check_external = True|False - check external links or only internal

Return value:

0 - always
non zero - if any error during start script
''')


if '__main__':
    regex = re.compile(
        r'^(?:http|ftp)s?://'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
        r'localhost|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$', re.IGNORECASE
    )
    try:
        if sys.argv[1] == '--help':
            usage()
            raise sys.exit(0)

        result = requests.get(sys.argv[1])
        main_link = Link(
            sys.argv[1], True,
            sys.argv[1], None,
            True,
        )
        initial_depth = int(sys.argv[2])
        urls = []
        check_links = [main_link.link]
        external_check = sys.argv[3]

        if external_check == 'False':
            external_check = False
        elif external_check == 'True':
            external_check = True
        else:
            raise Exception('External must be True or False')
        if initial_depth <= 0:
            raise Exception('Depth must be > 0')

        link_check(main_link, initial_depth, True)

    except Exception as err:
        print(err)
        usage()
