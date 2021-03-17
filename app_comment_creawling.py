import time
import glob
import os
import re
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
from combine_file import combine_file


### 구글 앱스토어 댓글 가져오기 함수
def google_app_cmt(url_list):
    for sub_url in url_list:

        driver = webdriver.Chrome(
            "./chromedriver.exe"
        )  # webdriver 객체 생성 (chromedriver(버전 맞는 크롬드라이버 깔아놔야함))

        url = "https://play.google.com/store/apps/" + sub_url + "&showAllReviews=true"  # url 생성, 뒤에 showallreview=ture
        driver.implicitly_wait(5.0)  # 웹 자원 로드 (3초)
        driver.get(url)  # 크롬으로 URL 접근

        # 스크롤링 자동화
        last_page_height = driver.execute_script(
            "return document.documentElement.scrollHeight")  #스크롤 정의

        while True:
            spread_review = driver.find_elements_by_xpath(
                "//button[@jsaction='click:TiglPc']")
            for i in range(len(spread_review)):
                isTrue = spread_review[i].is_displayed()  # 보이는 것인지를 확인
                if isTrue:
                    spread_review[i].click()
                    print(
                        str(i) +
                        "th more button is clicked and wait 0.5 secs...")
                    time.sleep(0.5)

            driver.execute_script(
                "window.scrollTo(0, document.documentElement.scrollHeight);")
            time.sleep(3.0)  # 1이상으로 인터벌을 줘야 데이터 취득가능 (롤링시 데이터 로딩 시간 때문)
            new_page_height = driver.execute_script(
                "return document.documentElement.scrollHeight")

            if new_page_height == last_page_height:
                #리스트 더보기가 있는지 확인하여 클릭하고 없으면 브레이크
                if driver.find_elements_by_xpath(
                        "//span[@class='RveJvd snByac']"):
                    spread_list = driver.find_elements_by_xpath(
                        "//span[@class='RveJvd snByac']")
                    for i in range(len(spread_list)):
                        spread_list[i].click()
                else:
                    break
            last_page_height = new_page_height

        html_source = driver.page_source  # 현재 렌더링 된 페이지의 Elements 가져오기
        short_reviews = driver.find_elements_by_xpath(
            "//span[@jsname='bN97Pc']")  #처음부터 보이는 잛은리뷰
        long_reviews = driver.find_elements_by_xpath(
            "//span[@jsname='fbQN7e']")  #한번에 표시되지 않는 리뷰 전체보기가 있는경우
        review_stars = driver.find_elements_by_xpath(
            "//span[@class='nt2C1d']/div[@class='pf5lIe']/div[@role='img']")
        review_date = driver.find_elements_by_xpath("//span[@class='p2TkOb']")

        App_title_path = driver.find_elements_by_xpath("//h1[@class='AHFaub']")
        App_title = App_title_path[0].text

        # 댓글 및 별점용 리스트
        str_app_comments = []

        for i in range(len(short_reviews)):
            if not long_reviews[i]:
                comment_tmp = str(long_reviews[i].text)
            else:
                comment_tmp = str(short_reviews[i].text)
            comment_tmp = comment_tmp.replace("\n", "")
            comment_tmp = comment_tmp.replace("\t", "")
            comment_tmp = comment_tmp.replace("   ", "")
            comment_tmp = re.sub(r"\d+", "", comment_tmp)

            if (comment_tmp != ""):
                str_app_comments.append({
                    "Date":
                    review_date[i].text,
                    "COMMENT":
                    comment_tmp,
                    "Star":
                    review_stars[i].get_attribute('aria-label')
                })

        driver.close()

        # MODIRY VIEW FORMAT
        google_app_pd = pd.DataFrame(str_app_comments)

        # WRITE TO CSV
        file_name = "./data/cmt_대신 읽어줘.csv"
        if not os.path.exists(file_name):
            google_app_pd.to_csv(file_name,
                                 index=False,
                                 mode="w",
                                 encoding="utf-8-sig")
        else:
            google_app_pd.to_csv(file_name,
                                 index=False,
                                 mode="a",
                                 encoding="utf-8-sig",
                                 header=False)


# app_list = [    "details?id=com.tmapforjlr.android", "details?id=com.kakao.i.connect",
# "details?id=com.kakao.i.home", "details?id=com.skt.aladdin",
# "details?id=com.google.android.apps.googleassistant",
# "details?id=com.google.android.tts", "details?id=com.naver.nozzle",
# "details?id=com.naver.clova.minute", "details?id=com.lguplus.aispeaker",
# "details?id=com.kt.gigagenie.mobile", "details?id=net.ai.ai.ai.inoi",
# "details?id=com.sunny_lte", "details?id=com.dek.voice",
# "details?id=kr.co.systran.eztalky",
# "details?id=com.ssongshrimptruck.tistory.readforme",
# "details?id=com.onethefull.avadin", "details?id=ru.yvs",
# "details?id=com.whox2.whowho.tts"]
app_list = [
    "details?id=com.dek.voice",
]

# 크롤링 실행
google_app_cmt(app_list)

# 크롤링 데이터 합치기
combine_file("cmt_google_app")