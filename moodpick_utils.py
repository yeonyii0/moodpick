# utils.py
from moodpick_constants import OTT_LIST
from moodpick_constants import mood_to_genres

def get_valid_ott_choices(user_input):
    choices = [i.strip() for i in user_input.split(",") if i.strip().isdigit()]
    selected_indexes = [int(i) for i in choices if 1 <= int(i) <= len(OTT_LIST)]
    return selected_indexes

def is_invalid_selection(input_list):
    # 정해진 범위 외 숫자가 포함되어 있는지 확인
    for val in input_list:
        if not val.isdigit() or not (1 <= int(val) <= len(OTT_LIST)):
            return True
    return False

def get_genre_codes_by_mood(mood_text):
    return mood_to_genres.get(mood_text, [])
