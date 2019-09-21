import sys
import requests
import httplib2
from bs4 import BeautifulSoup, SoupStrainer


class Link:
    def __init__(self, link, valid, parent, status):
        self.valid = valid
        self.parent = parent
        self.link = link
        self.status = status
        pass


def start(url, depth, main):
    external_links, internal_links = get_links(url)
    if external and external_links:
        check(internal_links + external_links, url.link, depth - 1, main)
    elif not external and internal_links:
        check(internal_links, url.link, depth - 1, main)
    pass


def check(urls, parent_link, depth, main):
    for link in urls:
        if depth != 0:
            new_link = Link(link, None, parent_link, None)
            links.append(new_link)
            start(new_link, depth, False)
    if main:
        end_status()
    pass


def end_status():
    print(len(links))
    print('Web site: {0} has invalid URLs:'.format(main_link.link))

    for link in links:
        if not link.valid:
            print('{0} on parent url {1} ({2})'.format(link.link, link.parent, link.status))
    print('URLs on {0} checked, all links work.Valid URLs:'.format(main_link.link))
    for link in links:
        if link.valid:
            print(link.link)


def link_add(response, tag, attr):
    added_links = []
    for link in BeautifulSoup(response, "html.parser", from_encoding="iso-8859-1", parse_only=SoupStrainer(tag)):
        if link.has_attr(attr):
            added_links.append(link[attr])
    return added_links


def get_links(url):
    try:
        http = httplib2.Http()
        status, response = http.request(url.link)

        url.valid = True

        external_links = []
        internal_links = []
        url.link = url.link.replace('www.', '')
        if not url.parent:
            url.parent = main_link.link
        added_links = []
        added_links += link_add(response, 'a', 'href') + \
                    link_add(response, 'link', 'href') + \
                    link_add(response, 'script', 'src') + \
                    link_add(response, 'source', 'srcset')

        for link in added_links:
            link = link.replace('www.', '')
            new_internal, new_external = check_teg(link, url)
            internal_links += new_internal
            external_links += new_external

        return external_links, internal_links

    except Exception as error:
        url.valid = False
        url.status = type(error).__name__

        return None, None


def check_teg(link, url):
    internal_new_link = []
    external_new_link = []
    if (link not in check_links) and ((url.parent + link) not in check_links):
        check_links.append(link)
        if 'http' not in link:
            internal_new_link.append(url.parent + link)
        else:
            external_new_link.append(link)

    return external_new_link, internal_new_link


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

    try:
        if sys.argv[1] == '--help':
            usage()
            raise sys.exit(0)
        res = requests.get(sys.argv[1])
        main_link = Link(sys.argv[1], True, None, None)
        depth = int(sys.argv[2]) + 1
        links = []
        check_links = []
        external = sys.argv[3]
        if external == 'False':
            external = False
        elif external == 'True':
            external = True
        else:
            raise Exception('External must be True or False')

        if depth <= 0:
            raise Exception('Depth must be > 0')

        start(main_link, depth, True)
    except Exception as err:
        print(err)
        usage()
