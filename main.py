from logger_config import setup_logger
import login


def main():
    logger = setup_logger()
    logger.info("=== 프로그램 시작 ===")

    # 로그인 시도
    bLoginSuccess = login.run_login(logger)

    # 로그인 성공 시 찜 페이지 실행
    if bLoginSuccess:
        logger.info("로그인 성공")
        # heart.show_heart_page(logger)

    else:
        logger.warning("로그인 실패 → 프로그램 종료")

    logger.info("=== 프로그램 종료 ===")


if __name__ == "__main__":
    main()
