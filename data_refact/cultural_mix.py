import json
import random
import os

ISO_MAP = {
    'china':  ['China'],
    'korea':  ['South_Korea'],
    'en':     ['US', 'UK'],   # 영어권: 미국(US)과 영국(UK)
    'spain':  ['Spain'],
    'mexico': ['Mexico'],
}


def construct_mc_from_country(json_path, target_country, output_path):
    iso_list = ISO_MAP.get(target_country)
    if not iso_list:
        raise ValueError(f"No ISO mapping for {target_country}")

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    result_entries = []
    for item in data:
        question = item['en_question']
        choices_map = item['country_choices']      # e.g. {'US': [...], 'CN': [...], ...}
        country_list = item['country_list']        # e.g. ['US','CN','KR',...]

        # 2) 정답 ISO 코드 찾기: 매핑 리스트 중 JSON 에 실제 있는 것
        available = [code for code in iso_list if code in choices_map]
        if not available:
            continue
        correct_code = available[0]
        correct_choice = choices_map[correct_code][0]

        # 3) distractor 후보: country_list 에서 en(US,UK) 모두 제외
        distractor_codes = [c for c in country_list if c not in iso_list]
        distractors = [
            (choices_map[c][0], c)
            for c in distractor_codes
            if c in choices_map
        ]
        if len(distractors) < 3:
            continue

        # 무작위 3개 뽑고, 모름 옵션 추가
        random.shuffle(distractors)
        selected = distractors[:3] + [("I can not answer that question.", "X")]

        # 정답 보기도 포함해 섞기
        all_choices = selected + [(correct_choice, correct_code)]
        random.shuffle(all_choices)

        # 1-based 정답 인덱스
        true_label = next(
            i for i,(text,code) in enumerate(all_choices, start=1)
            if code == correct_code and text == correct_choice
        )

        # entry 생성
        entry = {
            "Question":   question,
            "Answer":     correct_choice,
            "True Label": true_label
        }
        # one, two, three, four, five 에 텍스트 할당
        for idx,(text,code) in enumerate(all_choices):
            entry[["one","two","three","four","five"][idx]] = text

        # country_list 필드: 선택된 ISO 코드 순서대로
        entry["country_list"] = [code for _,code in all_choices]

        result_entries.append(entry)

    # 저장
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result_entries, f, ensure_ascii=False, indent=2)


# 실행 부분
targets = ['china', 'korea', 'en', 'spain', 'mexico']

for target_country in targets:
    input_file = f"./data/cultural/{target_country}_cultural_choices_descriptive.json"
    output_file = f"./data/test_data/cultural/{target_country}_cultural_shuffled.json"
    construct_mc_from_country(input_file, target_country, output_file)
