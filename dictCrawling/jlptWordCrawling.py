from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

options = Options()
options.add_argument("--start-maximized")
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)



jlptLevel = 5 # JLPT 급수

count = 0 # 단어 index

folder_path = "./JLPT"
file_name = "JLPT_N5.txt"

file_path = os.path.join(folder_path, file_name)

f = open(file_path, "w", encoding='utf-8')

for i in range(75): # 페이지 수

    pageUrl = f"https://ja.dict.naver.com/#/jlpt/list?level={jlptLevel}&part=allClass&page={i+1}"

    driver.get(pageUrl)

    # 페이지 로딩 기다리기
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "li.row")))

    for j in range(10): # 페이지 당 단어 수
        # 해당 단어의 엘리먼트 선택
        try:
            word = driver.find_elements(By.CSS_SELECTOR, "li.row")[j]
        except:
            print("word Error", count)
            break

        # 단어의 히라가나 추출
        try:
            hiragana = word.find_element(By.CLASS_NAME, "link").text.replace("-", "")
        except:
            print("hiragana Error", count)

        # 단어의 한자 추출
        try:
            kanji = word.find_element(By.CLASS_NAME, "pronunciation").text
        except:
            print("kanji Error", count)
            kanji = "-"

        if(kanji): 
            kanji = kanji.replace("[", "").replace("]", "")

        # 단어의 의미 추출
        mean = word.find_element(By.CLASS_NAME, "mean").text

        parts = [] # 품사

        # 의미 문자열에서 품사 추출
        while True:
            mean.strip()
            partArray = mean.split()
            if(len(partArray) > 1 and (partArray[0] == "명사" or partArray[0] == "대명사" or partArray[0] == "동사" or partArray[0] == "조사" or partArray[0] == "형용사" or partArray[0] == "접사" or partArray[0] == "부사" or partArray[0] == "감동사" or partArray[0] == "형용동사" or partArray[0] == "기타")):
                parts.append(partArray[0])
                partArray = partArray[1:]
                mean = " ".join(partArray)
            else:
                break

        printString = f"\"{count}\", \"{kanji}\", \"{hiragana}\", \"{parts}\", \"{mean}\"\n"

        f.write(printString)

        count+=1

f.close()