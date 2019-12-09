##############################################################################
#
# Copyright (c) 2019 TomskSoft LLC
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# FILE: link_check.py
# Authors: Maxim Felchuck
#
##############################################################################
'''It is a script for checking the site for working and non-working links
for specified depth checking and external/internal checking

'''
import argparse
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


def link_check(url, depth, main_links_check, urls, external_check, checked_links):
    external_links, internal_links = get_links(url, checked_links)
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
                link_check(new_url, depth - 1, [main_links_check[0], False], urls, external_check, checked_links)

    if external_check and external_links:
        for link in external_links:
            if depth != 0:
                new_url = Link(
                    link, None,
                    url.link, None,
                    True
                )
                urls.append(new_url)
                link_check(new_url, depth - 1, [main_links_check[0], False], urls, external_check, checked_links)

    if main_links_check[1]:
        complete_check(urls, main_links_check[0])


def complete_check(urls, main_link):
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


def get_links(url, checked_links):
    regex = re.compile(
        r'^(?:http|ftp)s?://'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
        r'localhost|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$', re.IGNORECASE
    )

    http = httplib2.Http()
    try:
        status, response = http.request(url.link)
        url.valid = True
    except Exception as error:
        url.valid = False
        url.status = type(error).__name__
        return None, None
    external_links = []
    internal_links = []
    added_links = link_search(response, 'a', 'href') \
                  + link_search(response, 'link', 'href') \
                  + link_search(response, 'script', 'src') \
                  + link_search(response, 'source', 'srcset') \
                  + link_search(response, 'img', 'src')

    for link in added_links:
        if (link not in checked_links) and ((url.parent_url + link) not in checked_links) \
                and (url.link + link not in checked_links):
            if (re.match(regex, link)) and (url.link not in link) \
                    and ((link.split("//")[-1].split("/")[0]) not in url.link):

                external_links.append(link)
                checked_links.append(link)
            else:
                if url.external:
                    parsed_uri = urlparse(url.link)
                    external_url = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
                    internal_links.append(external_url + link)
                    checked_links.append(external_url + link)
                else:
                    home = link.split("//")[-1].split("/")[0]
                    if (link.split("//")[-1].split("/")[0] in url.link) and (len(home) > 0):
                        internal_links.append(link)
                        checked_links.append(link)

                    else:

                        internal_links.append(url.parent_url + '/' + link)
                        checked_links.append(url.parent_url + link)
    return external_links, internal_links


def use_as_os_command():
    '''usage: link_check <url> <depth_to_check> <check_only_internal>

    url - url from which to start checking
    depth_to_check 1,2,3,.. - depth checking
    check_external = True|False - check external links or only internal

    Return value:

    0 - always
    non zero - if any error during start script
    '''
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('-h', '--help', action='store_true')
    parser.add_argument('url', nargs='?')
    parser.add_argument('depth_to_check', nargs='?', type=int)
    parser.add_argument('check_external', nargs='?')
    parser.usage = use_as_os_command.__doc__
    args = parser.parse_args()
    if args.help:
        print('usage: ' + use_as_os_command.__doc__)
        sys.exit(0)
    if args.url is None:
        print('''<url> isn't specified''')
        print('usage: ' + use_as_os_command.__doc__)
        sys.exit(2)
    if args.depth_to_check is None:
        print('''<depth_to_check> isn't specified''')
        print('usage: ' + use_as_os_command.__doc__)
        sys.exit(2)
    if args.check_external is None:
        print('''<check_external> isn't specified''')
        print('usage: ' + use_as_os_command.__doc__)
        sys.exit(2)
    if args.depth_to_check <= 0:
        print('''<depth_to_check> must be >= 0''')
        print('usage: ' + use_as_os_command.__doc__)
        sys.exit(2)
    external_check = args.check_external
    if external_check == 'False':
        external_check = False
    elif external_check == 'True':
        external_check = True
    else:
        print('''<check_external> must be True or False''')
        print('usage: ' + use_as_os_command.__doc__)
        sys.exit(2)

    try:
        requests.get(args.url)
    except Exception:
        print('{0} - connection error'.format(args.url))
        print('usage: ' + use_as_os_command.__doc__)
        sys.exit(2)
    main_link = Link(
        args.url, True,
        args.url, None,
        False,
    )
    urls = []
    checked_links = [main_link.link]

    link_check(main_link, args.depth_to_check, [main_link, True],
               urls, external_check, checked_links)


if __name__ == '__main__':
    use_as_os_command()
