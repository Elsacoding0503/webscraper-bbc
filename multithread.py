import requests
from bs4 import  BeautifulSoup as bs
import time
import json
import concurrent.futures
from fake_useragent import UserAgent 

ua = UserAgent()

headers = {
    'User-Agent': ua.random
}

def scraper_science(links):

    try:
        response_bbc = requests.get(links, headers=headers, timeout =5)

        if response_bbc.status_code ==200:
            soup_bbc = bs(response_bbc.text, 'lxml')

            news_all = []
            urls = soup_bbc.find_all('h2', {'class':'bbc-3hl34q e47bds20'})
            for i in urls:
                news = {}
                tag = [] 
                time.sleep(1)
                subresponse = requests.get(i.a["href"], headers=headers)
                soup_sub = bs(subresponse.text, 'lxml')
                titles_article = soup_sub.find('h1', id='content')

                if titles_article: 
                    news['title'] = titles_article.text
                else:
                    print("title not existed")

                tags = soup_sub.find_all('li', 'bbc-1msyfg1 e2o6ii40')

                if tags:
                    for elements in tags:
                        tag.append(elements.text)
                else:
                    print("tags not existed")

                news['tags']= tag
                print(news)
                news_all.append(news)

        else:
            print("status_code is not 200")

        with open ('bbc_news.json', 'w') as f:
                json.dump(news_all, f, indent=4, ensure_ascii=False)

    except Exception as e:
        print(str(e))


starttime = time.time()

links = [f'https://www.bbc.com/zhongwen/simp/topics/c9mjeq29pxlt?page={page}' for page in range(1,5)]

with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    executor.map(scraper_science, links)

endtime = time.time()
print(f'spent {endtime - starttime} seconds')