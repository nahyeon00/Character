import os
import json
import argparse
import pandas as pd
import random
from tqdm import tqdm

def shuffle_mc_answers(input_file, output_file, name):
    if not os.path.exists(input_file):
        print(f"[Skip] File not found: {input_file}")
        return

    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    result_data = []

    for row in tqdm(data, desc=f"Shuffling - {name if name else 'NoProfile'}"):
        answer = row["Answer"]

        # 정답과 Incorrect Answer 9는 반드시 포함
        fixed_choices = [answer]
        if "Incorrect Answer 9" in row:
            fixed_choices.append(row["Incorrect Answer 9"])

        # 나머지 오답들 수집 (1~8번 중에서 이미 포함된 것은 제외)
        distractors = []
        for i in range(1, 8):
            key = f"Incorrect Answer {i}"
            if key in row and row[key] not in fixed_choices:
                distractors.append(row[key])

        # 무작위로 2개 선택하여 고정 보기와 합침
        if len(fixed_choices) == 2:            
            sampled = random.sample(distractors, 3)
            all_choices = fixed_choices + sampled
        else:
            sampled = random.sample(distractors, 4)
            all_choices = fixed_choices + sampled
            
        random.shuffle(all_choices)
        # if len(all_choices) < 4:
        #     print("error")
        correct_index = all_choices.index(answer) + 1

        entry = {
            "Question": row["Question"],
            "Answer": answer,
            "True Label": correct_index,
            "one": all_choices[0],
            "two": all_choices[1],
            "three": all_choices[2],
            "four": all_choices[3],
            "five": all_choices[4],
        }
        result_data.append(entry)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result_data, f, ensure_ascii=False, indent=2)
    print(f"Saved shuffled results to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_file", type=str, required=True, help="Path to input JSON file")
    parser.add_argument("--output_file", type=str, required=True, help="Path to output JSON file")
    parser.add_argument("--name", type=str, default="", help="Character name (optional for no-profile)")
    args = parser.parse_args()

    shuffle_mc_answers(args.input_file, args.output_file, args.name)
