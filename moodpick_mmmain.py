# moodpick_mmmain.py

from moodpick_utils import get_genre_codes_by_mood 
from kino_scraper import scrape_kino, CONTENT_TYPES, CONTENT_TYPE_MAP
from moodpick_constants import OTT_LIST, MOODS, EXTRA_MOODS
from kino_scraper import scrape_kino

CHROMEDRIVER_PATH = r"C:\Users\82104\Desktop\moodpick\chromedriver.exe"

# 1. 사용자 이름 받기
username = input("당신의 이름 또는 닉네임을 알려주세요😊: ")

# 2. OTT 플랫폼 선택
print(f"\n🎥 {username}님께 최적화된 콘텐츠를 추천해드리기 위해,")
print("시청 가능한 OTT 플랫폼을 선택해주세요!\n")
for idx, p in enumerate(OTT_LIST, 1):
    print(f"{idx}. {p}")

while True:
    raw = input("\n해당 번호를 모두 입력해주세요\n*복수선택 가능해요 (예:1,3)*: ")
    inputs = [i.strip() for i in raw.split(",")]

    if not inputs or any(not i.isdigit() or not (1 <= int(i) <= len(OTT_LIST)) for i in inputs):
        print("\n⚠️ 숫자를 잘못 입력하셨어요.")
        print(f"1번 ~ {len(OTT_LIST)}번에서 골라 다시 입력해 주세요. 제가 기다리고 있을게요!😊")
        continue

    selected_indexes = [int(i) for i in inputs]

    if len(OTT_LIST) in selected_indexes:
        if len(selected_indexes) == 1:
            print("\n원하는 플랫폼이 목록에 없군요...")
            print("아쉽게 해드려서 정말 죄송합니다🙇")
            print("무드픽은 더 다양한 콘텐츠와 플랫폼을 담기 위해 열심히 준비 중이에요.")
            print("조금만 기다려주시면, 더 만족스러운 무드픽이 되어 돌아올게요 💙")
            exit()
        else:
            print("\n⚠️ 숫자를 잘못 입력하셨어요.")
            print(f"1번 ~ {len(OTT_LIST)-1}번 중에서 골라 다시 입력해 주세요. 제가 기다리고 있을게요!😊")
            continue

    selected_platforms = [OTT_LIST[i - 1] for i in selected_indexes]
    print(f"\n✅ {username}님이 선택한 OTT 플랫폼:")
    for p in selected_platforms:
        print(f"👉 {p}")
    break


# 콘텐츠 종류 선택
print("\n어떤 유형의 콘텐츠를 추천받고 싶으신가요?")
for idx, ct in enumerate(CONTENT_TYPES, 1):
    print(f"{idx}. {ct}")
    
while True:
    content_input = input("번호를 입력하세요: ").strip()
    if content_input.isdigit() and 1 <= int(content_input) <= len(CONTENT_TYPES):
        selected_text = CONTENT_TYPES[int(content_input) - 1]
        content_type = CONTENT_TYPE_MAP[selected_text]
        print(f"\n🎬 {username}님이 선택한 콘텐츠 유형:")
        print(f"👉 {selected_text}")
        break
    else:
        print("\n⚠️ 숫자를 잘못 입력하셨어요.")
        print(f"1번 ~ {len(CONTENT_TYPES)}번 중에서 골라 다시 입력해 주세요. 제가 기다리고 있을게요!😊\n")

# 감정 선택
print(f"\n지금부터 {username}님만을 위한 추천을 시작할게요.")
print("오늘은 어떤 기분이신가요? 😊\n")
for key, value in MOODS.items():
    print(f"{key}. {value}")

while True:
    mood_input = input("\n당신의 오늘 기분에 가장 가까운 번호를 입력해주세요: ")
    
    if mood_input in [str(i) for i in range(1, 11)]:
        selected_mood = MOODS[mood_input]
        print(f"\n{username}님의 오늘의 기분:")
        print(f"👉 {selected_mood}")
        if mood_input == "10":
            genres = []
        else:
            genres = get_genre_codes_by_mood(selected_mood)
        break

    elif mood_input == "11":
        print("\n💡 더 다양한 감정을 보여드릴까요?\n")
        for key, value in EXTRA_MOODS.items():
            print(f"{key}. {value}")

        while True:
            mood_input = input("\n1~26번 중 하나를 골라 입력해 주세요: ")
            if mood_input in MOODS:
                selected_mood = MOODS[mood_input]
            elif mood_input in EXTRA_MOODS:
                selected_mood = EXTRA_MOODS[mood_input]
            else:
                print("\n⚠️ 숫자를 잘못 입력하셨어요.")
                print("1번 ~ 26번 중에서 골라 다시 입력해 주세요. 제가 기다리고 있을게요!😊\n")
                continue

            print(f"\n{username}님의 오늘의 기분:")
            print(f"👉 {selected_mood}")
            genres = get_genre_codes_by_mood(selected_mood)
            break
        break
    else:
        print("\n⚠️ 숫자를 잘못 입력하셨어요.")
        print("1번 ~ 11번 중에서 골라 다시 입력해 주세요. 제가 기다리고 있을게요!😊")

# 크롬 드라이버 경로 지정 후 추천 실행
print(f"\n🔍 무드픽이 {username}님을 위한 추천 콘텐츠를 찾고 있어요... 잠시만 기다려 주세요!")
scrape_kino(
    chromedriver_path=CHROMEDRIVER_PATH,
    platforms=selected_platforms,
    content_type=content_type,
    genres=genres,
    username=username
)
