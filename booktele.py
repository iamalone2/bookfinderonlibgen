import requests,bs4,urllib,csv              
import pandas as pd
#Getting the name of the book to be searched
import pyrogram
from pyrogram import Client, filters
from pyromod import listen
#from details import api_id, api_hash, bot_token
from pyrogram.types import User, Message
import subprocess
import os
import aiohttp
import asyncio
import aiofiles
import re
from csv import reader
import time

bot = Client(
    "bookuploader",
    api_id=7654273,
    api_hash='61433d4f3704606593802b9d92992e76',
    bot_token="1915481883:AAErsP1-cSKEUdQWXoOyw1mezl5BTbF4g3Q")


@bot.on_message(filters.command(["start"]))
async def start(bot, update):
    await update.reply_text("Hi I am book finder and downloader Press /book_download <book_name>")


@bot.on_message(filters.command(['book_download'])& ~filters.edited)
async def animelist(bot: Client, m: Message):
    search = await m.reply_text("**Enter the Book Name To find **")
    input1: Message = await bot.listen(search.chat.id, timeout=600) 
    search1 = input1.text
    nameofbook = input1.text
    #print('Enter book name: ',end='')
    #search = input()
    #url of the age to be scraped
    print(search1)
    url = f'http://gen.lib.rus.ec/search.php?req={search1}&phrase=1&view=simple&column=def&sort=year&sortmode=DESC'
    res = requests.get(url) #requests to the server and gets response
    res.raise_for_status()  #raises error if request is rejected or due to any other reason

    #res.text bieng passed to the BeautifulSoup function as only text object can be processed
    #'html.parse' is given to provide a uniform parser even if it is used on another platform
    soup = bs4.BeautifulSoup(res.text,'html.parser') 

    table = soup.find('table',attrs = {"class":"c"}) #Finding the table with class='c'

    results = table.findAll('tr') #Finding all the <tr> tag components

    #Initialising all the variables to be stored in the csv file
    author = []
    title = []
    publisher = []
    year = []
    pages = []
    language = []
    size = []
    extension = []
    link1 = []
    link2 = []
    link3 = []
    link4 = []
    link5 = []
    teledata = []
    vv = []
    count = 1
    # Items stored in results is in list form, thus looping over its items
    for i in range(1,len(results)):
        #Writing everything in one list so as to write later in the csv file        
        author.append((results[i].select('td'))[1].getText())   #Selecting <td> tag text content
        title.append((results[i].select('td'))[2].getText())
        publisher.append((results[i].select('td'))[3].getText())
        year.append((results[i].select('td'))[4].getText())
        pages.append((results[i].select('td'))[5].getText())
        language.append((results[i].select('td'))[6].getText())
        size.append((results[i].select('td'))[7].getText())
        extension.append((results[i].select('td'))[8].getText())
        link1.append(results[i].select('td')[9].find('a').get('href'))  #Selecting <td> tag <a> content with value 'href'
        link2.append(results[i].select('td')[10].find('a').get('href'))
        link3.append(results[i].select('td')[11].find('a').get('href'))
        link4.append(results[i].select('td')[12].find('a').get('href'))
        link5.append(results[i].select('td')[13].find('a').get('href'))
        teledata.append(count)
        count = count+1
        teledata.append((results[i].select('td'))[1].getText())
        teledata.append((results[i].select('td'))[2].getText())
        teledata.append((results[i].select('td'))[4].getText())
        teledata.append((results[i].select('td'))[5].getText())
        teledata.append((results[i].select('td'))[6].getText())
        teledata.append((results[i].select('td'))[7].getText())
        teledata.append((results[i].select('td'))[8].getText())
        teledata.append(results[i].select('td')[9].find('a').get('href'))  #Selecting <td> tag <a> content with value 'href'
        teledata.append(results[i].select('td')[10].find('a').get('href'))
        teledata.append(results[i].select('td')[11].find('a').get('href'))
        teledata.append(results[i].select('td')[12].find('a').get('href'))
        teledata.append(results[i].select('td')[13].find('a').get('href')) 
        if len(f'{vv}{teledata}') > 4096:
            await m.reply_text(vv)
            vv = []
        vv+=teledata
        teledata=[]
        

    await m.reply_text(vv)



    

    
    columns = []
    columns.append([author,title,publisher,year,pages,language,size,extension,link1,link2,link3,link4,link5])   #Writing everything in one list so as to write later in the csv file
    
    # Converting above list into row form as only rows can be written in csv file
    rows = list(zip(*columns[0]))
    
    #Inserting headings of each column element
    rows.insert(0,('Author','Title','Publisher',"Year","Pages","Language","Size","Type","Link 1","Link 2","Link 3","Link 4","Link 5"))
    #Writing on the csv file strictly using 'utf-8' encoding
    with open('Scrape.csv','w',newline = '',encoding = 'utf-8') as f:
        csv_output = csv.writer(f)
        csv_output.writerows(rows)
    
    #Reading files using pandas library for more readability
    file = pd.read_csv('Scrape.csv')    
    if file.size == 0:
        await m.reply_text("Book not found")
        
    #Printing only the desired content of the data
    #print(file.iloc[:,:8])
    
    #Determining the index of the book to get
    #search3 = await m.reply_text("**Enter index number of the book: **")
    #input2: Message = await bot.listen(search.chat.id, timeout=600) 
    #book = input2.text
    #book = input2.text

    #print(int(book))
    #Determining the link to be used as there are 5 links stored in the data
    #search4 = await m.reply_text("**Enter the link number you would like to use: **")
    #input3: Message = await bot.listen(search4.chat.id, timeout=600) 
    #link = input3.text
    #print(int(link))
    
    search4 = await m.reply_text("**Enter the link you would like to download **")
    input3: Message = await bot.listen(search4.chat.id, timeout=600)    
    download_page_link = input3.text
    
    editable4= await m.reply_text("Now send the Pdf or epub in which format is the book")
    input6 = message = await bot.listen(editable.chat.id, timeout = 700)
    raw_text6 = input6.text

    #Scraping another page which was gained from link
    download_page = requests.get(download_page_link)
    download_page.raise_for_status()
    page_soup = bs4.BeautifulSoup(download_page.text,'html.parser')
    
    #Getting the download page's link
    for i in range(len(page_soup.find_all('a'))):
        if (page_soup.find_all('a')[i].getText()) == 'GET':
            download_link = page_soup.find_all('a')[i]['href']
    #book_name = 'abcd'
    cmd  = f'yt-dlp -o "{raw_text6}" "{download_link}" --external-downloader aria2c --downloader-args "aria2c: -x 16 -j 32" '
    os.system(cmd)
    #Writing data on the csv file
    #def download_file(download_url):
    #    response = urllib.request.urlopen(download_url)
    #    file = open('%s.pdf'%nameofbook, 'wb')
    #    file.write(response.read())
    #    file.close()
    #    print("Completed")
    
    #download_file(download_link)
    def progress(current, total):
        print(f"{current * 100 / total:.1f}%")

    await m.reply_document(f'{raw_text6}',caption ='downloaded book by IAMALONE bot',progress = progress )
    time.sleep(2)
    os.remove(f'{raw_text6}')
    





bot.run()
