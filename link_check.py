import sys
import bs4
import re
import requests


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
        if main:
            print('MAIN-----')
        #print(depth)
        if depth != 0:
            new_link = Link(link, None, parent_link, None)
            links.append(new_link)
            start(new_link, depth, False)
    if main:
        end_status()
    pass


def end_status():
    print('Web site: {0} has invalid URLs:'.format(main_link.link))
    print(len(links))
    for link in links:
        if not link.valid:
            print('{0} on parent url {1} ({2})'.format(link.link, link.parent, link.status))
    print('URLs on {0} checked, all links work.Valid URLs:'.format(main_link.link))
    for link in links:
        if link.valid:
            print(link.link)



def get_links(url):
    try:
        result = requests.get(url.link)
        url.valid = True
        soup = bs4.BeautifulSoup(res.text, "html.parser")
        urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
                          result.text)
        external_links = []
        internal_links = []
        url.link = url.link.replace('www.', '')

        for link in urls:
            link = link.replace('www.', '')
            if link not in check_links:

                check_links.append(link)
                if url.link in link:

                    internal_links.append(link)
                else:

                    external_links.append(link)

        if not url.parent:
            url.parent = main_link.link
        for href in soup.find_all('a', href=True):


            link = href['href']
            link = link.replace('www.', '')

            href_external, href_internal = check_teg(link, url, internal_links, external_links)
            internal_links += href_internal
            external_links += href_external

        for href in soup.find_all('link', href=True):
            link = href['href']
            link = link.replace('www.', '')

            href_external, href_internal = check_teg(link, url, internal_links, external_links)

            internal_links += href_internal
            external_links += href_external

        for src in soup.find_all('script', src=True):
            link = src['src']
            link = link.replace('www.', '')

            src_external, src_internal = check_teg(link, url, internal_links, external_links)
            internal_links += src_internal
            external_links += src_external

        for srcset in soup.find_all('source', srcset=True):
            link = srcset['srcset']
            link = link.replace('www.', '')

            srcset_external, srcset_internal = check_teg(link, url, internal_links, external_links)
            internal_links += srcset_internal
            external_links += srcset_external

        return external_links, internal_links

    except Exception as error:
        url.valid = False

        url.status = type(error).__name__

        return None, None


def check_teg(link, url, internal_links, external_links):

    internal_new_link = []
    external_new_link = []
    if (link not in check_links) and ((url.parent + link) not in check_links):

        check_links.append(link)
        if (link not in internal_links) and (link not in external_links):

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
