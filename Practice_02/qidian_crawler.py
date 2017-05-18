import re
import requests
from bs4 import BeautifulSoup
from collections import namedtuple
from pandas import DataFrame
import time

paramters = {
    'kw':'玄幻',
    'page':2
}
url = 'http://se.qidian.com/'

request = requests.get(url,params=paramters)
html_cont = request.text
bsobj = BeautifulSoup(html_cont,"html5lib")
mid_info = bsobj.find_all('div',{'class':"book-mid-info"})
right_info = bsobj.find_all('div',{'class':"book-right-info"})


def get_book_link(mid_info):
    book_link = []
    for url in mid_info:
        book_link.append(url.h4.a['href'])
    return book_link

def get_book_title(mid_info):
    book_title = []
    for title in mid_info:
        book_title.append(title.h4.text)
    return book_title

def get_book_author(mid_info):
    book_author = []
    for author in mid_info:
        book_author.append(author.find('a',{'class':'name'}).text)
    return book_author

def get_book_intro(mid_info):
    book_intro = []
    for intro in mid_info:
        book_intro.append(intro.find('p',{'class':'intro'}).getText().strip())
    return book_intro

def get_number(string):
    p = re.compile(r'\d*\.?\d+')
    if '万' in string:
        number = float(p.findall(string)[0])*10000
        return number
    else:
        number = int(p.findall(string)[0])
        return number

def get_book_total(right_info):
    book_total = []
    total_tuple = namedtuple('total_tuple', ['总字数', '总推荐', '总点击'])
    for i in right_info:
        span_list = i.find('div', {'class': 'total'}).find_all('span')
        tuple01 = total_tuple(get_number(span_list[0].getText()),get_number(span_list[1].getText()),get_number(span_list[2].getText()))
        book_total.append(tuple01)
    return book_total

def creat_book_detail_dict(kw,pages):
    paramters = {
        'kw': kw,
        'page': pages
    }
    url = 'http://se.qidian.com/'
    index = -1
    book_detail_dict = {}
    request = requests.get(url, params=paramters)
    html_cont = request.text
    bsobj = BeautifulSoup(html_cont, "html5lib")
    mid_info = bsobj.find_all('div', {'class': "book-mid-info"})
    right_info = bsobj.find_all('div', {'class': "book-right-info"})
    link_list = get_book_link(mid_info)
    title_list = get_book_title(mid_info)
    author_list = get_book_author(mid_info)
    intro_list = get_book_intro(mid_info)
    total_list = get_book_total(right_info)
    for i in range(len(title_list)):
        dict_book = {}
        index += 1
        index_book = '{}.{}'.format(pages,index)
        dict_book['title'] =  title_list[i]
        dict_book['intro'] = intro_list[i]
        dict_book['author'] = author_list[i]
        dict_book['link'] = link_list[i]
        dict_book['总字数'] = total_list[i].总字数
        dict_book['总推荐'] = total_list[i].总推荐
        dict_book['总点击'] = total_list[i].总点击
        book_detail_dict[index_book] = dict_book
    return book_detail_dict

if __name__ == '__main__':
    dict_1_10 = {}
    kw = '玄幻'
    for i in range(1,10):
        dict_1_10.update(creat_book_detail_dict(kw,i))
        print('抓取第{}页'.format(i))
        time.sleep(5)
    data = DataFrame(dict_1_10).T
    data.to_excel('qidian_{}.xlsx'.format(kw), sheet_name='书籍信息')