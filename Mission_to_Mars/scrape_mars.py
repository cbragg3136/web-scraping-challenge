# import dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": './chromedriver'}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()

#NASA Mars News

    #Visit mars.nasa.gov/news
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    #Scrape page into Soup
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    #Get title and paragraph of latest news article
    news_title = soup.find('div', class_='list_text').find('div', class_='content_title').text
    news_p = soup.find('div', class_='article_teaser_body').text

#JPL Mars Space Images
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Click links to retrieve html of large image
    browser.links.find_by_partial_text('FULL IMAGE').click()
    browser.links.find_by_partial_text('more info').click()

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Find the image url for the current Featured Mars Image and assign the url string
    url = soup.find('figure', class_='lede').find('a')['href']
    featured_image_url = 'https://www.jpl.nasa.gov' + url
    featured_image_url

#Mars Facts
    # Use Pandas to scrape the table of mars facts
    url = 'https://space-facts.com/mars/'
    table = pd.read_html(url)[0]
    table.columns=["Description", "Mars"]
    mars_facts = table.set_index('Description')
    mars_table = mars_facts.to_html()

#Mars Hemispheres
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Scrape and List the names of the 4 hemispheres
    title = soup.find_all('h3')
    hemispheres = [x.text.split(' Enhanced')[0] for x in title]

    hemisphere_image_urls = []

    for hemisphere in hemispheres:
        hem_dict = {}
    # Click each of the links to the hemispheres in order to find the image url to the full resolution image
        browser.links.find_by_partial_text(hemisphere).click()

        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')

    # Save image url string and the Hemisphere title containing the hemisphere name in a Python dictionary
        hem_dict['title'] = soup.find('h2', class_='title').text.replace("Enhanced","").strip()
        hem_dict['img_url'] = soup.find('div', class_='downloads').find('a')['href']
        hemisphere_image_urls.append(hem_dict)
        
        browser.back()

        
    hemisphere_image_urls

    browser.quit()

    # Store all the scraped data in a dictionary
    mars_data = {
        'news_title': news_title,
        'news_p': news_p,
        'featured_image_url': featured_image_url,
        'mars_table': mars_table,
        'hemisphere_image_urls' : hemisphere_image_urls,

    }

    return mars_data