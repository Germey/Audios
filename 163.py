from multiprocessing import Process
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time
from os.path import exists
from os import makedirs
from redis import StrictRedis
from selenium.common.exceptions import WebDriverException

db = StrictRedis(host='localhost', port=6379, db=0, password='foobared', decode_responses=True)

urls = [
    'http://music.163.com/#/djradio?id=350234234',
    'http://music.163.com/#/djradio?id=350234234',
    'http://music.163.com/#/djradio?id=6779005',
    'http://music.163.com/#/djradio?id=350589167',
    'http://music.163.com/#/djradio?id=7375084',
    'http://music.163.com/#/djradio?id=349374451',
    'http://music.163.com/#/djradio?id=350325839',
    'http://music.163.com/#/djradio?id=337676057',
    'http://music.163.com/#/djradio?id=349629091',
    'http://music.163.com/#/djradio?id=349977940',
    'http://music.163.com/#/djradio?id=346216051',
    'http://music.163.com/#/djradio?id=333635084',
    'http://music.163.com/#/djradio?id=334635050',
    'http://music.163.com/#/djradio?id=344503082',
    'http://music.163.com/#/djradio?id=1116004',
    'http://music.163.com/#/djradio?id=349593302',
    'http://music.163.com/#/djradio?id=349079050',
    'http://music.163.com/#/user/home?id=273682588',
    'http://music.163.com/#/djradio?id=338771052',
    'http://music.163.com/#/djradio?id=345598058',
    'http://music.163.com/#/djradio?id=350158577',
    'http://music.163.com/#/djradio?id=334290084',
    'http://music.163.com/#/djradio?id=350304168',
    'http://music.163.com/#/djradio?id=1208050',
    'http://music.163.com/#/djradio?id=333626055',
    'http://music.163.com/#/djradio?id=337824096',
    'http://music.163.com/#/djradio?id=336383090',
    'http://music.163.com/#/djradio?id=389046',
    'http://music.163.com/#/djradio?id=349665868',
    'http://music.163.com/#/djradio?id=347519326',
    'http://music.163.com/#/djradio?id=345140065',
    'http://music.163.com/#/djradio?id=6581008',
]


def response(flow):
    url = '.mp3'
    if url in flow.request.url:
        url = flow.request.url
        website = '网易云电台'
        
        path = '{website}/{album}'.format(website=website, album=db.get('album'))
        file = '{website}/{album}/{title}.mp3'.format(website=website,
                                                      album=db.get('album'), title=db.get('title'))
        if not exists(path):
            makedirs(path)
        print('Saving', url)
        content = requests.get(url).content
        with open(file, 'wb') as f:
            f.write(content)


def crawl():
    from selenium import webdriver
    proxy = '127.0.0.1:8080'
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--proxy-server=http://' + proxy)
    browser = webdriver.Chrome(chrome_options=chrome_options)
    wait = WebDriverWait(browser, 10)
    for url in urls:
        try:
            browser.get(url)
            browser.switch_to.frame('g_iframe')
            db.set('album', wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.tit .f-ff2'))).text)
            elements = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'j-tr')))
            for element in elements:
                y = element.location['y']
                js = 'var q = document.documentElement.scrollTop=' + str(y)
                print(js)
                browser.execute_script(js)
                db.set('title', element.find_element_by_css_selector('td.col2 > .tt > a').text)
                play = element.find_element_by_class_name('ply')
                print(db.get('album'), db.get('title'), play)
                play.click()
                time.sleep(5)
        except WebDriverException:
            pass
    
    browser.close()


process = Process(target=crawl)
process.start()
