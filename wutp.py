#!/usr/bin/env python 

from urllib.request import urlopen as uReq 
from bs4 import BeautifulSoup as soup

class Wutp():

    def __init__(self, url):
        
        self.url = url 
        
        uClient = uReq(url)
        html = uClient.read() 
        uClient.close() 

        self.parsed = soup(html, "html.parser") 

    def convert(self, string):
        return string.encode('ascii', 'ignore').decode('utf-8') 


    def get_headings(self):
        """ returns an array of the headings in the page """ 
        headings = self.parsed.findAll("table", {"class":"mcnBoxedTextContentContainer"})
        heading_array = []
        for heading in headings:
            try:
                heading_text = heading.find('strong').text
                heading_text = self.convert(heading_text)
                heading_array.append(heading_text)
            except:
                pass
        return heading_array 

    def get_points(self):
        ''' returns a two dimensional array with points of a heading at each
        index''' 

        points_array = []  
        curr_points = []

        bodies = self.parsed.findAll('td', {"class": 'mcnTextContent'})

        for body in bodies:
            points = body.findAll('li')

            # skip if no lists 
            if len(points) == 0:
                continue 

            for point in points:
                point_text = point.text 
                point_text = point_text.replace(u'\xa0', ' ')
                point_text = self.convert(point_text)
                curr_points.append(point_text)            

            points_array.append(curr_points)
            curr_points = []

        return points_array

    def get_content(self):
        """ returns a dictionary with headings as key and the corresponding
        points as an array value """
        
        content = {}

        headings = self.get_headings() 
        points = self.get_points() 

        for heading, point_container in zip(headings,points):
            content[heading] = point_container

        return content

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
    url = 'http://mailchi.mp/wakeuptopolitics/091317?e=58381c74c0'
    wutp = Wutp(url)
    print('------------------ HEADINGS ----------------------')
    print(wutp.get_headings()) 
    # print('------------------ POINTS ------------------------') 
    # print(wutp.get_points())
    print('------------------- CONTENT ----------------------') 
    print(wutp.get_content())
    print('------------------- URLS -------------------------') 
    print(Wutp.get_urls())
    print('-------------------- DATES ------------------------') 
    print(Wutp.get_dates()) 







































































































