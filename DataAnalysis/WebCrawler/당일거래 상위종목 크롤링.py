# 필요한 라이브러리 불러오기
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time

stock_titles = []
current_prices = []
trade_volumes = []

def stock_naver_crawler(index):
    wd_name = f"wd{index}"
    # 주식 정보 가져오기
    globals()[wd_name] = webdriver.Chrome('bigdata/2_Selenium/chromedriver_mac_arm64/chromedriver')
    globals()[wd_name].get(f'https://finance.naver.com/sise/sise_quant.naver')
    time.sleep(3)

    # 페이지 소스  가져오기
    html = globals()[wd_name].page_source
    soup = BeautifulSoup(html, 'html.parser')

    ### 주식 정보를 html형식 리스트로 저장하기
    stock_info = soup.select('div#newarea > div#contentarea > div.box_type_l > table.type_2 > tbody > tr')[2:]
    for stock in stock_info:
        stock_info = stock.text.replace('\t','').split('\n')
        stock_info = list(filter(None, stock_info))
        if stock_info != []:
            # print(stock_info)
            stock_titles.append(stock_info[1]) # 종목명
            current_prices.append(stock_info[2]) # 현재가
            trade_volumes.append(stock_info[5]) # 거래량

    globals()[wd_name].quit()
    return 0

stock_naver_crawler(1)

### 테스트
# print(stock_titles)
# print(current_prices)
# print(trade_volumes)

# print(len(stock_titles))
# print(len(current_prices))
# print(len(trade_volumes))

# csv 파일로 저장하기
stock_info_df = pd.DataFrame({'종목':stock_titles,'현재가':current_prices,'거래량':trade_volumes})
print(stock_info_df)
stock_info_df.to_csv('bigdata/3_Site_Crawling/stock_naver_info.csv',encoding='utf-8-sig',index=False)