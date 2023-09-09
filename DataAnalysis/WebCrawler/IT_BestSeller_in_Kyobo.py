# 필요한 라이브러리 불러오기
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time

book_title = []
book_author = []
book_price = []

IT_category = 'e'

# def book_kyobo_crawler(category,page,index):
def book_kyobo_crawler(index):
    wd_name = f"wd{index}"
    # 책 정보 가져오기
    globals()[wd_name] = webdriver.Chrome('bigdata/2_Selenium/chromedriver_mac_arm64/chromedriver')
    globals()[wd_name].get(f'https://product.kyobobook.co.kr/bestseller/total?saleCmdtClstCode=e&period=002#?page=1&per=20&period=002&ymw=&bsslBksClstCode={IT_category}')
    time.sleep(3)

    # 페이지 소스  가져오기
    html = globals()[wd_name].page_source
    soup = BeautifulSoup(html, 'html.parser')

    # 책 정보를 html형식 리스트로 저장하기
    book_list = soup.select('ol.prod_list > li.prod_item > div.prod_area.horizontal > div.prod_info_box')
    
    # 책 제목, 저자, 가격
    for book in book_list:
        title_data = book.select_one('span.prod_name').text
        book_title.append(title_data)
        author_data = book.select_one('span.prod_author').text
        book_author.append(author_data)
        price_data = book.select_one('span.price > span.val').text
        book_price.append(price_data)

    globals()[wd_name].quit()
    return 0

book_kyobo_crawler(1)

# 테스트
# print(book_title)
# print(book_author)
# print(book_price)

# print(len(book_title))
# print(len(book_author))
# print(len(book_price))

# csv 파일로 저장하기
book_info_df = pd.DataFrame({'제목':book_title,'출판정보':book_author,'가격':book_price})
print(book_info_df)
book_info_df.to_csv('bigdata/3_Site_Crawling/book_kyobo_info.csv',encoding='utf-8-sig',index=False)