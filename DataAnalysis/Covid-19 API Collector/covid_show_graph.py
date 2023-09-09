import pandas as pd
import matplotlib.pyplot as plt

# 확진자 수 hPntCnt
# 검사 중 수 uPntCnt
# 치료 중 환자 수 careCnt
# 사망자 수 gPntCnt
# 누적 검사 수 accExamCnt
# 누적 검사 완료 수 accExamCompCnt
# 누적 확진률 accDefRate

# 한글 폰트
plt.rc('font', family='AppleGothic')

# 저장한 csv파일 불러옴
df = pd.read_csv('bigdata/5_ Covid_Report/covid_info.csv',encoding='utf-8-sig')
print(df.columns)
dates = df.loc[:,'기준일자'].to_list()
dates = [str(date)[4:] for date in dates]

def get_covid_info(category):
    infoList = df.loc[:,category].to_list()

    plt.plot(dates,infoList) # x축, y축

    # x축 눈금 설정
    fig, ax = plt.subplots()
    ax.plot(dates, infoList)
    ax.set_xticks(range(0, len(dates), 7))

    plt.title('2020 ' + category)
    plt.xlabel('날짜')
    plt.ylabel(category)
    plt.show()

get_covid_info('확진자 수')
get_covid_info('검사 중 수')
get_covid_info('치료중 환자수')
get_covid_info('사망자 수')
get_covid_info('누적 검사 수')
get_covid_info('누적 검사 완료 수')
get_covid_info('누적 확진률')