from bs4 import BeautifulSoup
import requests
from splinter import Browser
import pandas as pd

def init_browser():
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()
    mars_data = {}

    # NASA Mars News
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    news_title = soup.find("div", class_="content_title").text
    news_p = soup.find("div", class_="article_teaser_body").text

    mars_data["news_title"] = news_title
    mars_data["news_paragraph"] = news_p

    # JPL Mars Space Images - Featured Image
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    image = soup.find("article", class_="carousel_item")["style"]
    image_url = image[image.find("('")+2:image.find("')")]
    base_url = "https://www.jpl.nasa.gov"
    featured_image_url = base_url + image_url

    mars_data["featured_image"] = featured_image_url

    # Mars Weather
    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    mars_weather = soup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text

    mars_data["mars_weather"] = mars_weather

    # Mars Facts
    url = "https://space-facts.com/mars/"
    browser.visit(url)
    table = pd.read_html(url)
    df = table[0]
    df = df.rename(columns={df.columns[0]:"Fact",df.columns[1]:"Data"})
    df = df.set_index("Fact")
    html_table = df.to_html()

    mars_data["mars_facts"] = html_table

    # Mars Hemispheres
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    base_url = "https://astrogeology.usgs.gov"
    hemisphere_image_urls = []
    for x in range(0,4):
        link = browser.find_by_tag("h3")[x]
        link.click()
        html = browser.html
        soup = BeautifulSoup(html, "html.parser")
        title = soup.find("h2", class_="title").text
        link = soup.find("img", class_="wide-image")["src"]
        img_link = base_url + link
        title_and_url = {"Title" : title,"img_url" : img_link}
        hemisphere_image_urls.append(title_and_url)
        browser.back()
    
    mars_data["mars_hemispheres"] = hemisphere_image_urls


    return mars_data
