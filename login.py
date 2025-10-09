from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
from selenium.common.exceptions import TimeoutException

URL = "https://finmate.site"
LOGIN_URL = URL + "/login"
TEST_ID = "test"      # 실제로는 여기에 ID 채우기
TEST_PW = "1234"

import os
from datetime import datetime

def save_artifacts(driver, prefix="finmate_error"):
    folder_name = "artifacts"
    os.makedirs(folder_name, exist_ok=True)  # 폴더 없으면 자동 생성

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_path = os.path.join(folder_name, f"{prefix}_{ts}.png")
    html_path = os.path.join(folder_name, f"{prefix}_{ts}.html")

    try:
        driver.save_screenshot(screenshot_path)
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        print(f"[저장 완료] {screenshot_path}, {html_path}")
    except Exception as e:
        print(f"[오류] 아티팩트 저장 실패: {e}")


def run_login(logger, timeout=5):
    logger.info("=== FinMate 로그인 자동화 시작 ===")

    if not TEST_ID:
        logger.warning("TEST_ID가 비어있음 → 로그인 시도 중단")
        # 로그인 안 해도 브라우저 띄워서 보여주기
        service = Service(ChromeDriverManager().install())
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(LOGIN_URL)
        input("로그인 화면 띄웠어요! 브라우저 닫으려면 Enter 누르세요...")
        driver.quit()
        return False

    driver = None
    try:
        service = Service(ChromeDriverManager().install())
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        driver = webdriver.Chrome(service=service, options=options)
        wait = WebDriverWait(driver, timeout)

        # 로그인 페이지 이동
        driver.get(LOGIN_URL)
        logger.info(f"로그인 페이지 접속: {LOGIN_URL}")

        # 로그인 폼 대기
        login_form_xpath = '//*[@id="app"]/div/div[1]/div[2]/div[1]/div/div/form'
        id_input_xpath = login_form_xpath + "/input[1]"
        pw_input_xpath = login_form_xpath + "/input[2]"
        wait.until(EC.presence_of_element_located((By.XPATH, id_input_xpath)))
        wait.until(EC.presence_of_element_located((By.XPATH, pw_input_xpath)))
        logger.info("로그인 폼 로드 확인")

        # 값 입력
        id_input = driver.find_element(By.XPATH, id_input_xpath)
        pw_input = driver.find_element(By.XPATH, pw_input_xpath)
        id_input.clear(); pw_input.clear()
        id_input.send_keys(TEST_ID)
        pw_input.send_keys(TEST_PW)

        # 로그인 버튼 클릭
        try:
            login_btn = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "login-button")))
        except TimeoutException:
            try:
                login_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]')))
            except TimeoutException:
                login_btn = driver.find_element(By.XPATH, "//button[contains(., '로그인')]")
        login_btn.click()
        logger.info("로그인 버튼 클릭 완료")

        # 로그인 성공/실패 판정
        try:
            wait.until_not(EC.presence_of_element_located((By.XPATH, login_form_xpath)))
            cur_url = driver.current_url.rstrip('/')
            logger.info(f"로그인 후 URL: {cur_url}")

            if cur_url == URL:
                logger.info("로그인 성공: 메인 페이지 이동")
                # 브라우저 유지
                input("✅ 로그인 성공! 브라우저 닫으려면 Enter 누르세요...")
                return True
            else:
                logger.warning("로그인 후 URL이 메인 아님 → 실패로 처리")
                save_artifacts(driver)
                input("❌ 로그인 실패 (화면 유지 중). Enter 누르면 닫힙니다...")
                return False

        except TimeoutException:
            logger.warning("로그인 폼이 여전히 존재함 → 로그인 실패로 판단")
            save_artifacts(driver)
            input("❌ 로그인 실패 (화면 유지 중). Enter 누르면 닫힙니다...")
            return False

    except Exception as ex:
        logger.error(f"로그인 중 예외 발생: {ex}")
        if driver:
            save_artifacts(driver)
        input("⚠️ 예외 발생. 브라우저 닫으려면 Enter 누르세요...")
        return False

    finally:
        if driver:
            driver.quit()
        logger.info("브라우저 종료")
