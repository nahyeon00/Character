import os
import json
import argparse
import pandas as pd
import random
from tqdm import tqdm

def shuffle_mc_answers(input_file, output_file, name, type):
    if not os.path.exists(input_file):
        print(f"[Skip] File not found: {input_file}")
        return

    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    result_data = []

    for row in tqdm(data, desc=f"Shuffling - {name if name else 'NoProfile'}"):
        answer = row["Answer"]

        # 정답과 Incorrect Answer 9 또는 10은 반드시 포함
        fixed_choices = [answer]
        if type == "fact":
            fixed_choices.append(row["Incorrect Answer 9"])
        else:
            number = random.choice([9, 10])
            key = f"Incorrect Answer {number}"
            fixed_choices.append(row[key])  # 9 또는 10 중 하나 랜덤 포함(prompt3으로 만든 보기)

        # Incorrect Answer 1~4 중에서 하나, 5~8 중에서 하나 선택
        group1 = []
        group2 = []
        for i in range(1, 9):
            key = f"Incorrect Answer {i}"
            if key in row and row[key] not in fixed_choices:
                if i <= 4:
                    group1.append(row[key])
                else:
                    group2.append(row[key])

        sampled = []
        if group1:
            sampled.append(random.choice(group1))
        else:
            print(f"[Warn] No valid distractor in group1 for: {row['Question']}")
        if group2:
            sampled.append(random.choice(group2))
        else:
            print(f"[Warn] No valid distractor in group2 for: {row['Question']}")

        # 총 5개가 되도록 추가로 하나 더 뽑기 (남은 distractors에서)
        used_set = set(fixed_choices + sampled)
        remaining = [row[f"Incorrect Answer {i}"] for i in range(1, 9)
                     if f"Incorrect Answer {i}" in row and row[f"Incorrect Answer {i}"] not in used_set]

        if remaining:
            sampled.append(random.choice(remaining))
        else:
            print(f"[Warn] No remaining distractors to fill for: {row['Question']}")

        all_choices = fixed_choices + sampled
        random.shuffle(all_choices)

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
    parser.add_argument("--type", type=str, required=True, help="Prefix for file naming (e.g., temporal, cultural, cross etc.)")

    args = parser.parse_args()

    shuffle_mc_answers(args.input_file, args.output_file, args.name, args.type)
