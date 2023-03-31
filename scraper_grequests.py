import grequests
from bs4 import  BeautifulSoup as bs
import time
import json
from fake_useragent import UserAgent 

ua = UserAgent()

headers = {
    'User-Agent': ua.random
}

links = [f'https://www.bbc.com/zhongwen/simp/topics/c9mjeq29pxlt?page={page}' for page in range(1,5)]

starttime = time.time()

try:
    response = (grequests.get(link, headers=headers) for link in links)
    response_bbc = grequests.imap(response, grequests.Pool(4))

    news_all = []
    for res in response_bbc:
        soup_bbc = bs(res.text, 'lxml')

        urls = soup_bbc.find_all(
            'h2', {'class':'bbc-3hl34q e47bds20'})
        
        sub_links = [i.a["href"] for i in urls]
        sub_response = (grequests.get(sub_link, headers=headers) for sub_link in sub_links)
        sub_response_bbc = grequests.imap(sub_response, grequests.Pool(70))
        
        for sub_res in sub_response_bbc:
            news = {}
            tag = [] 
            soup_sub = bs(sub_res.text, 'lxml')
            titles_article = soup_sub.find('h1', id='content')

            if titles_article: 
                news['title'] = titles_article.text
                print(titles_article.text)
            else:
                print("title not existed")

            tags = soup_sub.find_all('li', 'bbc-1msyfg1 e2o6ii40')

            if tags:
                for elements in tags:
                    tag.append(elements.text)
                    print(tag)
            else:
                print("tags not existed")

            news['tags']= tag
            # print(news)
            news_all.append(news)

    with open ('bbc_news.json', 'w') as f:
            json.dump(news_all, f, indent=4, ensure_ascii=False)

except Exception as e:
    print(str(e))


endtime = time.time()
print(f'spent {endtime - starttime} seconds')