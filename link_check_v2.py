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
        if depth != 0:
            new_link = Link(link, None, parent_link, None)
            links.append(new_link)
            start(new_link, depth, False)
    if main:
        end_status()
    pass


def end_status():
    print('Web site: {0} has invalid URLs:'.format(main_link.link))
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
            check_links.append(link) #проверить

            if link not in check_links:
                if url.link in link:
                    internal_links.append(link)
                else:
                    external_links.append(link)
        if not url.parent:
            url.parent = main_link.link
        all_links = soup.find_all('a', href=True) + soup.find_all('link', href=True) + soup.find_all('script', src=True) \
                    + soup.find_all('source', srcset=True)

        for href in soup.find_all('a', href=True):
             #доделать
            #href = href.replace('www.', '')
            link = href['href']

            if (link not in links) and ((url.parent + link) not in links) and ((main_link.link + link) not in links):
                if (link not in internal_links) and (link not in external_links):

                    if 'http' not in link:
                        internal_links.append(url.parent + link)
                    else:
                        external_links.append(link)

        return external_links, internal_links

    except Exception as error:
        url.valid = False
        url.status = type(error).__name__
        #print(error)
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
