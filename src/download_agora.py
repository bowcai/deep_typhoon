import urllib.request
import urllib.error
import urllib.parse
import re
import os
import threading
from bs4 import BeautifulSoup


def get_ty_links(start_year, end_year):
    years = []
    year_links = []
    for i in range(start_year, end_year):
        years.append(str(i))
        year_links.append('http://agora.ex.nii.ac.jp/digital-typhoon/year/wnp/' + str(i) + '.html.en')

    tys = []
    ty_links = []
    for i in range(0, len(years)):
        html = None
        while True:
            try:
                html = urllib.request.urlopen(year_links[i]).read()
            except Exception as e:
                print(e)
                continue
            break

        soup = BeautifulSoup(html, "html.parser")
        row1 = soup.find_all(attrs={"class": "ROW1"})
        row0 = soup.find_all(attrs={"class": "ROW0"})
        # get all typhoon-page links
        number = len(row1) + len(row0)
        for j in range(1, 10):
            tys.append(years[i] + '0' + str(j))
            ty_links.append('http://agora.ex.nii.ac.jp/digital-typhoon/summary/wnp/k/' +
                            years[i] + '0' + str(j) + '.html.en')
        for j in range(10, number + 1):
            tys.append(years[i] + str(j))
            ty_links.append('http://agora.ex.nii.ac.jp/digital-typhoon/summary/wnp/k/' +
                            years[i] + str(j) + '.html.en')

    return tys, ty_links


def download_imgs(path_, tys, ty_links):
    root = path_ + '/tys_raw/'
    if not os.path.exists(root):
        os.mkdir(root)

    for i in range(0, len(ty_links)):
        html = None
        while True:
            try:
                html = urllib.request.urlopen(ty_links[i]).read()
            except Exception as e:
                print(e)
                continue
            break

        soup = BeautifulSoup(html, "html.parser")
        a_list = soup.find_all('a')
        # all satellite images for every 6 hour
        for a in a_list:
            if a.string != '\n\t\tImage':
                continue

            image_link = 'http://agora.ex.nii.ac.jp/' + a['href']

            html_new = None
            while True:
                try:
                    html_new = urllib.request.urlopen(image_link).read()
                except Exception as e:
                    print(e)
                    continue
                break

            soup_new = BeautifulSoup(html_new, "html.parser")
            tr_list = soup_new.find_all('tr')

            boo = False
            wind = '0'
            for tr in tr_list:
                if 'Maximum Wind' in str(tr.string):
                    tr_next = tr.next_sibling.next_sibling
                    if tr_next.string[0] == '0':  # 0kt should be excluded
                        boo = True
                        break
                    wind = str(re.findall(r'\d+', tr_next.string))
            if boo:  # 0kt should be excluded
                continue

            pressure = '1000'
            for tr in tr_list:
                if 'Central Pressure' in str(tr.string):
                    tr_next = tr.next_sibling.next_sibling
                    pressure = str(re.findall(r'\d+', tr_next.string))

            pict_list = []
            anew_list = soup_new.find_all('a')
            for anew in anew_list:  # find ir images
                if anew.string == 'Magnify this':
                    st = anew['href']
                    if st.find("/1/") != -1:
                        print(st)
                        pict_list.append('http://agora.ex.nii.ac.jp' + st)

            try:  # save images
                s = pict_list[0]
                # filename : typhoon-number_time(YYMMDDHH)_wind_pressure.jpg
                filename = tys[i] + '_' + s[len(s) - 19:len(s) - 11] + '_' + wind + '_' + pressure
                filename = rename(filename)

                f = open(root + filename + '.jpg', 'wb')

                req = None
                while True:
                    try:
                        req = urllib.request.urlopen(s)
                    except Exception as e:
                        print(e)
                        continue
                    break

                buf = req.read()
                f.write(buf)
                f.close()

            except Exception as e:
                print(e)
            # print(tys[i], 'has been downloaded.')


def rename(fname):  # there maybe some unexpected char in fname, drop them

    new_fname = fname.replace('[', '')
    new_fname = new_fname.replace(']', '')
    new_fname = new_fname.replace('u', '')
    new_fname = new_fname.replace('\'', '')
    return new_fname


class MyThread(threading.Thread):
    def __init__(self, path_, thread_id, start_year, end_year):
        threading.Thread.__init__(self)
        self.path_ = path_
        self.thread_id = thread_id
        self.start_year = start_year
        self.end_year = end_year

    def run(self):
        print("Thread starts: " + self.name)
        ts, links = get_ty_links(self.start_year, self.end_year)
        download_imgs(self.path_, ts, links)
        print("Thread exits: " + self.name)


def create_threads(path_, start_year, end_year, thread_count=20):
    time_span = end_year - start_year + 1
    st_et = []
    # thread=[]
    thread_year = int(time_span / thread_count)
    if thread_year == 1:
        thread_count = time_span
    for i in range(thread_count):
        if i != thread_count - 1:
            st_et.append((start_year + i * thread_year, start_year + (i + 1) * thread_year))
        else:
            st_et.append((start_year + i * thread_year, end_year + 1))
    print(st_et)
    for i in range(len(st_et)):
        # thread.append(MyThread(i,st_et[i][0],st_et[i][1]).start())
        MyThread(path_, i, st_et[i][0], st_et[i][1]).start()
    # for j in thread:
    #     j.join()


def download_agora(path_):
    create_threads(path_, 1979, 2019, 20)
