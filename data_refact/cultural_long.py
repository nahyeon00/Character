import os
import json
import pandas as pd
from tqdm import tqdm
from openai import OpenAI

def load_template(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def is_icna(text):
    """Check if the answer is a variation of 'I can not answer that question'."""
    return "i can not answer that question" in text.lower()

def construct_long(input_file, target_country, output_file):
    template = load_template("./prompt/cultural_long.txt")
    client = OpenAI(api_key="")

    df = pd.read_json(input_file)
    result_data = []

    for idx, row in tqdm(df.iterrows(), total=len(df), desc=f"{target_country}", unit="questions"):
        question = row['Question']
        answers = [row['one'], row['two'], row['three'], row['four'], row['five']]

        # "I can not answer that question" 위치 기록
        icna_idx = [i for i, ans in enumerate(answers) if is_icna(ans)]

        prompt = template.format(
            Question=question,
            one=answers[0],
            two=answers[1],
            three=answers[2],
            four=answers[3],
            five=answers[4],
        )

        messages = [
            {"role": "system", "content": "You are a multiple-choice rewriter."},
            {"role": "user", "content": prompt},
        ]

        # try:
        outputs = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            temperature=0.0,
            max_tokens=512,
            n=1,
            top_p=0.95,
        )
        response = outputs.choices[0].message.content.strip().split('\n')

        # 응답 파싱: 최대 5개 줄에서 "n: ..." 형식 추출
        rewritten_answers = [''] * 5
        line_count = 0
        for line in response:
            if ':' not in line:
                continue
            try:
                _, text = line.split(':', 1)
                rewritten_answers[line_count] = text.strip()
                line_count += 1
                if line_count >= 5:
                    break
            except Exception:
                continue

        # ICNA 위치는 원래 보기 유지
        for i in icna_idx:
            rewritten_answers[i] = "I can not answer that question"

        result_data.append({
            "Question": question,
            "Answer": row["Answer"],
            "True Label": row["True Label"],
            "one": row["one"],
            "two": row["two"],
            "three": row["three"],
            "four": row["four"],
            "five": row["five"],
            "rewritten_one": rewritten_answers[0],
            "rewritten_two": rewritten_answers[1],
            "rewritten_three": rewritten_answers[2],
            "rewritten_four": rewritten_answers[3],
            "rewritten_five": rewritten_answers[4],
            "country_list": row.get("country_list", [])
        })

    # 결과 저장
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result_data, f, indent=2, ensure_ascii=False)

# 실행 대상
targets = ['China', 'South_Korea', 'US']

for target_country in targets:
    input_file = f"./0511_data/shuffled/{target_country}_cultural_shuffled.json"
    output_file = f"./0511_data/shuffled/{target_country}_cultural_long_shuffled.json"
    construct_long(input_file, target_country, output_file)
