from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime

BASE_URL = "https://finmate.site"
TEST_EMAIL = "test"
TEST_PASSWORD = "1234"

def save_artifacts(driver, prefix="finmate_error"):
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    driver.save_screenshot(f"{prefix}_{ts}.png")
    with open(f"{prefix}_{ts}.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)

def main():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    wait = WebDriverWait(driver, 10)

    try:
        # 1) 홈 → "로그인 하러 가기" 클릭
        driver.get(BASE_URL)
        btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".custom-login-button")))
        btn.click()

        # 2) 아이디/비번 입력
        email = wait.until(EC.visibility_of_element_located((
            By.XPATH, '//*[@id="app"]/div/div[1]/div[2]/div[1]/div/div/form/input[1]'
        )))
        email.clear()
        email.send_keys(TEST_EMAIL)

        pw_input = wait.until(EC.visibility_of_element_located((
            By.XPATH, '//*[@id="app"]/div/div[1]/div[2]/div[1]/div/div/form/input[2]'
        )))
        pw_input.clear()
        pw_input.send_keys(TEST_PASSWORD)

        # 3) 로그인 제출 버튼: 추정 셀렉터 → 없으면 실제 DOM 알려줘!
        #   우선 submit 버튼 공통 패턴 두 가지를 시도
        try:
            submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]')))
        except:
            # 텍스트 포함으로 대안
            submit = wait.until(EC.element_to_be_clickable((
                By.XPATH, "//button[contains(., '로그인')]"
            )))
        submit.click()

        # 4) 성공 판정(라우트/닉네임 노출 등 실제 기준으로 바꿔줘)
        wait.until(EC.any_of(
            EC.url_to_be(f"{BASE_URL}/"),
            EC.url_to_be(f"{BASE_URL}"),
            EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-testid='username']"))
        ))
        print("로그인 성공")

    except Exception as e:
        print(f"오류: {e}")
        save_artifacts(driver)
        raise
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
