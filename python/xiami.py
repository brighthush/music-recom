#coding=UTF-8
import urllib2
import gzip
import StringIO
from bs4 import BeautifulSoup
import json

OUT_DIR = '../data/'
WEBSITE = 'http://www.xiami.com'

colls = {}
arts = {}
songs = {}
colls_name = {}

def decodePage(page):
    encoding = page.info().get("Content-Encoding")
    try:
        if encoding in ('gzip', 'x-gzip', 'deflate'):
            content = page.read()
            if encoding == 'deflate':
                data = StringIO.StringIO(zlib.decompress(content))
            else:
                data = gzip.GzipFile('', 'rb', 9, StringIO.StringIO(content))
            page = data.read()
        else:
            page = page.read()
        return page
    except:
        return None

def get_page(url):
    header = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6', 'Accept-Encoding':'gzip'}
    request = urllib2.Request(url,  headers=header)
    response = urllib2.urlopen(request)
    #print response.info().get('Content-Encoding')
    the_page = decodePage(response)
    return the_page

def get_last(string, delim):
    items = string.split(delim)
    return items[-1]

coll_cnt = 0
# parse collection page
def get_coll(url):
    print 'get_collection %s ...' %(url)
    global coll_cnt
    global colls
    global arts
    global songs
    coll_id = get_last(url, '/')
    if coll_id in colls:
        print '%s had been crawled.' %(url)
        return
    else:
        print 'get_coll %s, coll_cnt=%d ...' %(url, coll_cnt)
        coll_cnt += 1
    the_page = get_page(url)
    soup = BeautifulSoup(the_page, from_encoding='UTF-8')
    if soup.link.get('href') != None:
        coll_url = soup.link['href']
        #print coll_url
        coll_id = get_last(coll_url, '/')
        #print coll_id
    else:
        return
    lists = soup.find_all('span')
    coll = []
    for l in lists:
        if l.get('class') != None and l['class'][0] == u'song_name':
            song_artist = l.find_all('a')
            if len(song_artist) == 2:
                song = song_artist[0]
                song_id = song['href']
                song_name = unicode(song.string)
                song_id = get_last(song_id, u'/')
                artist = song_artist[1]
                artist_id = artist['href']
                artist_name = unicode(artist.string)
                artist_id = get_last(artist_id, u'/')
                print '\t', song_id, song_name, artist_id, artist_name
                coll.append([song_id, artist_id])
                if song_id not in songs:
                    songs[song_id] = song_name
                if artist_id not in arts:
                    arts[artist_id] = artist_name
    colls[coll_id] = coll
    print 'finished call_localnewslist ...'

def extract_next(soup):
    a_list = soup.find_all('a')
    for a in a_list:
        if a.get('class') != None and a['class'][0]=='p_redirect_l':
            next_url = a['href']
            return WEBSITE + next_url
    return None


def extract_links(soup):
    global colls_name
    links = []
    a_list = soup.find_all('a')
    for a in a_list:
        if a.get('title')!=None and a.get('href')!=None:
            if a['href'].startswith('http://www.xiami.com/collect/'):
                if get_last(a['href'], '/').isdigit():
                    link = a['href']
                    if link not in colls_name:
                        colls_name[link] = a['title']
                        links.append(link)
    return links

def walk(url):
    page_cnt = 0
    while True:
        print 'walk to %s, page_cnt %d...' %(url, page_cnt)
        page = get_page(url)
        soup = BeautifulSoup(page, from_encoding='UTF-8')
        links = extract_links(soup)
        for link in links:
            get_coll(link)
        page_cnt += 1
        print 'get %d collections, %d different songs, %d differnet artists.' \
                %(len(colls), len(songs), len(arts))
        next_url = extract_next(soup)
        if next_url == None:
            break
        url = next_url

def dump_file(val, path):
    fout = open(path, 'w')
    val_json = json.dumps(val)
    fout.write(val_json)
    fout.close()

def load_file(path):
    fin = open(path, 'r')
    val_json = fin.read()
    val = json.loads(val_json)
    fin.close()
    return val

def main():
    #get_coll('http://www.xiami.com/collect/40902765')
    #get_coll('http://www.xiami.com/collect/41304337')
    walk('http://www.xiami.com/search/orinew?spm=a1z1s.3061701.6856305.6.UR9ZWI&order=favorites&l=0')
    dump_file(songs, OUT_DIR + 'songs.txt')
    dump_file(arts, OUT_DIR + 'arts.txt')
    dump_file(colls, OUT_DIR + 'colls.txt')
    dump_file(colls_name, OUT_DIR + 'colls_name.txt')

def test_load():
    global songs
    global arts
    global colls
    songs = load_file(OUT_DIR + 'songs.txt')
    arts = load_file(OUT_DIR + 'arts.txt')
    colls = load_file(OUT_DIR + 'colls.txt')
    print songs
    print arts
    print colls

if __name__ == '__main__':
    main()
    #test_load()


