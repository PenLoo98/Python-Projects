import requests
import xml.etree.ElementTree as ET
import pandas as pd
from datetime import datetime, timedelta

# xml 형태로 데이터를 받아옴
# 기준일자 statusDt
# 확진자 수 hPntCnt
# 검사 중 수 uPntCnt
# 치료 중 환자 수 careCnt
# 사망자 수 gPntCnt
# 누적 검사 수 accExamCnt
# 누적 검사 완료 수 accExamCompCnt
# 누적 확진률 accDefRate

statusDt = []
hPntCnt = []
uPntCnt = []
careCnt = []
gPntCnt = []
accExamCnt = []
accExamCompCnt = []
accDefRate = []

# 날짜 리스트 생성 (20200501~20220301)
start_date = datetime(2020, 5, 1)
end_date = datetime(2020, 6, 1)
date_list = []
while start_date <= end_date:
    date_list.append(start_date.strftime('%Y%m%d'))
    start_date += timedelta(days=1)


# API를 통해 데이터 받아오는 함수
def get_covid_info(date):
    # API
    serviceKey = '0LTYCAX2Qakrmrre5AqmxT+BffL9mP8R0Tj3Qhpu/vic7TlNW1Te2stdxhw03lDEu5fsPbAYtltSeX7dkuUEqA=='
    url = 'http://apis.data.go.kr/1352000/ODMS_COVID_02/callCovid02Api'
    params ={'serviceKey' : serviceKey, 'pageNo' : '1', 'numOfRows' : '500', 'apiType' : 'json', 'status_dt' : str(date) }

    response = requests.get(url, params=params)
    html = response.content

    root = ET.fromstring(html)
    statusDt.append(root.find('.//statusDt').text)
    hPntCnt.append(root.find('.//hPntCnt').text)
    uPntCnt.append(root.find('.//uPntCnt').text)
    careCnt.append(root.find('.//careCnt').text)
    gPntCnt.append(root.find('.//gPntCnt').text)
    accExamCnt.append(root.find('.//accExamCnt').text)
    accExamCompCnt.append(root.find('.//accExamCompCnt').text)
    accDefRate.append(root.find('.//accDefRate').text)

    print(f'{date} 데이터 받아오기 완료')

# 날짜별로 데이터 받아오기
for date in date_list:
    get_covid_info(date)

# 데이터 프레임에 채우기
df = pd.DataFrame(columns=['기준일자', '확진자 수', '검사 중 수', '치료중 환자수', '사망자 수', '누적 검사 수', '누적 검사 완료 수', '누적 확진률'])
df['기준일자'] = statusDt
df['확진자 수'] = hPntCnt
df['검사 중 수'] = uPntCnt
df['치료중 환자수'] = careCnt
df['사망자 수'] = gPntCnt
df['누적 검사 수'] = accExamCnt
df['누적 검사 완료 수'] = accExamCompCnt
df['누적 확진률'] = accDefRate

# csv 파일로 저장
df.to_csv('/Users/penloo/Library/CloudStorage/GoogleDrive-penloo@gachon.ac.kr/My Drive/Programming-Language/Python/Bigdata-WepCrawling/bigdata/0_API_Crawling/covid_info.csv', index=False, encoding='utf-8-sig')
print(f'{start_date}~{end_date} 저장 완료')

