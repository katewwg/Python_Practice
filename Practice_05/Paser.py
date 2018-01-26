#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/1/26 上午10:43
# @Author  : Allen Wang
# @File    : Paser.py

import requests
from soccer_team_crawler import start_page_headers
from lxml import etree

test_url = 'http://data.nowgoal.cc/OddsComp/817495.html'
data = requests.get(test_url, headers=start_page_headers)
html = etree.HTML(data.text)
tr_node = html.xpath('//tr[@class="b1"]')[0]
company = tr_node.xpath('child::td')
for i in company:
    if i.text:
        print(i.text)
    for c in i.xpath('child::*'):
        if c.text:
            print(c.text)