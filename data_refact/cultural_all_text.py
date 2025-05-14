import json
import os
from tqdm import tqdm
from openai import OpenAI

# OpenAI API Key 설정 (환경변수 또는 직접 입력)
client = OpenAI(api_key="")

# 프롬프트 템플릿 로드
def load_prompt_template(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

# GPT-4를 이용해 보기 문장을 서술형으로 변환
def get_descriptive_sentence(prompt_template, country, item, question):
    # prompt = prompt_template.format(
    #     country=country.replace("_", " "),
    #     item=item,
    #     question=question
    # )

    prompt = prompt_template.format(
        item=item,
        question=question
    )

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )

    return response.choices[0].message.content.strip()

# 전체 JSON 처리
def process_json(input_path, output_path, prompt_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    prompt_template = load_prompt_template(prompt_path)

    for entry in tqdm(data):
        # print("before: ", entry)
        # print("\n")
        question = entry["en_question"]
        
        descriptive_choices = {}
        for country, items in entry["country_choices"].items():
            item = items[0]
            descriptive = get_descriptive_sentence(prompt_template, country, item, question)
            descriptive_choices[country] = [descriptive]

        # 기존 country_choices는 그대로 두고, 새로운 필드 추가
        entry["formatted_choices"] = descriptive_choices

        # print("after: ", entry)
        # assert 1 == 0  # 디버깅 중이면 유지하세요

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    # 파일 경로 설정
    targets = ['china', 'korea', 'en', 'spain', 'mexico']
    for target_country in targets:
        input_json_path = f"/path/{target_country}/{target_country}_cultural_choices.json"
        output_json_path = f"./data/cultural/{target_country}_cultural_choices_descriptive.json"
        prompt_txt_path = "./prompt/cultural_tolong.txt"

        process_json(input_json_path, output_json_path, prompt_txt_path)
