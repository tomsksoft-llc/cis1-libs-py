import requests, bs4, webbrowser, re
from selenium import webdriver
import urllib.request
import traceback
import sys


class Link:
    def __init__(self, valid):
        self.valid = valid
        pass


def start(url, depth, main):
    print('Start-', url)
    if not external:
        external_links, internal_links = get_links(url)

        print('External links:', external_links)
        print("Internal links:", internal_links)
        check(internal_links, depth - 1, main)


def check(links, depth, main):
    for link in links:
        print(link)
        print(depth)
        if depth != 0:
            start(link, depth, False)
    if main:
        end_status()
    return


def end_status():
    print('END!')


def get_links(url):
    res = requests.get(url)
    if res.status_code != requests.codes.ok:
        print('{0} is a broken link. Response: 404 Not Found'.format(url))
    else:
        print(url, '----OK LINK!')
    soup = bs4.BeautifulSoup(res.text, "html.parser")
    # links = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
    # res.text)  # список сайтов
    links = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
                       res.text)  # список (протокол, сайт, страница)
    external = []
    internal = []
    for link in links:
        if url in link:
            internal.append(link)
        else:
            external.append(link)
    for link in soup.find_all('a', href=True):
        if (link['href'] not in internal) and (link['href'] not in external):

            internal.append(url + link['href'])#не правильная конструкция, на более высокой глубине неккоректные ссылки. создать класс,
                                                #объекты которого будут содержать в себе ссылку родителя, внутренние ссылки 'logo.php' и т.д записывать в виде
                                                #"ссылка родитель + внутренняя ссылка" (создавая новый объект класса

    return external, internal
    # res = requests.get(url)
    # if res.status_code != requests.codes.ok:

    #  print('{0} is a broken link. Response: 404 Not Found'.format(url))


"""
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
    """
if '__main__':
    external = sys.argv[3]
    depth = int(sys.argv[2])
    invalid_links, valid_links = [], []
    if external == 'False':
        external = False
    start(sys.argv[1], depth, True)
    """
    try:    
        if sys.argv[1] == '--help':
            usage()
            raise sys.exit(0)
        url = sys.argv[1]
        depth = int(sys.argv[2])
        
        external = sys.argv[3]
        if external == 'False':
            external = False
        elif external == 'True':
            external = True
        else:
            raise Exception('External must be True or False')
        
        if depth <= 0:
            raise Exception('depth must be > 0')

        start(url, depth, external)
        

    except Exception as err:
        print(err)
        usage()
"""
