
# coding: utf-8
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
from splinter import Browser
from selenium import webdriver

def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)


def scrape():
      
    browser = init_browser()
    mars_data = {}

    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    html = browser.html
    soup = bs(html, 'html.parser')

    news_title = soup.find('div', class_='content_title').text
    news_body = soup.find('div', class_='article_teaser_body').text

    mars_data["news_title"] = news_title
    mars_data["news_body"] = news_body

    url_1 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url_1)
    
    image_html = browser.html
    soup = bs(image_html,'html.parser')

    image_url = soup.find('a', class_='button fancybox')['data-fancybox-href']

    base_url = 'https://www.jpl.nasa.gov'

    featured_image_url = f"{base_url}{image_url}"

    mars_data["featured_image_url"] = featured_image_url
   
    url_2 = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url_2)

    html = browser.html
    soup = bs(html, 'html.parser')

    mars_weather = soup.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text
    
    mars_data["mars_weather"] = mars_weather

    url_3 = 'http://space-facts.com/mars/'

    mars_table = pd.read_html(url_3)
    
    df = mars_table[0]
    df.columns = ['Characteristics','Mars Info']
    df.set_index('Characteristics', inplace=True)
    
    mars_table = df.to_html()
    mars_table = mars_table.replace('\n', '')
    mars_data["mars_table"] = mars_table

    
   
    url_4 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url_4)

    first = browser.find_by_tag('h3')[0].text
    second = browser.find_by_tag('h3')[1].text
    third = browser.find_by_tag('h3')[2].text
    fourth = browser.find_by_tag('h3')[3].text

    browser.find_by_css('.thumb')[0].click()
    first_img = browser.find_by_text('Sample')['href']
    browser.back()

    browser.find_by_css('.thumb')[1].click()
    second_img = browser.find_by_text('Sample')['href']
    browser.back()

    browser.find_by_css('.thumb')[2].click()
    third_img = browser.find_by_text('Sample')['href']
    browser.back()

    browser.find_by_css('.thumb')[3].click()
    fourth_img = browser.find_by_text('Sample')['href']

    hemisphere_image_urls = [
        {'title': first, 'img_url': first_img},
        {'title': second, 'img_url': second_img},
        {'title': third, 'img_url': third_img},
        {'title': fourth, 'img_url': fourth_img}
    ]
    mars_data ["hemisphere_image_urls"] = hemisphere_image_urls
    return mars_data


