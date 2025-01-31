from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
from selenium.common.exceptions import StaleElementReferenceException
import requests

'''
입력한 강의와 클릭한 강의 일치하는지 비교해야함 또한 비어있다면 '평가가 없습니다.' 라는 문구를 추가하자

ex) '회계' 입력시
회계
회계
법률회계  이것도 찾게 됨 그래서 일치하는지 비교해야함
'''
def lectureEval(id,password):
    '''
    1. 모든 강의 이름 찾기
    2. 각 강의 평가 긁어오기
    '''

    # 옵션 생성
    options = webdriver.ChromeOptions()
    # 창 숨기는 옵션 추가
    options.add_argument("headless")

    # driver 실행
    driver = webdriver.Chrome(options=options)
    try:
        driver.get("https://account.everytime.kr/login")            # 에브리타임
        ID = id
        PW = password

        # 로그인
        id_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='id']"))
        )
        pw_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='password']"))
        )
        id_field.send_keys(ID)
        pw_field.send_keys(PW)
        time.sleep(4)
        pw_field.send_keys(Keys.RETURN)
        time.sleep(4)

        # 시간표로 이동
        timetable_btn = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a[href='/timetable']"))
        )
        timetable_btn.click()

        # 학기 선택
        dropdown = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "select[id='semesters']"))
        )
        dropdown.click()
        semester = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='semesters']/option[6]"))  # 24년 2학기
        )
        semester.click()

        # 수업 목록 검색
        course_list_btn = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "li[class='button search']"))
        )
        course_list_btn.click()

        # 수업 목록 부분 스크롤 다운
        scroll_container = driver.find_element(By.CSS_SELECTOR, "div#subjects div.list")
        last_height = driver.execute_script("return arguments[0].scrollHeight", scroll_container)
        while True:
            # 스크롤 내리기
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scroll_container)
            time.sleep(2)  # 스크롤 후 로딩 대기
            # 새로운 높이 확인
            new_height = driver.execute_script("return arguments[0].scrollHeight", scroll_container)
            if new_height == last_height:  # 스크롤이 끝에 도달했으면 종료
                break
            last_height = new_height

            #break # to stop early

        # 모든 수업 찾기
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, "html.parser")
        bold_texts = soup.find_all("td", class_="bold")
        lectures = {td.get_text(strip=True): [] for td in bold_texts}

        # 강의실로 이동
        lecture_btn = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a[href='/lecture']"))
        )
        lecture_btn.click()

        # 강의평가 크롤링
        count = 0   # to check
        for lecture in lectures.keys():
            count += 1
            print(count,"/",len(lectures.keys()), "지금 찾는 강의: ", lecture)    # to check

            search_btn = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='search']"))
            )

            for i in range(5):      # 비워지지 않았는데 바로 써지는 경우 방지
                search_btn.clear()
                time.sleep(0.2)

            search_btn.send_keys(lecture)   # 입력
            search_btn.send_keys(Keys.RETURN)
            time.sleep(1)

            # 교수님만 다른 같은 강의들
            same_courses = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.lectures a span.highlight"))
            )
            for i in range(len(same_courses)):
                try:
                    # DOM 무효화 방지
                    same_courses = WebDriverWait(driver, 10).until(
                        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.lectures a div.name"))
                    )
                    element = same_courses[i]
                    element_txt = element.text

                    # 강의 이름이 다를 시, 넘어가도록
                    if lecture != element_txt:
                        continue

                    element.click()
                    time.sleep(1)

                    # 페이지 파싱
                    page_source = driver.page_source
                    soup = BeautifulSoup(page_source, "html.parser")

                    # 교수명, 평점, 평가 추출
                    professor_section = soup.find("section", class_="info")
                    professor_name = "미정 / 미정(전임)"
                    if professor_section:
                        professor_elements = professor_section.find_all("div", class_="item")
                        if len(professor_elements) >= 2:
                            professor_span = professor_elements[1].find("span")
                            if professor_span:
                                professor_name = professor_span.get_text(strip=True)
                    rate = "미평가"
                    review_section = soup.find("section", class_="review")
                    if review_section:
                        rating_div = review_section.find("div", class_="rating")
                        if rating_div:
                            title_div = rating_div.find("div", class_="title")
                            if title_div:
                                rate_span = title_div.find("span", class_="average")
                                if rate_span:
                                    rate = rate_span.get_text(strip=True)
                    details = soup.select("div.text")
                    details = [span.get_text(strip=True).replace('\n', ' ') for span in
                               details] if details else "미평가"

                    # 정보 하나라도 없을 시, 담지 않음
                    if not (professor_name == '미정 / 미정(전임)' or professor_name == '미정(전임)' or professor_name == '강사(미정)'or professor_name == '미정' or rate == '미평가' or details == '미평가'):
                        evaluation = "".join(f"교수명: {professor_name}; 평점: {rate} / 5.00; 평가: {details}")
                        print(evaluation)  # to check
                        lectures[lecture].append(evaluation)

                    driver.back()  # 뒤로 가기
                    time.sleep(1)

                except StaleElementReferenceException:  # 요소 무효화 시 다시 시도
                    print("StaleElementReferenceException 발생, 재시도")
                    continue

            driver.refresh()  # 성공적으로 처리


    finally:
        # 브라우저 닫기
        driver.quit()
        save_to_md("../documents/lectures_eval.md","lecture_eval", (lectures))
        return


def personalInfo(id,password):

    # 옵션 생성
    options = webdriver.ChromeOptions()
    # 창 숨기는 옵션 추가
    options.add_argument("headless")

    # driver 실행
    driver = webdriver.Chrome(options=options)

    try:
        driver.get("https://klas.kw.ac.kr/")  # 광운대학교
        ID = id
        PW = password

        # 로그인
        id_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[id='loginId']"))
        )
        pw_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[id='loginPwd']"))
        )
        id_field.send_keys(ID)
        pw_field.send_keys(PW)
        pw_field.send_keys(Keys.RETURN)
        time.sleep(3)

        cookies = driver.get_cookies()

        driver.get("https://klas.kw.ac.kr/std/cps/inqire/AtnlcScreStdPage.do")
        time.sleep(1)
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, "html.parser")
        info = soup.find("div", class_="tablelistbox")

        # 학생 이름
        stu_name = info.find("table", class_="tablegw").find("tbody").find("tr").find_all("td")[3]
        if stu_name:
            stu_name = stu_name.get_text(strip=True)
        print(stu_name) # to check
        # 취득 학점
        credits={}
        categories = ["전공", "교양", "기타", "계"]
        credit_element = info.find_all("table", class_="tablegw")[2].find("tbody").find_all("td")
        for i, credit in enumerate (credit_element[8:12]):
            value = credit.get_text(strip=True).split('(')[0]
            credits[categories[i]] = value
        print(credits)  # to check

        # 수강한 과목들
        courses_taken = set()
        semesters = info.find_all("table", class_="AType")
        for semester in semesters:
            semester = semester.find("tbody")
            courses = semester.find_all("tr")
            for course in courses:
                course = course.find_all('td')
                course = course[1].get_text(strip=True)
                courses_taken.add(course)
        print(courses_taken)    # to check

    finally:
        # 브라우저 닫기
        driver.quit()
        save_to_md("../documents/personalInfo.md","personal_info",(stu_name, credits, courses_taken))


def save_to_md(filename, data_type, data):
    with open(filename, "w", encoding="utf-8") as file:
        # 강의 평가 저장
        if data_type == "lecture_eval":
            file.write("# 강의 평가\n")
            for lecture, evaluations in data.items():
                file.write(f"## {lecture}\n")
                if evaluations:
                    for evaluation in evaluations:
                        file.write(f"- {evaluation}\n")
                else:
                    file.write("- 평가가 없습니다.")
                file.write("\n")

        # 학점 및 수강 과목 저장
        elif data_type == "personal_info":
            stu_name, credits, courses_taken = data
            file.write(f"# {stu_name} 학생의 개인 학습 정보입니다.\n")
            file.write("## 취득 학점:\n")       # 학점 저장
            for category, value in credits.items():
                file.write(f"- {category}: {value}\n")

            file.write("## 수강한 과목:\n")      # 수강 과목 저장
            if courses_taken:
                file.write(f"- {courses_taken}\n")
            else:
                file.write("- 수강한 과목 없음\n")
        else:
            raise ValueError("지원하지 않는 데이터 타입입니다.")

if __name__ == "__main__":
    id = input("id:")
    password = input("password:")
    personalInfo(id, password) # 취득 학점 및 수강한 과목들
    lectureEval(id,password) # 강의 평가





