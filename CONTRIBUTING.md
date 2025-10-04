#  날짜 + Conventional Commits 규칙

```
YYMMDD_<type>: <description>
```

---

## 🔑 주요 예시

### feat (새로운 기능)
- `251004_feat: 로그인 자동화 코드 구현`
- `251004_feat: 로그인 시나리오 테스트 케이스 작성`

### fix (버그 수정)
- `251004_fix: 비밀번호 입력 오류 수정`
- `251004_fix: 로그인 버튼 클릭 시 예외 처리 추가`

### docs (문서)
- `251004_docs: 요소 선택자 정리 문서 추가`
- `251004_docs: 실행 방법 가이드 업데이트`

### chore (환경/기타)
- `251004_chore: selenium_locator_guide.md → selenium_locator_guide_with_devtools.md 파일명 변경`
- `251004_chore: requirements.txt 패키지 버전 업데이트`

### refactor (리팩터링)
- `251004_refactor: 로거 설정 함수 구조 개선`
- `251004_refactor: 중복된 XPath 코드 정리`

---

## ✅ 권장 포맷
- 날짜는 **(YYMMDD)** 사용 → 정렬이 편리함
- 타입은 **Conventional Commits 규칙** 따르기
- 한 커밋은 **한 가지 의미만** 담을 것

---

## 📌 최종 템플릿

```
YYMMDD_<type>: <description>
```

예:  
```
251004_feat: Selenium 로그인 자동화 기능 추가
```

# 브랜치 관리 규칙

## 1. 기본 브랜치 전략
- **main**  
  - QA 자동화 스크립트를 모아두는 **대표 브랜치**  
---

## 2. 작업 브랜치 네이밍 규칙
포트폴리오 용도로는 **간단한 브랜치 네이밍**만 사용합니다.

| 브랜치 타입   | 설명 | 예시 |
|--------------|------|------|
| **main**     | 최종 QA 자동화 스크립트 저장소 | `main` |
| **feature/** | 새로운 테스트 시나리오 추가 | `feature/login-test-case` |
| **fix/**     | 깨진 테스트 코드/스크립트 수정 | `fix/login-wait` |
| **docs/**    | README, 가이드 등 문서 업데이트 | `docs/update-readme` |

---

## 3. 브랜치 작업 플로우
1. **새로운 기능 추가**  
   ```bash
   git checkout -b feature/login-test-case main
   ```

2. **작업 후 커밋 (날짜 + Conventional Commits 규칙 적용)**  
   ```bash
   251004_feat: 로그인 자동화 시나리오 추가
   ```

3. **main에 병합**  
   ```bash
   git checkout main
   git merge feature/login-test-case
   ```

4. **브랜치 정리**  
   ```bash
   git branch -d feature/login-test-case
   ```

---

## ✅ 정리
- 필요 시 `feature/`, `fix/`, `docs/` 브랜치만 가볍게 사용  
- 복잡한 Git Flow(`develop`, `release`)는 불필요  
- 커밋 메시지는 `YYMMDD type: 설명` 규칙으로 작성  
---

📌 예시 커밋
```
251004_feat: 로그인 자동화 시나리오 추가
251004_fix: 로그인 버튼 클릭 타임아웃 수정
251004_docs: 실행 방법 README 업데이트
```
