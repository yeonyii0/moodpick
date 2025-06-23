# kino_scraper.py

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# 플랫폼 이름 → 아이콘 클래스 매핑
PLATFORM_ICON = {
    "넷플릭스":   "kino-icon--netflix",
    "티빙":      "kino-icon--tving",
    "웨이브":    "kino-icon--wavve",
    "쿠팡플레이": "kino-icon--coupang-play",
    "디즈니+":   "kino-icon--disney",
    "라프텔":    "kino-icon--laftel"
}

# 지원 콘텐츠 종류 리스트
CONTENT_TYPES = ["영화", "드라마", "애니메이션", "예능","상관없어요"]

CONTENT_TYPE_MAP = {
    "영화": "영화",
    "드라마": "드라마",
    "애니메이션": "애니메이션",
    "예능": "예능",
    "상관없어요": "전체"
}

def scrape_kino(chromedriver_path, platforms, content_type, genres, username):
    opts = Options()
    opts.add_argument("--window-size=375,812")
    # opts.add_argument("--headless")

    driver = webdriver.Chrome(service=Service(chromedriver_path), options=opts)
    wait = WebDriverWait(driver, 10)
    driver.get("https://m.kinolights.com/discover/explore?hideBack=true")
    time.sleep(5)

    # 1) OTT 선택
    for plat in platforms:
        cls = PLATFORM_ICON.get(plat)
        if cls:
            driver.execute_script(
                f"document.querySelector('i.{cls}').parentElement.click();"
            )
            time.sleep(0.5)

    # 2) 콘텐츠 종류 탭 클릭 (예능 포함, 상관없어요는 클릭 X)
    if content_type in CONTENT_TYPES and content_type != "전체":
        try:
            tab = wait.until(EC.element_to_be_clickable((
                By.XPATH, f"//button[normalize-space()='{content_type}']"
            )))
            tab.click()
            time.sleep(0.5)
        except:
            print(f"⚠️ 콘텐츠 탭 클릭 실패: {content_type}")

    # 3) 장르 필터 열기 (예능 제외, 나머지 포함 + 상관없어요 포함)
    if content_type != "예능" and genres:
        try:
            modal = wait.until(EC.element_to_be_clickable((
                By.CSS_SELECTOR, "button[data-component-id='filterModalButton']"
            )))
            modal.click()
            time.sleep(1)

            for g in genres:
                try:
                    # 여러 방법으로 시도
                    selectors = [
                        f"//button[normalize-space()='{g}']",                    # 기본 방법
                        f"//button[.//span[normalize-space()='{g}']]",           # span 안의 텍스트
                        f"//button[contains(., '{g}')]",                         # 포함하는 텍스트
                        f"//span[normalize-space()='{g}']/parent::button"        # span에서 부모 버튼으로
                    ]
                    
                    clicked = False
                    for selector in selectors:
                        try:
                            btn = wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
                            btn.click()
                            print(f"✅ {g} 클릭 성공! (셀렉터: {selector})")
                            clicked = True
                            break
                        except:
                            continue
                    
                    if not clicked:
                        print(f"❌ {g} 클릭 실패")
                        
                    time.sleep(0.3)
                except:
                    print(f"⚠️ 장르 필터 실패: {g}")
                        
        except Exception as e:  # ← 이 except 블록이 누락되어 있었음
            print(f"모달 열기 실패: {e}")

    # 4) 전체 작품 보기 클릭
    if content_type != "예능" and genres:
        try:
            show_all = wait.until(EC.element_to_be_clickable((
                By.XPATH, "//span[contains(text(),'개의 작품 보기')]"
            )))
            show_all.click()
            time.sleep(2)
        except:
            print("⚠️ 작품 보기 클릭 실패")

    # 5) 결과 추출 및 출력
    import random

# 5) 결과 추출 및 출력
    cards = driver.find_elements(By.CSS_SELECTOR, "a[id^='contentPosterCard-']")
    if not cards:
        print("😥 선택하신 조건에 맞는 작품을 찾지 못했어요.")
    else:
        selected_cards = random.sample(cards[:20], min(5, len(cards)))

        print(f"\n🎁 {username}님을 위한 오늘의 추천작 5편입니다!\n")

        for idx, card in enumerate(selected_cards, 1):
            title = card.find_element(By.CSS_SELECTOR, "span.body__title").text
            try:
                score = card.find_element(By.CSS_SELECTOR, "span.score__number").text + "%"
            except:
                score = "N/A"
            print(f"{idx:3d}. {title}")


    driver.quit()