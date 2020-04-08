#!/usr/bin/env python
# coding: utf-8

# In[1]:


from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from bs4 import BeautifulSoup
from linebot import LineBotApi
from linebot.models import TextSendMessage
import json


# In[27]:


options = FirefoxOptions()
options.add_argument("--headless")
driver = webdriver.Firefox(options=options)
driver.get("https://www.ozbargain.com.au/cat/electrical-electronics/deals")
htmltext = driver.page_source
driver.close()

soup = BeautifulSoup(htmltext, 'html.parser')
deals_divs = soup.findAll("div", {"class": "node-ozbdeal"})

line_bot_api = LineBotApi('your_token')


new_deals = []
update = False

with open('data.txt') as json_file:
    pre_data = json.load(json_file)
    tmp_data = [p['id'] for p in pre_data['deals']]

for i,deal in enumerate(deals_divs):
    if i >= 10:
        break
    else:
        h2 = deal.find('h2')
        deal_id = h2['id'].replace('title','')

        if deal_id not in tmp_data:
            update = True
            new_deals.append(deal_id)
            #title = h2['data-title']

            #push message to one user
            line_bot_api.push_message(
                'user_id', 
                TextSendMessage(text=title+" https://www.ozbargain.com.au/node/"+deal_id)
            )
        
if update:
    for deal in new_deals:
        pre_data['deals'].insert(0,{'id':deal})
        pre_data['deals'].pop()
    
    with open('data.txt', 'w') as outfile:
        json.dump(pre_data, outfile)
        
        


# In[ ]:




