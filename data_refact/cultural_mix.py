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

        # 정답
        correct_choice = country_choices[target_country][0]

        # 오답 후보 추출
        distractors = [country_choices[c][0] for c in distractor_countries]

        # 오답이 4개 미만이면 해당 항목 건너뜀
        if len(distractors) < 4:
            continue

        random.shuffle(distractors)
        selected_distractors = distractors[:4]

        # 보기 섞기
        all_choices = selected_distractors + [correct_choice]
        random.shuffle(all_choices)

        correct_index = all_choices.index(correct_choice) + 1  # 1-based index

        entry = {
            "Question": question,
            "Answer": correct_choice,
            "True Label": correct_index,
            "one": all_choices[0],
            "two": all_choices[1],
            "three": all_choices[2],
            "four": all_choices[3],
            "five": all_choices[4],
        }

        result_entries.append(entry)

    # JSON 저장
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result_entries, f, ensure_ascii=False, indent=2)



targets = ['China', 'South_Korea', 'US']
json_path = "/path"
file_name = "_cultural_choices.json"

for target_country in targets:
    input_file = os.path.join(json_path, f"{target_country}{file_name}")
    output_file = f"./data/shuffled/{target_country}_cultural_shuffled.json"
    construct_mc_from_country(input_file, target_country, output_file)
