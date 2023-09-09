# 필요한 라이브러리 불러오기
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd

# 매장 정보 리스트 선언
store_name_list = []
store_address_list = []
store_phone_list = []

# 성남시 매장 정보 가져오기
# gyunggi_index = 9
# seongnam_index = [16,17,18]
# wd.get('https://www.kyochon.com/shop/domestic.asp?sido1={gyunggi_index}&sido2={seongnam_index}&txtsearch=')

def kyochon_store_crawler(gyunggi_index,seongnam_index,index):
    wd_name = f"wd{index}"
    # 매장 정보 가져오기
    globals()[wd_name] = webdriver.Chrome('bigdata/2_Selenium/chromedriver_mac_arm64/chromedriver')
    globals()[wd_name].get(f'https://www.kyochon.com/shop/domestic.asp?sido1={gyunggi_index}&sido2={seongnam_index}&txtsearch=')

    # 페이지 소스  가져오기
    html = globals()[wd_name].page_source
    soup = BeautifulSoup(html, 'html.parser')

    # 매장 정보를 html형식 리스트로 저장하기
    store_list = soup.select('div.shopSchList > ul > li')

    # 가게 이름, 주소, 전화번호
    for store in store_list:
        store_name = store.select_one('span.store_item > strong').text
        store_name_list.append(store_name)

        store_address_phone_list = store.select_one('span.store_item > em').text.replace('\t','').split('\n')
        store_address_list.append(store_address_phone_list[2].replace('(','').replace(')',''))
        store_phone_list.append(store_address_phone_list[3])

    globals()[wd_name].quit()
    return 0

kyochon_store_crawler(9,16,1)
kyochon_store_crawler(9,17,2)
kyochon_store_crawler(9,18,3)

# 테스트
# print("store_name_list: "+str(store_name_list))
# print("store_address_list: "+str(store_address_list))
# print("store_phone_list: "+str(store_phone_list))
# print(len(store_name_list))
# print(len(store_address_list))
# print(len(store_phone_list))

# csv 파일로 저장하기
store_info_df = pd.DataFrame({'이름':store_name_list,'도로명 주소':store_address_list,'전화번호':store_phone_list})
print(store_info_df)
store_info_df.to_csv('bigdata/3_Site_Crawling/kyochon_store_info.csv',encoding='utf-8-sig',index=False)