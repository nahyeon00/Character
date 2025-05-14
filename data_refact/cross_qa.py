import json
import random
import pandas as pd
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--country", default="korea", type=str,
                    help="choices : korea, china, us&uk, mexico, spain")
args = parser.parse_args()

# 입력 JSON 파일 경로
character_file = f"{args.country}_character.json"

# 출력 디렉토리
output_dir = "./data"
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
            # 질문 생성
            q = random.choice(templates).format(name=other["name"])
            # 답변: char가 real-present, other가 real-past인 경우에만 I know
            if (char["history"] == "real" and
                char["time"]    == "present" and
                other["time"]   == "past"):
                a = f"I know about {char['profile']}."
            else:
                a = "I can not answer that question."

            rows.append({
                "Question": q,
                "Answer"  : a
            })

    if rows:
        df = pd.DataFrame(rows)
        fname = f"{char['name']}_cross_questions.xlsx"
        df.to_excel(os.path.join(output_dir, fname), index=False)
        print(f"Saved to {os.path.join(output_dir, fname)}")
