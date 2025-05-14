import json
import random
import pandas as pd
import os
import argparse

def generate_cross_universe_questions(country, input_dir, output_dir):
    # 입력 JSON 파일 경로
    character_file = os.path.join(input_dir, f"{country}_character.json")

    # 출력 디렉토리 생성
    os.makedirs(output_dir, exist_ok=True)

    # 질문 템플릿
    templates = [
        "Do you know {name}?",
        "Have you heard of {name}?",
        "Have you met {name}?"
    ]

    # 캐릭터 JSON 파일 로드
    with open(character_file, 'r', encoding='utf-8') as f:
        characters = json.load(f)

    for char in characters:
        rows = []
        for other in characters:
            if other["name"] == char["name"]:
                continue
            # 같은 history, 다른 time 페어만
            if other["history"] == char["history"] and other["time"] != char["time"]:
                q = random.choice(templates).format(name=other["name"])

                if (char["history"] == "real" and
                    char["time"] == "present" and
                    other["time"] == "past"):
                    a = f"I know about {char['profile']}."
                else:
                    a = "I can not answer that question."

                rows.append({
                    "Question": q,
                    "Answer": a
                })

        if rows:
            df = pd.DataFrame(rows)
            fname = f"{char['name']}_cross_questions.xlsx"
            df.to_excel(os.path.join(output_dir, fname), index=False)
            print(f"Saved to {os.path.join(output_dir, fname)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--country", default="korea", type=str,
                        help="choices: korea, china, us&uk, mexico, spain")
    parser.add_argument("--input_dir", type=str, required=True,
                        help="Directory where the character JSON file is located")
    parser.add_argument("--output_dir", type=str, default="./data/cross_before",
                        help="Directory where output files will be saved")
    args = parser.parse_args()

    generate_cross_universe_questions(args.country, args.input_dir, args.output_dir)
