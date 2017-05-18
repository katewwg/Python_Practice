import requests
import time
from bs4 import BeautifulSoup

header = {
'Cookie':'bid=1e6_skQiWXw; gr_user_id=06036372-521a-4a6a-98f6-8b0e1db0ce2d; __yadk_uid=Xh1hxyDFIeuoWh3pUFPiBMAgw7rnFyC2; ll="108288"; _pk_ref.100001.3ac3=%5B%22%22%2C%22%22%2C1494213088%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D; viewed="4812810_26253304_26667778_25910544_1809089_3227098_2311306_2362464_6801878_1102259"; gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03=a341c5df-b2e6-47f3-9bfb-c3a5f4aecb66; gr_cs1_a341c5df-b2e6-47f3-9bfb-c3a5f4aecb66=user_id%3A0; _vwo_uuid_v2=93D3501F80D98E877760DB0565FF6E95|2e0cb87346382c7fe0903fbc38373442; __utmt_douban=1; __utmt=1; ps=y; ue="18001229080@163.com"; dbcl2="123001451:TWDc55TDKvg"; ck=gt7i; push_noty_num=0; push_doumail_num=0; _pk_id.100001.3ac3=206b15d98fc0d755.1493791922.10.1494215001.1494211059.; _pk_ses.100001.3ac3=*; __utma=30149280.937714620.1493711796.1494210507.1494213089.11; __utmb=30149280.49.10.1494213089; __utmc=30149280; __utmz=30149280.1494210507.10.10.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utma=81379588.388495411.1493791922.1494210513.1494213089.10; __utmb=81379588.77.9.1494214306321; __utmc=81379588; __utmz=81379588.1494210513.9.9.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/'
}
paramters = {'start':0,'type':'T'}

def get_cont(url,paramters):
    cont = requests.get(url,params=paramters,headers = header)
    cont_bsobj = BeautifulSoup(cont.text,'html.parser')
    return cont_bsobj

def get_title(url,paramters):
    title_list = []
    cont_bsobj = get_cont(url,paramters)
    subject_item = cont_bsobj.find_all('li', {'class': 'subject-item'})
    for i in subject_item:
        item_title = i.find('h2').a['title']
        title_list.append(item_title)
    return title_list

def get_star(url,paramters):
    star_list = []
    cont_bsobj = get_cont(url, paramters)
    rating_nums = cont_bsobj.find_all('span',{'class':'rating_nums'})
    for i in rating_nums:
        try:
            star_list.append(float(i.text))
        except:
            star_list.append(0)
    return star_list

def get_pl(url,paramters):
    pl_list = []
    cont_bsobj = get_cont(url, paramters)
    pl = cont_bsobj.find_all('span',{'class':'pl'})
    for i in pl:
        try:
            pl_numbers = int(i.text.strip()[1:-4])
            pl_list.append(pl_numbers)
        except:
            pl_numbers = 0
            pl_list.append(pl_numbers)
    return pl_list

def get_book_url(url,paramters):
    url_list = []
    cont_bsobj = get_cont(url, paramters)
    book_url_obj =cont_bsobj.find_all('a',{'class':'nbg'})
    for i in book_url_obj:
            book_url = i['href']
            url_list.append(book_url)
    return url_list

def get_book_details(url,paramters):
    book_dict = {}
    title_list = get_title(url,paramters)
    star_list = get_star(url, paramters)
    pl_list = get_pl(url, paramters)
    url_list = get_book_url(url, paramters)
    for i in range(15):
        book_details = {}
        if pl_list[i] == 0:
            star_list.insert(i,0)
        book_details['star'] = star_list[i]
        book_details['pl'] = pl_list[i]
        book_details['url'] = url_list[i]
        book_dict[title_list[i]] = book_details
    return book_dict

def construct_paramters(index):
    index = index * 20
    paramters = {'start': index, 'type': 'T'}
    return paramters

def book_type_getall(url,page_number):
    book_dict_all = {}
    for i in range(0,page_number):
        book_dict_all.update(get_book_details(url,paramters=construct_paramters(i)))
        time.sleep(.5)
        print('正在爬取第{}页'.format(i))
    return book_dict_all


if __name__ == '__main__':
    print(get_book_url('https://book.douban.com/tag/Python',construct_paramters(1)))
