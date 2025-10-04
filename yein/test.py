import os
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# ===============================
# 테스트용 상수 (Config)
# ===============================
URL = "https://finmate.site/"
TEST_ID = "test"
TEST_PW = "1234"
LOG_DIR = "yein/logs"
LOG_FILE = "log.txt"


def setup_logger():
    # logs 폴더 생성
    log_dir = os.path.join(os.getcwd(), LOG_DIR)
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, LOG_FILE)

    # 로거 생성
    logger = logging.getLogger("finmate_logger")
    logger.setLevel(logging.INFO)

    # 포맷 지정
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")

    # 파일 핸들러
    fh = logging.FileHandler(log_file, encoding="utf-8")
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    # 콘솔 핸들러
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    return logger


def main():
    logger = setup_logger()

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    wait = WebDriverWait(driver, 10)

    # URL 접속
    driver.get(URL)
    logger.info("사이트 접속: %s", URL)

    # 로그인 버튼 클릭
    try:
        goLogin_btn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".custom-login-button"))
        )
        goLogin_btn.click()
        logger.info("로그인 버튼 클릭 성공!")
    except Exception as e:
        logger.error("로그인 버튼 클릭 실패: %s", e)

    # 아이디/비번 입력
    try:
        id_input = wait.until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="app"]/div/div[1]/div[2]/div[1]/div/div/form/input[1]')
        ))
        id_input.send_keys(TEST_ID)

        pw_input = driver.find_element(
            By.XPATH, '//*[@id="app"]/div/div[1]/div[2]/div[1]/div/div/form/input[2]'
        )
        pw_input.send_keys(TEST_PW)

        login_btn = driver.find_element(By.CLASS_NAME, "login-button")
        login_btn.click()
        logger.info("로그인 시도 완료!")

    except Exception as e:
        logger.error("로그인 실패: %s", e)

    input("종료하려면 엔터를 누르세요...")


if __name__ == "__main__":
    main()
