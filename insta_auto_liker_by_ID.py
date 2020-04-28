import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
import requests

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
#chrome_options.add_argument("--headless")
driver = webdriver.Chrome('C:/Users/PC/Downloads/chromedriver/chromedriver.exe',
                          options=chrome_options)

## url에 접근
driver.get('https://www.instagram.com/')
print("○ 로그인 페이지 접속")

username = 'aaa'
password = 'aaa'
driver.implicitly_wait(2)
print("○ 로그인 시도 중")

# id, pw 입력할 곳을 찾습니다.
driver.find_element_by_name("username").send_keys(username)
driver.find_element_by_name("password").send_keys(password + Keys.ENTER)
time.sleep(2)
print("○ 로그인 완료")
time.sleep(2)
print("○ 작업 시작")

# 엑셀 불러오기
print("○ 엑셀 파일 로딩")
where_file=('instaurl.xlsx')
df=pd.read_excel(where_file, 'Sheet1', index_col=None, na_values=['NA'])


if 'done' in df.columns:
    print("체크 용 done열 존재")
else:
    df["done"]=""
    print("체크 용 done열 생성")



# 엑셀의 2번째 줄부터(1번째 줄은 col로 설정) 불러와서 정보 parsing
for i in range(0,len(df)):

    url = df.iloc[i, 0]  # 첫 열의 첫 줄부터 순서대로 처리
    instaid = url.split('/')[3]  # 인스타 아이디 분리

    if df.iloc[i,1]=='O':
        print(instaid," 이미 좋아요 하고 넘어감")
    else:
        print("안넘어가")
        ## url에 접근
        # url='https://www.instagram.com/kissrealslow/'
        driver.get(url)
        driver.implicitly_wait(2)

        text = driver.page_source
        soup = BeautifulSoup(text, 'html.parser')
        userPostGet = soup.findAll("div", {"class": "v1Nh3"})

        links = []
        for userPost in userPostGet:
            instaLink = 'https://www.instagram.com'
            linkAddr = userPost.find("a")['href']
            links.append(instaLink + linkAddr)

        instaId = url.split('/')[3]
        print(instaId)
        links = links[0:3]
        for s in links:
            print(s)

        for url in links:
            driver.get(url)
            time.sleep(3)
            driver.find_element_by_css_selector("._8-yf5").click()
            print("성공")
            time.sleep(2)

        df.iloc[i, 1] = 'O'

        df.to_excel(where_file, 'Sheet1', index=False, encoding='utf-8')










# 불러와서 done 열에 동그라미 들어가있는지 확인하고
# 안들어가있을 경우 하나씩 url 들어가고 done 열에 동그라미 추가







