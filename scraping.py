# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt


def scrape_all():
    # Splinter & Executable Path Set Up
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless = True)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in dictionary
    data = {
      "news_title": news_title,
      "news_paragraph": news_paragraph,
      "featured_image": featured_image(browser),
      "facts": mars_facts(),
      "hemispheres" : hemispheres(browser),
      "last_modified": dt.datetime.now()
    }

    # Stop webdriver and return data
    browser.quit()
    return data

def mars_news(browser): 
    #Adding browser to our function tells python that we'll be using the browser variable the we defined outside the function.
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    try:    
        slide_elem = news_soup.select_one('div.list_text') 
        # Referencing the title text of first article.
        slide_elem.find('div', class_= 'content_title') 

        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_= 'content_title').get_text()
    
        # Retrieving the first article summary text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    
    except AttributeError:
        return None, None
    
    return news_title, news_p

def featured_image(browser):
    
    #Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try: 
        # find the relative image url
        img_url_rel = img_soup.fing('img', class_='fancybox-image').get('src')
    except AttributeError:
        return None
    
    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url

def mars_facts(browser):

    # Add try/except for error handling
    try:
        # use 'read_html' to scrape the facts table into a df
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    
    except BaseException:
        return None
    # Assign columns and set index (without new variable reassignment)
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html()

def hemispheres(browser):
    # 1. Use browser to visit the URL 
    url = 'https://marshemispheres.com/'
    browser.visit(url + 'index.html')

    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # Looping through links
    for link in range(4):
    
        #Finding elements
        browser.find_by_css('a.product-item img')[link].click()
    
        # Extract the img_urls
        hemisphere_data = scraping_hemispheres(browser.html)
        hemisphere_data['img_url'] = url + hemisphere_data['img_url']
    
        # Adding to hemisphere_image_urls list
        hemisphere_image_urls.append(hemisphere_data)
    
        # Restart the loop
        browser.back() 
    return hemisphere_image_urls

def scraping_hemispheres(html_text):
    # Parse html 
    hemisphere_soup = soup(html_text, 'html.parser')

    # Error Handling
    try:
        title_element = hemisphere_soup.find("h2", class_='title').get_text()
        sample_element = hemisphere_soup.find('a', text='Sample').get('href')
    
    except AttributeError:
        title_element = None
        sample_element = None
    
    hemispheres = {"title": title_element, "img_url": sample_element}

if __name__ == '__main__':
    # If running as script, print scraped data
    print(scrape_all())


