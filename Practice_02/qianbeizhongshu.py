import requests
import time
from bs4 import BeautifulSoup
from pandas import DataFrame

url = 'http://weixin.sogou.com/weixin'
header = {'Cookie' : 'SUV=007D55426A25FCC659083235AF363015; CXID=94FE22558AD3FBFFD0B05B4A12856FD4; ad=s2Rpylllll2BRlZDlllllV6S0jGlllllzAgDekllllyllllljv7ll5@@@@@@@@@@; SUID=C6FC256A2A0B940A0000000059083235; ld=qkllllllll2BjRwClllllV6q41tlllllzAgDekllll9lllllRj7ll5@@@@@@@@@@; ABTEST=0|1494919910|v1; SNUID=5A60BEF19B9ED304B6A65A0D9CE4C2A5; weixinIndexVisited=1; sct=2; IPLOC=CN; JSESSIONID=aaapW3SWhMUrb7FrNX2Vv; ppinf=5|1494919943|1496129543|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZToyNzolRTglQjQlOUQlRTclOEUlODklRTUlQjAlOUF8Y3J0OjEwOjE0OTQ5MTk5NDN8cmVmbmljazoyNzolRTglQjQlOUQlRTclOEUlODklRTUlQjAlOUF8dXNlcmlkOjQ0Om85dDJsdU1BYXg2VVlIcWFOUGE5OE9DS09nS29Ad2VpeGluLnNvaHUuY29tfA; pprdig=q3da2ejqgZVzRhXDwFkpMdDETZZlOplPi_CV8nHYnWS2x9frCt09PF57_4D2vmsuTJp3CN2U7gLgwlL8CCvkdc54XHaYvUibU000lbItAkXtFdHgbAaTHdBpPQyEJ84veFQ5Cvuj2ZHnJ65LpEy8XdJj_jVWqDVJL6PXtk5efZo; sgid=; ppmdig=14949199430000005fbabebf2e42cdf6950bd188bc502a8b'}
params = {
'query':'前辈种树',
'sut':'1952',
'lkt':'1,1494919787254,1494919787254',
's_from':'input',
'_sug_':'n',
'type':2,
'sst0':1494919787366,
'page':3,
'ie':'utf8',
'w':'01019900',
'dr':1,
}

def get_link_list(bsobj):
    dict_detail = {}
    link_bsobj = bsobj.find_all('a',{'target':'_blank'})
    count = 0
    for link in link_bsobj[7:-3]:
        title = link.text
        if '前辈种树' in title:
            link_dict = {}
            count += 1
            href = link['href']
            link_dict['href'] = href
            bsobj_href = BeautifulSoup(requests.get(href).text,"html5lib").find_all('em',{'class':"rich_media_meta rich_media_meta_text"})
            author_list = []
            for i in bsobj_href:
                author_list.append(i.text)
            link_dict['date'] = author_list[0]
            try:
                link_dict['author'] = author_list[1]
            except:
                link_dict['author'] = None
            dict_detail[title] = link_dict
            print('正在爬取{}{}'.format(count, title))
            time.sleep(1)
    return dict_detail

def get_author(url):
    author_list = []
    cont = requests.get(url).text
    bsobj = BeautifulSoup(cont,"html5lib")
    for i in bsobj.find_all('em',{'class':"rich_media_meta rich_media_meta_text"}):
        author_list.append(i.text)
    return author_list

dict_all = {}
for i in range(25,30):
    params['page'] = i
    cont = requests.get(url,params=params,headers = header).text
    bsobj = BeautifulSoup(cont,"html5lib")
    dict = get_link_list(bsobj)
    time.sleep(5)
    dict_all.update(dict)

dataframe = DataFrame(dict_all).T
dataframe.to_excel('{}.xlsx'.format('前辈种树20-30'),sheet_name='1')