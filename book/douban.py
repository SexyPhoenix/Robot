# -*- coding: utf-8 -*-
# @Author: Sexy Phoenix
# @Date:   2019-10-23 11:01:08
# @Last Modified by:   Sexy Phoenix
# @Last Modified time: 2019-10-24 11:08:58
import requests
from bs4 import BeautifulSoup, SoupStrainer

#内容解析类
class Parse:

    #解析分类
    def parse_tags(self, content):

        only_div_tags = SoupStrainer('div', 'article')
        soup = BeautifulSoup(content, 'lxml', parse_only=only_div_tags)

        category = {}
        sub_category = {}

        # 解析大分类
        tag_title_wrapper = soup.find_all('a', 'tag-title-wrapper')

        for index,tag in enumerate(tag_title_wrapper):
            category[index] = tag.get('name')

        # 解析大分类下的具体分类
        tagCol = soup.find_all('table', "tagCol")
        for i,tag in enumerate(soup.find_all('table', "tagCol")):
            a = tag.find_all('a')
            sub_category[i] = []
            for t in a:
                sub_category[i].append(t.string)

        return category, sub_category

    #解析具体分类前20分书籍
    def parse_detail_tag(self, content):

        detail_conent = []
        only_ul_tags = SoupStrainer('ul', 'subject-list')
        soup = BeautifulSoup(content, 'lxml', parse_only=only_ul_tags)

        for li in soup.find_all('li', 'subject-item'):

            info = li.find('div', 'info')
            title = info.h2.a.get('title')
            star = info.find('span', 'rating_nums')
            extra_info = info.h2.next_sibling.next_sibling.string.split('/')
            author = extra_info[0].strip()
            price = extra_info[-1].strip()
            appraise = star.string
            appraise_num = star.next_sibling.next_sibling.string.strip()

            detail_conent.append({
                'title': title,
                'price': price,
                'author': author,
                'appraise':appraise,
                'appraise_num': appraise_num
            })

        return detail_conent

#内容获取类
class Spider:

    def __init__(self):

        self.url = 'https://book.douban.com/tag/?view=type&icn=index-sorttags-all'
        self.tag_url = 'https://book.douban.com/tag/'
        self.headers = {
            'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
        }
        self.parse = Parse()

    #获取分类HTML内容
    def get_all_tag(self):

        data = requests.get(self.url, headers=self.headers)
        if(data.status_code == requests.codes.ok):
            return self.parse.parse_tags(data.text)
        else:
            print('[ERROR]: GET Category Error')

    #获取书籍HTML内容
    def get_detail_tag(self, tag_name):
        data = requests.get(self.tag_url + tag_name, self.headers)
        if(data.status_code == requests.codes.ok):
            return self.parse.parse_detail_tag(data.text)
        else:
            print('[ERROR]: GET Sub Category Error')

    #显示
    def show(self):

        category, sub_category = self.get_all_tag()
        print('豆瓣大分类：')
        for index,value in category.items():
            i = index + 1
            print("{0}、{1}".format(i, value))
        try:
            key = int(input('请输入您选择的大分类：')) - 1
            sub_cate = sub_category[key]
            for index in range(len(sub_cate)):
                i = index + 1
                print("{0}、{1}".format(i, sub_cate[index]))
            try:
                sub_key  = int(input('请输入您选择的具体分类：')) - 1
                tag_name = sub_cate[sub_key]
                detail_content = self.get_detail_tag(tag_name)

                for book in detail_content:
                    print('\n')
                    print(book['title'])
                    print("作者：{0}, 价格：{1}, 评分：{2}{3}".format(book['author'],book['price'], book['appraise'], book['appraise_num']))
                    print('='*50)

            except:
                print('[ERROR]: 具体分类选择错误')
        except:
            print('[ERROR]: 大分类选择错误')

#入口
if __name__ == '__main__':
    spider = Spider()
    spider.show()

