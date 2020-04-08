#!/usr/bin/env python
# coding: utf-8

# In[40]:


from selenium import webdriver
from bs4 import BeautifulSoup
from linebot import LineBotApi
from linebot.models import TextSendMessage
import json


# In[69]:


driver = webdriver.Chrome() #path:/user/local/bin
driver.get("https://www.ozbargain.com.au/cat/electrical-electronics")
htmltext = driver.page_source
driver.close()

soup = BeautifulSoup(htmltext, 'html.parser')
deals_divs = soup.findAll("div", {"class": "node-ozbdeal"})


new_deals = []
update = False

with open('data.txt') as json_file:
    current_data = json.load(json_file)
    pre_data = [p['id'] for p in current_data['deals']]

for deal in deals_divs:
    
    h2 = deal.find('h2')
    deal_id = h2['id'].replace('title','')
    if deal_id not in pre_data:
        update = True
        new_deals.append(deal_id)
        title = h2['data-title']
        
        #push message to one user
        
        
if update:
    for deal in new_deals:
        current_data['deals'].pop()
        current_data['deals'].insert(0,{'id':deal})
    
    with open('data.txt', 'w') as outfile:
        json.dump(current_data, outfile)
        

