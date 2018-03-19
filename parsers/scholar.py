import requests
from bs4 import BeautifulSoup
from time import sleep
import os, sys


base_dir = None
base_url = 'https://scholar.google.ru/scholar'


def get_urls(html):
    soup = BeautifulSoup(html, 'lxml')
    resourses = soup.find('div', id='gs_res_ccl_mid').find_all('div', class_='gs_r gs_or gs_scl')
    name_urls = []
    for res in resourses:
        try:
            url = res.find('div', class_='gs_ggs gs_fl').find('a').get('href')
            name = res.find('div', class_='gs_ri').find('h3', class_='gs_rt').find('a').text
            if 'cyberleninka' not in url:
                name_urls.append((name, url))
        except:
            continue
    return name_urls

def download_file(name, url):
    sleep(1)
    try:
        r = requests.get(url, stream=True)
        # except:
        #     print('Scholar:', name, 'is not download')
        #     return 0
        postfix = url.split('.')[-1]
        if '#' in postfix:
            return 0
        if '/' in postfix:
            postfix = 'html'
        file_name = name.lower() + '.' + postfix
        print('Scholar: начинаю загрузку:', file_name)
        if file_name not in os.listdir(base_dir):
            with open(base_dir + '/' + file_name, 'wb') as file:
                for chunk in r.iter_content(4096):
                    file.write(chunk)
            print('Scholar:', file_name, 'загружен')
        else:
            print('Scholar: файл уже существует')
    except:
        print('Scholar: ошибка загрузки')

def scholar(b_dir, author='', title='', keywords='', year1='', year2=''):
    global base_dir
    base_dir= b_dir
    #sys.stdout = open('/'.join(base_dir.split('/')[:2]) + '/' + 'log_scholar.txt', 'a', encoding='utf-8')
    print('Scholar: начал работу')
    query = {
        'allintitle': '"' + title + '"',
        'author': '"' + author + '"',
    }
    params = {
        'q': keywords + ' ' + ' '.join([k+':'+v for k, v in query.items() if v[1:-1]]),
        'as_vis': 1,   # без цитат
        'as_ylo': year1, # год 1
        'as_yhi': year2, # год 2
        'hl': 'ru',
        'start': 0,  # страницы 10 20 ...80
    }
    while params['start'] <= 60:
        sleep(2)
        try:
            r = requests.get(base_url, params=params)
        except:
            print('Scholar: проверьте соединение с сетью')
            break
        print('Socholar: запрос:', r.url)
        html = r.text
        name_urls = get_urls(html)
        if name_urls:
            for name, url in name_urls:
                download_file(name, url)
        else:
            print('Scholar: загрузка завершена')
            break
        params['start'] += 10

if __name__ == '__main__':
    scholar('test')