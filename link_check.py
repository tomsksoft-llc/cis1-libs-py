from bs4 import BeautifulSoup
import urllib.request
import traceback
import sys
def start(url, link, depth, external, invalid_links, valid_links, main, path):
    if not external and main:
        path.append(url)
        links,static_files = get_links(url)
        print('Checking ' + url + '...')
        check_i(url, links, static_files, depth-1, external, invalid_links, valid_links, True, path)
        print('\n')
    elif not external and not main:
        links, static_files = get_links(url + '/' + link)
        path.append(link)
        check_i(url, links, static_files, depth-1, external, invalid_links, valid_links, False, path)
    elif external and main:
        path.append(url)
        links,static_files = get_links(url)
        print('Checking ' + url + '...')
        check_e(url, links, static_files, depth-1, external, invalid_links, valid_links, True, path)
        print('\n')
    elif external and not main:
        links, static_files = get_links(url + '/' + link)
        path.append(link)
        check_e(url, links, static_files, depth-1, external, invalid_links, valid_links, False, path)
        
def get_links(url):

    resp = urllib.request.urlopen(url)
    soup = BeautifulSoup(resp, 'html.parser')
    static_files = []
    links = []
    for link in soup.find_all('a', href=True):
            links.append(link['href'])
    for link in soup.find_all('link', href=True):
            static_files.append(link['href'])
               
    for link in soup.find_all('img', src=True):
            static_files.append(link['src'])
                
    for link in soup.find_all('script', src=True):
            static_files.append(link['src'])

    return links, static_files

def check_e(url, links, static_files, depth, external, invalid_links, valid_links, main, path):
    for link in static_files:
        try:
            if (link not in valid_links) and (link not in invalid_links):
                try:
                    resp = urllib.request.urlopen(link)
                    valid_links[link] = 'external'

                except:
                    resp = urllib.request.urlopen(url + '/' + link)
                    valid_links[link] = 'internal'

        except Exception as err:
            invalid_links[link] = (err, url, path)

    for link in links:
        try:
            if (link not in valid_links) and (link not in invalid_links):
                try:
                    resp = urllib.request.urlopen(link)
                    valid_links[link] = 'external'
                    if depth != 0:
                        start(link, '', depth, external, invalid_links, valid_links, False, path)

                except:
                    resp = urllib.request.urlopen(url + '/' + link)
                    valid_links[link] = 'internal'
                    if depth != 0:
                        start(url, link, depth, external, invalid_links, valid_links, False, path)
            

        except Exception as err:

            invalid_links[link] = (err, url, path)
    if main:
        end_status(url, valid_links, invalid_links)

def check_i(url, links, static_files, depth, is_link, invalid_links, valid_links, main, path):
    for link in static_files:
        try:
            if (link not in valid_links) and (link not in invalid_links):
                try:
                    resp = urllib.request.urlopen(link)
                    valid_links[link] = 'external'

                except:
                    resp = urllib.request.urlopen(url + '/' + link)
                    valid_links[link] = 'internal'

        except Exception as err:

            invalid_links[link] = (err, url, path)

    for link in links:
        if ('.html' in link) and (link not in valid_links) and (link not in invalid_links):
            try:
                resp = urllib.request.urlopen(url + '/' + link)
                valid_links[link] = 'internal'
            except Exception as err:
                invalid_links[link] = (err, url, path)

            if depth != 0:
                start(url, link, depth, external, invalid_links, valid_links, False, path)
    if main:
        end_status(url, valid_links, invalid_links)

def end_status(url, valid_links, invalid_links):

    print('\nURLs on {0} checked, all links work.Valid URLs: \n'.format(url))
    for key, value in valid_links.items():
        if value == 'internal':
            print(url + '/' + key)
        else:
            print(key)
    print('\nWeb site: {0} has invalid URLs:'.format(url))
    for key, value in invalid_links.items():
        print('\n' + key)
        print('Error: ({0})'.format(value[0]))
        for i in value[2]:
            if i != url:
                print(url + '/' + i)
            else:
                print (url)

def usage():
    print('''
usage:

link_check <url> <depth_to_check> <check_only_internal>
url - url from which to start checking
depth_to_check 1,2,3,.. - depth checking
check_only_internal = True|False - check external links or only internal

Return value:

0 - always
non zero - if any error during start script
''')
if '__main__':


    
    if sys.argv == '--help':
        usage()
    try:
        url = sys.argv[1]
        depth = int(sys.argv[2])
        external = bool(sys.argv[3])
        if depth <= 0:
            raise Exception('depth must be > 0')
        if (external != True) and (external != False):
            raise Exception()
        start(url, '', depth, external, {}, {}, True, [])
        

    except Exception as err:
        print(err)
        usage()
        

    
