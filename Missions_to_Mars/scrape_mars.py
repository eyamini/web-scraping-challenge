#!/usr/bin/env python
# coding: utf-8

# In[2]:


#Importing dependencies 

from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd


# In[3]:


# https://splinter.readthedocs.io/en/latest/drivers/chrome.html
get_ipython().system('which chromedriver')


# In[4]:


executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)


# In[5]:


#NASA URL to scrape
url = 'https://mars.nasa.gov/news/'
browser.visit(url)


# In[7]:


# Scrape the "News" using BeautifulSoup
html = browser.html
news = BeautifulSoup(html, "html.parser")
slides = news.select_one("ul.item_list li.slide")
slides.find("div", class_="content_title")


# In[8]:


# Scrape News headers
news_header = slides.find("div", class_="content_title").get_text()
print(news_header)


# In[10]:


# Scrape paragraph text
paragraph = slides.find("div", class_="article_teaser_body").get_text()
print(paragraph)


# In[11]:


# Go to JPL website
executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
browser = Browser("chrome", **executable_path)
url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
browser.visit(url)


# In[12]:


# Click full image view using Splinter
full_image = browser.find_by_id("full_image")
full_image.click()


# In[16]:


# Click "More Info" button
browser.is_element_present_by_text("more info", wait_time=2)
more_info = browser.links.find_by_partial_text("more info")
more_info.click()


# In[17]:


# Parse with BS
html = browser.html
soup = BeautifulSoup(html, 'html.parser')


# In[19]:


# Find Source
featured_image_url = soup.select_one("figure.lede a img").get("src")
featured_image_url


# In[20]:


# Creating absolute URL
featured_image_url = f"https://www.jpl.nasa.gov{featured_image_url}"
print(featured_image_url)


# In[41]:


# Go to Mars Weather on Twitter 
browser.visit("https://twitter.com/marswxreport?lang=en")


# In[42]:


html = browser.html
soup = BeautifulSoup(html, "html.parser")


# In[47]:


# Find latest Tweets
tweets = soup.find_all("p")


# In[50]:


# Get latest Tweet
mars_weather = tweets[0].text

print(mars_weather)


# In[51]:


# Using Pandas to scrape table data
table = pd.read_html('https://space-facts.com/mars/')


# In[52]:


df = table[1]
df


# In[53]:


# Visit the USGS Astrogeology site
executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
browser = Browser("chrome", **executable_path, headless=False)
url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
browser.visit(url)


# In[60]:


# Get URLs and titles for all four hemispheres
hemisphere_urls = []

# Build list of hemispheres
list = browser.find_by_css("a.product-item h3")
for i in range(len(list)):
    hemisphere = {}
    
    browser.find_by_css("a.product-item h3")[i].click()
    
    sample = browser.links.find_by_text("Sample").first
    hemisphere["img_url"] = sample["href"]
    
    # Collect titles
    hemisphere["title"] = browser.find_by_css("h2.title").text
    
    hemisphere_urls.append(hemisphere)
    
    # Go back and repeat
    browser.back()


# In[61]:


hemisphere_urls


# In[ ]:

def scrape():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    browser = Browser("chrome", **executable_path, headless=False)
    news_header, paragraph = news_header(browser)
    url = featured_image_url(browser)
    mars_weather = tweets(browser)
    hemisphere = hemisphere_urls(browser)

    data = {
        "news_header": news_header,
        "paragraph": paragraph,
        "featured_image": featured_image_url,
        "weather": mars_weather,
        "hemispheres": hemisphere_urls,
    }
    browser.quit()
    return data 

if __name__ == "__main__":
    print(scrape())


