from bs4 import BeautifulSoup
import requests
import pandas as pd
import json


def scrape():
    listings = {}
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    # 1.NASA Mars News
    url_news = 'https://mars.nasa.gov/api/v1/news_items/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    resp_1 = requests.get(url_news).json()
    listings["news_title"] = resp_1.get('items')[0].get('title')
    listings["news_p"] = resp_1.get('items')[0].get('description')

    # 2. JPL Mars Space Images - Featured Image
    url_image = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    resp_2 = requests.get(url_image,headers = headers)
    soup = BeautifulSoup(resp_2.content,'html.parser')
    listings["featured_image_url"] = 'https://www.jpl.nasa.gov' \
                                    + soup.find('a',{'class':"button fancybox"}).attrs.get('data-fancybox-href')
    
    # 3. Mars Weather
    url_weather='https://twitter.com/marswxreport?lang=en'
    resp_3 = requests.get(url_weather,headers = headers)
    soup = BeautifulSoup(resp_3.content,'html.parser')
    listings["mars_weather"] = soup.find('p',{"class":"TweetTextSize TweetTextSize--normal js-tweet-text tweet-text"})\
                                .get_text()[:-26]
    
    # 4. Mars Facts
    df = pd.read_html('https://space-facts.com/mars/')
    Mars_Facts = df[0]
    Mars_Facts.columns = ['profile','value']
    Mars_Facts.set_index('profile')
    listings['Mars_facts_table'] = Mars_Facts.to_html()

    # 5. Mars Hemispheres
    url_hemispheres = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    resp_5 = requests.get(url_hemispheres,headers = headers)
    soup = BeautifulSoup(resp_5.content,'html.parser')

    result = soup.find_all('h3')
    hemisphere_image_names = [x.get_text() for x in result]
    listings["hemisphere_image_names"] = hemisphere_image_names

    soup_objects = soup.find_all('a',{'class':"itemLink product-item"})
    links = ['https://astrogeology.usgs.gov' + x.attrs.get('href') for x in soup_objects]

    def get_high_res_image(link):
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        resp_6 = requests.get(link,headers = headers)
        soup = BeautifulSoup(resp_6.content,'html.parser')
        hemisphere_image_url = soup.find('a',{'target':"_blank"}).attrs.get('href')
        return hemisphere_image_url
    
    hemisphere_image_urls = []
    for l in links:
        hemisphere_image_urls.append(get_high_res_image(l))

    listings['hemisphere_image_urls'] = hemisphere_image_urls


    return listings
