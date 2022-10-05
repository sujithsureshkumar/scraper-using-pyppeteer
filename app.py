import asyncio
from typing import List
from pyppeteer import launch
# import json module
import json

async def get_article_titles(keyword):
   search_engine_url="https://duckduckgo.com/"
   # launch browser in headless mode
   browser = await launch({"headless": False, "args": ["--start-maximized"]})
   # create a new page
   page = await browser.newPage()
   # set page viewport to the largest size
   await page.setViewport({"width": 1600, "height": 900})
   # navigate to the page
   await page.goto(search_engine_url)
   # locate the search box
   entry_box = await page.querySelector("div")
   #.TextInput_userInput__807JK
   #.gLFyf

   print("====================== {} ======================".format(keyword))
    # type keyword in search box
   await entry_box.type(keyword)
    # wait for search results to load
   await page.waitFor(4000)
    # press enter key
   await page.keyboard.press('Enter')
    # wait for search results to load
   await page.waitFor(4000)
    

   # list of dictionaries 
   data = [
      {
         "search engine":search_engine_url,
         "search query":keyword
         }
   ]
   
    # extract the results
   results = await page.querySelectorAll("article")
   
    #intialise result index
   index=1
   for result in results:
     # dictionaries 
     dict = {}
      #assigning result index
     dict["result"]=index
        # extract the title of the result
     title = await result.querySelector("h2")
     titleContent = await title.getProperty("textContent")
       # extract the link of the result
     link = await result.querySelector("a:nth-child(2)")
     linkContent = await link.getProperty("textContent")
      # extract the description of the result
     description = await result.querySelector("div:nth-child(3)")
     descriptionContent = await description.getProperty("textContent")

      #adding key values to the dictionary
     dict["title"]=await titleContent.jsonValue()
     dict["link"]=await linkContent.jsonValue()
     dict["content"]=await descriptionContent.jsonValue()
       #adding dictionary to the data list
     data.append(dict)
     index=index+1

   # convert into json
   json_object = json.dumps(data, indent=2)
   # display
   print(json_object)

   with open("result.json", "w") as outfile:
    outfile.write(json_object)



print("Starting...")

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
loop.run_until_complete(get_article_titles("coffee"))
print("Finished extracting articles titles")