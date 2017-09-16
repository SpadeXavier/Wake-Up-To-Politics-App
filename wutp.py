#!/usr/bin/env python 

from urllib.request import urlopen as uReq 
from bs4 import BeautifulSoup as soup
from collections import OrderedDict

class Wutp():

    def __init__(self, url):
        
        self.url = url 
        
        uClient = uReq(url)
        html = uClient.read() 
        uClient.close() 

        self.parsed = soup(html, "html.parser") 

    def convert(self, string):
        string = string.replace('\n', '').replace(u'\xa0', ' ')
        string = string.encode('ascii', 'ignore').decode('utf-8')
        return string

    def traverse(self):
        """ traverses a page and returns an ordered dict of headings as keys
        and corresponding points as values """  

        content = self.parsed.findAll("table", {"class": 'mcnTextContentContainer'})
        
        news = OrderedDict() 
        heading_list = []   # keeps tracks of added headings
        point_list = []     # keeps track of added points
        points = False      # keeps track of if a point or a heading
        current_heading = ''

        for index,c in enumerate(content):
            if points:
                all_points = c.findAll('li')

                # -- if there are lists use the text of lists
                if len(all_points) > 0:
                    for each_point in all_points:
                        nested_points = each_point.findAll('li') 
                        # -- if there are nested lists get only the first span
                        # tag because the loop will grab the texts of the
                        # other lists later on 
                        if len(nested_points) > 0:
                            first_tag = each_point.find('span') 
                            point_list.append(first_tag.text)
                            news[current_heading].append(self.convert(first_tag.text))
                        # -- if no nested list just grab the text of the list 
                        else:
                            point_list.append(each_point.text) 
                            news[current_heading].append(self.convert(each_point.text))

                # -- if no lists but still after a heading, then just grab the text 
                else:
                    if c.text not in point_list:
                        point_list.append(c.text) 
                        news[current_heading].append(self.convert(c.text))

            # -- if it's a heading add it under headings 
            if c['cellpadding'] == '18':
                if c.text not in heading_list:
                    heading_list.append(c.text)
                    current_heading = self.convert(c.text)
                    news[current_heading] = [] 
                # -- next iteration will be points
                points = True        
          
            # -- need try and except for index out of range error 
            try:
                if content[index+1]['cellpadding'] == '18':
                    # -- next iteration will be a heading
                    points = False
            except:
                pass
       
        # -- remove last item which is copyright footer 
        news.popitem()

        self.news = news
        
        return news

    def get_headings(self):
        """ returns an array of the headings in the page """ 
        return [key for key in self.news] 

    def get_points(self):
        ''' returns a two dimensional array with points of a heading at each
        index''' 

        return [v for key,v in self.news.items()]  

    
    @staticmethod
    def get_urls():
        """ returns a dictionary of issues with url title as key and url target
        as value """ 

        urls = {} 

        base_url = 'http://us3.campaign-archive2.com/home/?u=4946817b18454973fb1cd7ecc&id=e81d77774f'

        uClient = uReq(base_url) 
        html = uClient.read() 
        uClient.close() 

        archive_parsed = soup(html, "html.parser") 

        all_lists = archive_parsed.findAll('li') 

        for each_list in all_lists:
            link = each_list.find('a') 
            link_target = link['href']
            urls[link.text]=link_target

        return urls

    @staticmethod
    def get_ordered_urls():
        """ returns an array of urls in order of date """
        urls = [] 

        base_url = 'http://us3.campaign-archive2.com/home/?u=4946817b18454973fb1cd7ecc&id=e81d77774f'

        uClient = uReq(base_url) 
        html = uClient.read() 
        uClient.close() 

        archive_parsed = soup(html, "html.parser") 
        
        all_lists = archive_parsed.findAll('li') 

        for each_list in all_lists:
            link = each_list.find('a') 
            link_target = link['href']
            urls.append(link_target) 

        return urls

    @staticmethod
    def get_dates():
        """ returns an array of dates of published issues from newest to oldest
        """
        dates = []
        
        base_url = 'http://us3.campaign-archive2.com/home/?u=4946817b18454973fb1cd7ecc&id=e81d77774f'

        uClient = uReq(base_url) 
        html = uClient.read() 
        uClient.close() 

        archive_parsed = soup(html, "html.parser") 

        all_lists = archive_parsed.findAll('li')
        
        for each_list in all_lists:
            unformatted = each_list.text
            date = unformatted.split(' ')[0]
            dates.append(date) 
        
        return dates


if __name__ == '__main__':
    url = 'http://us3.campaign-archive2.com/?u=4946817b18454973fb1cd7ecc&id=091f19cbd4'
    wutp = Wutp(url)
    wutp.traverse()  

    print('------------------ HEADINGS ----------------------')
    print(wutp.get_headings()) 
    print('------------------ POINTS ------------------------') 
    print(wutp.get_points())
    # print('------------------- CONTENT ----------------------') 
    # print(wutp.get_content())
    # print('------------------- URLS -------------------------') 
    # print(Wutp.get_urls())
    # print('-------------------- DATES ------------------------') 
    # print(Wutp.get_dates()) 







































































































