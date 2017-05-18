# coding=utf-8
from pandas import DataFrame
from douban_crawler import book_type_getall
from douban_crawler import get_title,paramters

# 得到一个Python字典
def book_sortby(keywords,number):
    dataframe_sorted = DataFrame(Python_book).T.sort_values(by=keywords,ascending=False)
    return dataframe_sorted[number:number+50][keywords]


if __name__ == '__main__':
    # print('请输入你想要抓取的标签名称')
    # Tag = input()
    #Python_book = book_type_getall('https://book.douban.com/tag/' + Tag, 10)
    #dataframe = DataFrame(Python_book).T
    # dataframe.to_excel('{}.xlsx'.format(Tag),sheet_name='1')
    for i in get_title('https://book.douban.com/tag/奇书',paramters):
        print('正在爬取 {}'.format(i))