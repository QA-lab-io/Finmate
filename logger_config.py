import os
import logging

def setup_logger(strLoggerName="finmate_logger"):
    # 로그 폴더 생성
    strLogDir = os.path.join(os.getcwd(), "yein", "logs")
    os.makedirs(strLogDir, exist_ok=True)

    # 로그 파일 경로
    strLogFile = os.path.join(strLogDir, "log.txt")

    # 로거 생성
    logger = logging.getLogger(strLoggerName)
    logger.setLevel(logging.INFO)

    # 중복 핸들러 방지
    if not logger.handlers:
        formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")

        # 파일 핸들러
        fh = logging.FileHandler(strLogFile, encoding="utf-8")
        fh.setFormatter(formatter)
        logger.addHandler(fh)

        # 콘솔 핸들러
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        logger.addHandler(ch)

    return logger
