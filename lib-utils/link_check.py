##############################################################################
#
# Copyright (c) 2020 TomskSoft LLC
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
# Author: Maxim Felchuck
#
##############################################################################
'''Tis is a script for checking a site for broken links

'''
import argparse
import sys
import re
import requests
from bs4 import BeautifulSoup
from progress.bar import IncrementalBar
from urllib3.exceptions import InsecureRequestWarning
import time


class Link:
    def __init__(self, link, status, way, host):
        self.link = link
        self.status = status
        self.way = way
        self.host = host

_valid_links = []
_invalid_links = []
_checked_links = []
_regex = re.compile(
    r'^(?:http|ftp)s?://'
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
    r'localhost|'
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
    r'(?::\d+)?'
    r'(?:/?|[/?]\S+)$', re.IGNORECASE
)
_FORBIDDEN_PREFIXES = ['#','tel:', 'mailto:']
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
_headers = {
  'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
  'accept-encoding':'gzip, deflate, br',
  'accept-language':'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
  'cache-control':'no-cache',
  'dnt': '1',
  'pragma': 'no-cache',
  'sec-fetch-mode': 'navigate',
  'sec-fetch-site': 'none',
  'sec-fetch-user': '?1',
  'upgrade-insecure-requests': '1',
  'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}
def _is_downloadable(url):
    """
    Does the url contain a downloadable resource
    """
    
    head = requests.head(url, allow_redirects=True, verify=False)
    header = head.headers
    content_type = header.get('content-type')
    if 'text' in content_type.lower():
        return False
    if 'html' in content_type.lower():
        return False
    return True


def link_check(url, depth, check_external):
    '''Checking site for broken links to specified url

    Args:
        url: site url
        depth: depth cheking
        check_external: check external links or only internal

    Returns:
        0: on success
        non 0: if fail
    '''
    if isinstance(url, str):
        if depth < 0:
            return -1
        elif depth == 0:
            try:
                request = requests.get(url, verify=False)
                status = request.status_code
                print('Url {0} checked\nstatus code - {1}'.format(url, status))
                return 0
            except Exception as err:
                print('Url {0} checked\nError: {1}'.format(url, err))
                return -1
        else:
            sert = url.split("//")[0]
            host = sert + '//' + url.replace(url.split("//")[0], '').replace("//", '').split('/')[0]
            url = Link(url, None, '', host)
            _checked_links.append(url.link)
            main_url = True
    else:
        main_url = False
        
    try:
        if _is_downloadable(url.link):
            request = requests.head(url.link, verify=False)
            status = request.status_code
            if main_url:
                print('{0} is downloadable link'.format(url.link))
                print('checked\nstatus code - {0}'.format(status))
                return status
            if request.ok:
                _valid_links.append(url)
            else:
                _invalid_links.append(url)

            return 0
    except Exception as err:
        url.status = err
        _invalid_links.append(url)
        if main_url:
            print('{0} is downloadable link'.format(url.link))
            print('checked\nstatus code - {0}'.format(url.status))
            return -1

        return 0

    try:
        time.sleep(0.01)
        request = requests.get(url.link, headers=_headers, verify=False)
        status = request.status_code
        url.status = status
        if request.ok:
            _valid_links.append(url)
        else:
            _invalid_links.append(url)

    except Exception as err:
        url.status = err
        _invalid_links.append(url)
        return 0
    if depth == 0:
        return 0
    soup = BeautifulSoup(request.content, 'lxml')
    links = _link_search(soup, 'a', 'href', url) \
            + _link_search(soup, 'link', 'href', url) \
            + _link_search(soup, 'script', 'src', url) \
            + _link_search(soup, 'source', 'srcset', url) \
            + _link_search(soup, 'img', 'src', url) \
            + _link_search(soup, 'div', 'href', url) \
            
    if main_url:
        progress_bar = IncrementalBar('Checking: ', max=len(links),
                                      suffix='%(percent).1f%% - %(elapsed)ds')

    for link in links:
        if url.host in link:
            link_check(Link(link, None, url.way + '->' + url.link, url.host),
                       depth - 1, check_external)
        elif check_external:
            link_check(Link(link, None, url.way + '->' + url.link, None), 0, False)
        if main_url:
            progress_bar.next()

    if main_url:
        progress_bar.finish()
        _complete_check(url)
        return status
    
    return 0


def _link_search(soup, tag_name, attr, url):
    links = []
    host = url.host
    url = url.link
    for end in ['.php', '.html']:
        if end in url:     
            new_url = url.replace(url.split('/')[-1], '')  
    for tag in soup.find_all(tag_name):
        if tag.has_attr(attr):
            link = tag[attr]
            if all(not link.startswith(prefix) for prefix in _FORBIDDEN_PREFIXES):
                if link.startswith('javascript:') or link == '/':
                    continue
                if re.match(_regex, link):
                    pass
                elif link.startswith('//'):
                    link = host.split('//')[0] + link
                elif link.startswith('/'):
                    link = host + link
                elif link.startswith('..'):
                    link = new_url.replace(new_url.split('/')[-1], '') + link.replace('..','')
                else:
                    link = new_url + '/' + link
                if link not in _checked_links:
                    links.append(link)
                    _checked_links.append(link)

        else:
            pass
    return links


def _complete_check(main_link):
    if len(_invalid_links) > 0:
        print('Web site: {0} has invalid URLs:'.format(main_link.link))
        for url in _invalid_links:
            print('----------------------')
            print(url.link)
            print('Status: ', url.status)
            print('Way to invalid url: \n', url.way)
        print('Valid URLs: ')
    else:
        print('URLs on {0} checked, all links work. Valid URLs:'.format(main_link.link))
    for url in _valid_links:
        print(url.link)


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
    if args.depth_to_check <= 0:
        print('''<depth_to_check> must be > 0''')
        print('usage: ' + use_as_os_command.__doc__)
        sys.exit(2)
    if args.check_external is None:
        print('''<check_internal> isn't specified''')
        print('usage: ' + use_as_os_command.__doc__)
        sys.exit(2)
    check_external = args.check_external
    if check_external == 'False':
        check_external = False
    elif check_external == 'True':
        check_external = True
    else:
        print('''<check_external> must be True or False''')
        print('usage: ' + use_as_os_command.__doc__)
        sys.exit(2)

    link_check(args.url, args.depth_to_check, check_external)


if __name__ == '__main__':
    use_as_os_command()
