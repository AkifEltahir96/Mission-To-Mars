# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

# Splinter & Executable Path Set Up
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless = False)

# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)
# Here we able to do two things.
# 1. We are searching for elements with a specific combination of the tag (div) and attribute (list_text).
# 2. wait_time =, allows us to delay the search for components which is useful for content heavy (images) pages.


html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')
#slide_elem is the parent element. It will contain the <div> tag and all of the descending elements.
# The . is used to select classes under a tag (in this case <div>).
# select_one allows us to pick the first matching element as CSS works from right to left.


# Referencing the title text of first article.
slide_elem.find('div', class_= 'content_title')
# .find allows you to narrow down a search in a variable containing tons of information.
# here we are looking for the content title, which we have specified with the arguments (tag, class)


# Use the parent element to find the first 'a' tag and save it as 'news_title'
news_title = slide_elem.find('div', class_= 'content_title').get_text()
news_title
# .get_text() will return the string content only

# Retrieving the first article summary text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p

# ### Featured Images

url = 'https://spaceimages-mars.com'
browser.visit(url)

# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()
# full_image_elem --> holds the scrape into a variable
# browser.find_by_tag('button') --> browser finds an element by its tag
# splinter will 'click' the image to view its full size.

# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel
# img is the tag that contains the photo
# .get('src') pulls the link to the image.


# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url

# ### Mars Facts

# We are creating a new DataFrame from the HTML table.
# read_html specifically searches for and returns a list of tables found in the table, we index 0 to only pull the first table.
df = pd.read_html('https://galaxyfacts-mars.com')[0]
# Assign columns
df.columns=['description', 'Mars', 'Earth']
# Setting the index to description without reassignment to a new variable
df.set_index('description', inplace=True)
df

# Converting the df to a html source.
df.to_html()

# Quitting automated browser
browser.quit()

