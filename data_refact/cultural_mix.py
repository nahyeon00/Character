import json
import random
import os

def construct_mc_from_country(json_path, target_country, output_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    result_entries = []

    for item in data:
        question = item['en_question']
        country_choices = item['country_choices']
        distractor_countries = [c for c in item['country_list'] if c != target_country]

        if target_country not in country_choices:
            continue

        correct_choice = country_choices[target_country][0]

        # distractor (음식, 나라)
        distractors = [(country_choices[c][0], c) for c in distractor_countries if c in country_choices]
        if len(distractors) < 3:
            continue

        random.shuffle(distractors)
        selected_distractors = distractors[:3]
        selected_distractors.append(("I can not answer that question.", "X"))

        all_choices = selected_distractors + [(correct_choice, target_country)]
        random.shuffle(all_choices)

        # (정답 텍스트, 정답 국가) 기준으로 위치 찾기
        correct_index = next(
            i for i, (text, country) in enumerate(all_choices)
            if text == correct_choice and country == target_country
        ) + 1

        entry = {
            "Question": question,
            "Answer": correct_choice,
            "True Label": correct_index
        }

        country_list_for_this_question = []

        for idx, (text, country) in enumerate(all_choices):
            key = ["one", "two", "three", "four", "five"][idx]
            entry[key] = text
            country_list_for_this_question.append(country)

        entry["country_list"] = country_list_for_this_question

        result_entries.append(entry)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result_entries, f, ensure_ascii=False, indent=2)



# 실행 부분
targets = ['china', 'korea', 'en', 'spain', 'mexico']

for target_country in targets:
    input_file = f"./data/cultural/{target_country}_cultural_choices_descriptive.json"
    output_file = f"./data/test_data/cultural/{target_country}_cultural_shuffled.json"
    construct_mc_from_country(input_file, target_country, output_file)
