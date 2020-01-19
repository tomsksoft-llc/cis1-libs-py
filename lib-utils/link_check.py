import argparse
import sys
import re
from urllib.parse import urlparse
import httplib2
import requests
from bs4 import BeautifulSoup
import lxml

class Link:
    def __init__(self, link, status, way):
        self.link = link
        self.status = status
        self.way = way


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
_FORBIDDEN_PREFIXES = ['#', 'tel:', 'mailto:']
_way = ''

def link_check(url, depth, check_only_internal):
    global _way
    if type(url) == str:
        depth+=1
        _checked_links.append(url)
        _way = url
        if depth < 0:
            return  -1
        elif depth == 0:
            try:
                request = requests.get(url)
                status = request.status_code
                print('Url {0} checked\nstatus code - {1}'.format(url, status))
                return 0
            except:
                return -1
        else:
            url = Link(url, None, _way)
            main_url = True
    else:
        _way = _way + '->' + url.link
        main_url = False
    host = url.link.split("//")[0] + "//" + url.link.split("//")[-1].split("/")[0]
    domain = url.link.split("//")[-1].split("/")[0]
    try:
        request = requests.get(url.link)
        status = request.status_code
        url.status = status
        if status != 200:
            _invalid_links.append(url)
            return 0
        _valid_links.append(url)
    except Exception as err:
        url.status = err
        _invalid_links.append(url)
        return 0
    if depth < 0:
        _way = _way.split('->')[0]
        return 0
    soup = BeautifulSoup(request.content, 'lxml')
    links = _link_search(soup, 'a', 'href', host, domain) \
     + _link_search(soup, 'link', 'href', host, domain) \
     + _link_search(soup, 'script', 'src', host, domain) \
     + _link_search(soup, 'source', 'srcset', host, domain) \
     + _link_search(soup, 'img', 'src', host, domain) \
     + _link_search(soup, 'div', 'href', host, domain) \
     + _link_search(soup, 'h1', 'href', host, domain) \
     + _link_search(soup, 'h2', 'href', host, domain) \
     + _link_search(soup, 'h3', 'href', host, domain) \
     + _link_search(soup, 'h4', 'href', host, domain)
    internal_links = []
    external_links = []

    for link in links:
        if domain not in link:
            external_links.append(link)
        else:
            internal_links.append(link)
    # check if link must be checked - continue if no
    for link in internal_links:
        if link not in _checked_links:
            _checked_links.append(link)
            link_check(Link(link, None, _way), depth - 1, check_only_internal)
    for link in external_links:
        if link not in _checked_links:
            _checked_links.append(link)
            if check_only_internal:
                link_check(Link(link, None, _way), 0, True)
            else:
                link_check(Link(link, None, _way), depth - 1, check_only_internal)


    if main_url:
        _complete_check(url)
        return status
    else:
        return 0
def _link_search(soup, tag, attr, host, domain):
    links = []
    for tag in soup.find_all(tag):
        if tag.has_attr(attr):
            link = tag[attr]
            if all(not link.startswith(prefix) for prefix in _FORBIDDEN_PREFIXES):
                if link.startswith('/') and not link.startswith('//'):
                    link = host + link
                if urlparse(link).netloc == domain and link not in _checked_links:
                    links.append(link)
        else:
            pass
    return links

def _complete_check(main_link):
    print(len(_valid_links))
    print(len(_invalid_links))
    if len(_invalid_links) > 0:
        print('Web site: {0} has invalid URLs:'.format(main_link.link))
        for url in _invalid_links:
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
    parser.add_argument('check_internal', nargs='?')
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
    if args.check_internal is None:
        print('''<check_internal> isn't specified''')
        print('usage: ' + use_as_os_command.__doc__)
        sys.exit(2)
    check_internal = args.check_internal
    if check_internal == 'False':
        check_internal = False
    elif check_internal == 'True':
        check_internal = True
    else:
        print('''<check_external> must be True or False''')
        print('usage: ' + use_as_os_command.__doc__)
        sys.exit(2)

    link_check(args.url, args.depth_to_check, check_internal)


if __name__ == '__main__':
    use_as_os_command()
