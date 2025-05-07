### cross_universe question 만들기

import json
import random
import pandas as pd

# 입력 JSON 파일 경로
character_file = "characters.json"

# 출력 엑셀 파일 경로
output_excel = "./data/korea_character_questions.xlsx"

# 질문 템플릿
templates = [
    "Do you know {name}?",
    "Have you heard of {name}?",
    "Have you met {name}?"
]

# 캐릭터 JSON 파일 로드
with open(character_file, 'r', encoding='utf-8') as f:
    characters = json.load(f)

# 질문 생성
rows = []
for character in characters:
    name = character["name"]
    profile = character["profile"]
    template = random.choice(templates)
    question = template.format(name=name)
    rows.append({
        "Question": question
    })

# 엑셀 파일로 저장
df = pd.DataFrame(rows)
df.to_excel(output_excel, index=False)

print(f"Saved to {output_excel}")
