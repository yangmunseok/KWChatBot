from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import requests
from selenium.common.exceptions import StaleElementReferenceException
import re
from selenium.webdriver.chrome.options import Options
import os
from selenium.common.exceptions import TimeoutException


# 개인 정보 ---------------------------------
def personalInfo(ID, PW):
    # ChromeDriver 경로 설정
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # 창 없이 실행
    driver = webdriver.Chrome(options=chrome_options)

    stu_info = {}  # 개인 정보

    try:
        driver.get("https://klas.kw.ac.kr/")  # 광운대학교

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

        # KLAS 수강 / 성적조회 사이트
        driver.get("https://klas.kw.ac.kr/std/cps/inqire/AtnlcScreStdPage.do")
        time.sleep(1)
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, "html.parser")
        info = soup.find("div", class_="tablelistbox")

        # 학생 정보 - 나에 대한 정보 추가하자
        stu_categories = ["학부/학과", "학번", "이름", "학적상황"]
        stu_elements = (
            info.find("table", class_="tablegw").find("tbody").find("tr").find_all("td")
        )
        for i, stu_element in enumerate(stu_elements[1:5]):
            value = stu_element.get_text(strip=True)

            if stu_categories[i] == "학번":
                stu_yr = value[:4]  # 2020
                stu_info["입학 년도"] = f"{stu_yr}년도 신입학자"

            stu_info[stu_categories[i]] = value

        table_num = len(
            info.find_all("table", class_="tablegw")
        )  # 공학란 있으면 3, 없으면 2

        # 프로그램 학위과정 (없을 수도 있음)
        if table_num > 2:
            grad_element = (
                info.find_all("table", class_="tablegw")[1].find("tbody").find("td")
            )
            if grad_element:
                grad_process = grad_element.get_text(strip=True)
                stu_info["학위 과정"] = f"{grad_process} 프로그램"
        else:
            stu_info["학위 과정"] = "일반 프로그램"

        # 취득 학점
        cre_categories = ["전공 학점", "교양 학점", "기타 학점", "총 학점"]
        credit_element = (
            info.find_all("table", class_="tablegw")[table_num - 1]
            .find("tbody")
            .find_all("td")
        )
        for i, credit in enumerate(credit_element[8:12]):
            value = credit.get_text(strip=True).split("(")[0]
            stu_info[cre_categories[i]] = value

        # 수강한 과목들
        courses_taken = set()
        semesters = info.find_all("table", class_="AType")
        for semester in semesters:
            semester = semester.find("tbody")
            courses = semester.find_all("tr")
            for course in courses:
                course = course.find_all("td")
                course_name = course[1].get_text(strip=True)
                course_credit = course[4].get_text(strip=True)
                courses_taken.add((course_name, course_credit))
        stu_info["수강한 과목"] = list(courses_taken)
        print(stu_info)

    finally:
        # 브라우저 닫기
        driver.quit()
        # save_to_md("Graduation/personal_info.md", "dictionary", stu_info)

        return stu_info


# 강의 카테고리 (에브리타임)----------------------------------
def lectureEval_everytime(ID, PW):
    """
    1. 모든 강의 이름 찾기
    2. 각 강의 평가 긁어오기
    """

    # ChromeDriver 경로 설정
    driver = webdriver.Chrome()
    try:
        driver.get("https://account.everytime.kr/login")  # 에브리타임

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
            EC.presence_of_element_located(
                (By.XPATH, "//*[@id='semesters']/option[4]")
            )  # 25년 1학기
        )
        semester.click()

        # 수업 목록 검색
        course_list_btn = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "li[class='button search']")
            )
        )
        course_list_btn.click()

        # 수업 목록 부분 스크롤 다운
        scroll_container = driver.find_element(By.CSS_SELECTOR, "div#subjects div.list")
        last_height = driver.execute_script(
            "return arguments[0].scrollHeight", scroll_container
        )
        while True:
            # 스크롤 내리기
            driver.execute_script(
                "arguments[0].scrollTop = arguments[0].scrollHeight", scroll_container
            )
            time.sleep(2)  # 스크롤 후 로딩 대기
            # 새로운 높이 확인
            new_height = driver.execute_script(
                "return arguments[0].scrollHeight", scroll_container
            )
            if new_height == last_height:  # 스크롤이 끝에 도달했으면 종료
                break
            last_height = new_height

            break  # to stop early

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
        count = 0  # to check
        for lecture in lectures.keys():
            count += 1
            print(
                count, "/", len(lectures.keys()), "지금 찾는 강의: ", lecture
            )  # to check

            search_btn = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "input[type='search']")
                )
            )

            for i in range(5):  # 비워지지 않았는데 바로 써지는 경우 방지
                search_btn.clear()
                time.sleep(0.2)

            search_btn.send_keys(lecture)  # 입력
            search_btn.send_keys(Keys.RETURN)
            time.sleep(1)

            # 교수님만 다른 같은 강의들
            same_courses = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, "div.lectures a span.highlight")
                )
            )
            for i in range(len(same_courses)):
                try:
                    # DOM 무효화 방지
                    same_courses = WebDriverWait(driver, 10).until(
                        EC.presence_of_all_elements_located(
                            (By.CSS_SELECTOR, "div.lectures a div.name")
                        )
                    )
                    element = same_courses[i]
                    element_txt = element.text

                    # 강의 이름이 다를 시, 무시 (강의 이름 포함될 시 고려)
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
                        professor_elements = professor_section.find_all(
                            "div", class_="item"
                        )
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
                    details = (
                        [
                            span.get_text(strip=True).replace("\n", " ")
                            for span in details
                        ]
                        if details
                        else "미평가"
                    )

                    # 정보 하나라도 없을 시, 담지 않음
                    if not (
                        professor_name == "미정 / 미정(전임)"
                        or professor_name == "미정(전임)"
                        or professor_name == "강사(미정)"
                        or professor_name == "미정"
                        or rate == "미평가"
                        or details == "미평가"
                    ):
                        evaluation = "".join(
                            f"교수명: {professor_name}; 평점: {rate} / 5.00; 평가: {details}"
                        )
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
        # save_to_md("eval/lectures_eval.md", "list_in_dictionary", lectures)
        return lectures


# 음식 카테고리 (네이버 지도)-------------------------------
def food_naver_maps():
    def time_wait(timeout, code):
        """
        주어진 시간 ('timeout') 내에 특정 CSS 선택자 'code'를 사용하여
        웹 페이지에서 요소가 나타날 때까지 기다리는 기능을 수행합니다.
        """
        try:
            wait = WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, code))
            )
            return wait
        except TimeoutException:
            print(code, "태그를 찾지 못하였습니다.")
            driver.quit()
            return None

    def switch_frame(frame):
        """
        주어진 프레임 ID로 전환하는 함수입니다.
        """
        try:
            # 프레임 ID로 찾기
            iframe = driver.find_element(By.ID, frame)
            # 해당 프레임으로 전환
            driver.switch_to.frame(iframe)
            print(f"Switched to frame: {frame}")
        except Exception as e:
            print(f"Error switching to frame: {frame}. Exception: {e}")

    def page_down(num):
        """
        웹 페이지를 지정된 횟수만큼 아래로 스크롤하는 함수입니다.
        """
        try:
            # 웹 페이지의 body 요소 찾기
            body = driver.find_element(By.CSS_SELECTOR, "body")
            # 페이지를 활성화하기 위해 body 요소를 여러 번 클릭
            for _ in range(10):
                body.click()
                time.sleep(0.3)
            # 지정된 횟수만큼 페이지를 아래로 스크롤
            for i in range(num):
                body.send_keys(Keys.PAGE_DOWN)
                time.sleep(0.3)
        except Exception as e:
            print(f"Error while scrolling down. Exception: {e}")

    def extract_number(string):
        # 정규 표현식을 사용하여 문자열에서 숫자 부분 추출 (쉼표 제거)
        cleaned_string = re.sub(r",", "", string)
        match = re.search(r"\d+", cleaned_string)
        if match:
            # 추출한 숫자 부분을 정수형으로 변환하여 반환
            return int(match.group())
        else:
            # 숫자가 없는 경우 None 반환
            return None

    def search_restaurants():
        driver.maximize_window()  # 화면 최대화
        driver.get("https://map.naver.com/")  # 네이버 지도 사이트 주소
        time.sleep(3)

        # 검색창 대기 및 찾기
        time_wait(10, "div.input_box > input.input_search")
        search = driver.find_element(
            By.CSS_SELECTOR, "div.input_box > input.input_search"
        )

        # 맛집 검색
        search.send_keys("광운대 맛집")
        search.send_keys(Keys.RETURN)
        time.sleep(3)

        # searchIframe 프레임으로 전환
        switch_frame("searchIframe")
        # 더 많은 식당을 얻기 위해 스크롤 다운
        # page_down(40) # 60개 식당임
        page_down(10)  # 20개 식당임
        time.sleep(3)

        # 크롤링 하려는 식당 개수 파악 위함
        restaurant_list = driver.find_elements(By.XPATH, "//li[@class='UEzoS rTjJo']")

        restaurants = dict()
        print("크롤링 시작")
        """
        프레임 전환
        searchIframe 에서 해당 식당 클릭 해야,
        entryIframe 이 생성되고 해당 식당에 대한 정보가 표시됩니다.
        """
        for i in range(len(restaurant_list)):
            # 프레임 초기화 및 searchIframe 프레임으로 전환
            driver.switch_to.default_content()
            switch_frame("searchIframe")

            print(f"----------{i + 1}/{len(restaurant_list)}번 째 식당----------")
            # i번 째 식당 클릭 위함
            name = restaurant_list[i].find_element(
                By.XPATH, ".//div[@class='place_bluelink N_KDL']"
            )  # 여긴 계속 바뀜 (수정 대상)
            for _ in range(2):
                name.click()

            # i번 째 식당의 정보를 크롤링하기 위함
            # 프레임 초기화 및 entryIframe 프레임으로 변경
            driver.switch_to.default_content()
            switch_frame("entryIframe")
            time.sleep(3)

            # 페이지 소스 가져오기 ------
            """
            일반적으로 entryIframe 의 탭 기본값은 "홈" 입니다.
            따라서 페이지 소스를 가져올 때, "홈" 탭의 페이지 소스가 가져와 집니다.

            예외) 첫 번째 식당의 entryIframe의 탭이 가끔 "홈"이 아닐 때가 존재합니다.
            """
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, "html.parser")  # "홈" 탭이 아닐 수 있음

            # 시작 시 "홈" 탭인지 확인 및 클릭
            """
            실제 "홈" 탭은 (탭 이동) 버튼 뒤에 위치합니다.
            따라서 (탭 이동) 버튼이 화면에 존재하면서 "홈" 탭으로 이동하고자 한다면, 
            (탭 이동) 버튼을 먼저 누른 후에 "홈" 탭을 클릭합니다.        
            """
            tabs = soup.find("div", class_="flicking-camera")
            # overlapping_element = soup.find('a', class_='PznE8')
            if tabs:
                tabs = driver.find_elements(By.XPATH, "//a[@class='tpj9w _tab-menu']")
                overlapping_element = driver.find_element(
                    By.CLASS_NAME, "PznE8"
                ).find_element(By.CLASS_NAME, "nK_aH")

                if (
                    overlapping_element.is_displayed()
                ):  # overlapping 이 화면에 있는 경우
                    overlapping_element.click()  # (탭 이동) 버튼 클릭
                    time.sleep(3)

                for tab in tabs:  # 탭 (홈, 소식(may not exist), 메뉴, 리뷰, 사진, 정보)
                    if tab.find_element(By.CLASS_NAME, "veBoZ").text.strip() == "홈":
                        tab.click()
                        time.sleep(3)

                        # "홈" 탭의 페이지 소스 가져오기
                        page_source = driver.page_source
                        soup = BeautifulSoup(page_source, "html.parser")
                        break

            # 식당 이름
            title = soup.find("span", class_="GHAhO").text.strip()
            print("식당 이름:", title)
            if title in restaurants.keys():
                continue
            else:
                restaurants[title] = []

            # 타입
            type = soup.find("span", class_="lnJFt").text.strip()
            type = f"타입: {type}"
            print(type)
            restaurants[title].append(type)

            # 별점
            rate = soup.find("span", class_="PXMot LXIwF")
            if rate:
                rate = float(rate.text[2:].strip())

            else:
                rate = None
            rate = f"평점: {rate}"
            print(rate)
            restaurants[title].append(rate)

            # 리뷰 총 수 (방문자 리뷰 수 + 블로그 리뷰 수)
            review_parent = soup.find("div", class_="dAsGb")
            if review_parent:
                review_types = review_parent.find_all("span", class_="PXMot")
                reviews_tot = 0
                for review_type in review_types:  # 방문자 리뷰 & 블로그 리뷰
                    review_type = review_type.find("a", {"role": "button"})
                    if review_type:  # 없을 수도 있기 때문
                        number = extract_number(review_type.text.strip())
                        if number is not None:
                            reviews_tot += number

            else:
                reviews_tot = None
            reviews_tot = f"리뷰 총 수: {reviews_tot}"
            print(reviews_tot)
            restaurants[title].append(reviews_tot)

            # 위치
            res_loc = soup.find("span", class_="LDgIH")
            if res_loc:
                res_loc = res_loc.text.strip()
            else:
                res_loc = None
            res_loc = f"위치: {res_loc}"
            print(res_loc)
            restaurants[title].append(res_loc)

            # 리뷰 표현 (n 명/ 총 방문자 수)
            """
            리뷰 탭으로 이동하여 방문자들의 리뷰 중 
            가장 많은 투표 수를 받은 표현,
            그 표현에 투표한 인원 수,
            참여한 모든 인원 수를 가져옵니다.
            """
            tabs = soup.find("div", class_="flicking-camera")
            exp = None
            if tabs:
                tabs = driver.find_elements(By.XPATH, "//a[@class='tpj9w _tab-menu']")
                for tab in tabs:  # 탭 (홈, 소식(may not exist), 메뉴, 리뷰, 사진, 정보)
                    if tab.find_element(By.CLASS_NAME, "veBoZ").text.strip() == "리뷰":
                        tab.click()  # "리뷰" 탭 클릭
                        time.sleep(3)
                        page_source = (
                            driver.page_source
                        )  # "리뷰" 탭 페이지 소스 가져오기
                        soup = BeautifulSoup(page_source, "html.parser")

                        # 가장 많은 투표 수를 받은 표현
                        expression = soup.find("span", class_="t3JSf")
                        if expression:
                            expression = expression.text.strip()
                        else:
                            expression = None

                        # 그 표현에 투표한 인원
                        expressed_num = soup.find("span", class_="CUoLy")
                        if expressed_num:
                            expressed_num = expressed_num.text.strip()
                        else:
                            expressed_num = None

                        # 방문자 총 인원
                        expressed_tot = soup.find("div", class_="jypaX")
                        if expressed_tot:
                            expressed_tot = expressed_tot.find("em").text.strip()
                        else:
                            expressed_tot = None
                        exp = f"{expression}: ({expressed_num}/{expressed_tot})"

            exp = f"리뷰 표현: {exp}"
            print(exp)
            restaurants[title].append(exp)

            # i 번째 식당 완료
            print(f"{i + 1}번째 식당 완료\n")

        # 정리
        print("----------Summary----------")
        print("총", len(restaurant_list), "개의 식당을 조회 하였습니다.")
        print("모든 식당 담은 딕셔너리: ", restaurants)

        return restaurants

    driver = webdriver.Chrome()
    restaurants = search_restaurants()
    driver.quit()  # 웹 드라이버 종료

    return restaurants


# 공지사항 카테고리 (광운대 사이트)-------------------------
def academic_info_kw():
    # 크롤링할 URL 설정
    url = "https://www.kw.ac.kr/ko/life/notice.jsp?srCategoryId=&mode=list&searchKey=1&searchVal="

    # 브라우저 User-Agent 설정
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    notices = [
        f"## {li.get_text(strip=True)}"
        for li in soup.find_all("li", class_="top-notice")
    ]
    notices = "\n\n".join(notices)
    return notices
