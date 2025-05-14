### mutiple data로 만드는 코드

import os
import certifi

# OpenAI import 전에 SSL_CERT_FILE을 certifi로 덮어쓰기
os.environ["SSL_CERT_FILE"] = certifi.where()

import os
import json
import argparse
import pandas as pd
from tqdm import tqdm
from openai import OpenAI

def load_template(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def load_characters(path):
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    names = [c["name"] for c in data]
    profiles = [c["profile"] for c in data]
    return names, profiles

def query_gpt(prompt, model="gpt-4o", api_key=None):
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a plausible incorrect answer generator for multiple choice question datasets."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.0,
        max_tokens=512,
        top_p=0.95,
    )
    return response.choices[0].message.content.strip()

def generate_step1(input_dir, output_dir, api_key, names, profiles, type_name, use_profile):
    template_path = f"./prompt/neg1_{'profile' if use_profile else 'nonprofile'}.txt"
    print("tem:", template_path)
    template = load_template(template_path)

    for i in range(len(names)):
        name = names[i]
        profile = profiles[i]

        if type_name == 'fact':
            filename = f"{name}_FirstPerson_QA_English.xlsx"
        if type_name == 'temporal':
            filename = 'technology_questions.xlsx'
        if type_name == 'cross':
            filename = f'{name}_cross_questions.xlsx'

        input_file = os.path.join(input_dir, filename)
        df = pd.read_excel(input_file)

        result_data = []

        for _, row in tqdm(df.iterrows(), total=len(df), desc=f"Step1 - {name if use_profile else 'NoProfile'}"):
            answer = "I can not answer that question." if type_name.strip().lower() == "temporal" else row["Answer"]

            if use_profile:
                # print("1")
                prompt = template.format(
                    profile=profile,
                    Question=row["Question"],
                    Answer=answer
                )
            else:
                # print("2")
                prompt = template.format(
                    Question=row["Question"],
                    Answer=answer
                )

            raw_output = query_gpt(prompt, api_key=api_key)
            answers = [line.split(": ", 1)[1] for line in raw_output.split("\n") if line.startswith("Incorrect Answer")]
            answers += [""] * (4 - len(answers))

            result_data.append({
                "Question": row["Question"],
                "Answer": answer,
                "Incorrect Answer 1": answers[0],
                "Incorrect Answer 2": answers[1],
                "Incorrect Answer 3": answers[2],
                "Incorrect Answer 4": answers[3],
            })
            ## cross 일 경우 question에 자기 이름 들어가있으면 저장 제외

        filename = f"{name}_{type_name}_1.json" if use_profile else f"noprofile_{type_name}_1.json"
        output_path = os.path.join(output_dir, filename)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result_data, f, ensure_ascii=False, indent=2)
        print(f"Saved: {output_path}")

def generate_step2(input_dir, output_dir, api_key, names, profiles, type_name, use_profile):
    # print("step 3")
    template_path = f"./prompt/neg2_{'profile' if use_profile else 'nonprofile'}.txt"
    template = load_template(template_path)

    for i in range(len(names)):
        name = names[i]
        profile = profiles[i]
        filename = f"{name}_{type_name}_1.json" if use_profile else f"noprofile_{type_name}_1.json"
        input_file = os.path.join(input_dir, filename)
        df = pd.read_json(input_file)
        result_data = []

        for _, row in tqdm(df.iterrows(), total=len(df), desc=f"Step2 - {name if use_profile else 'NoProfile'}"):
            if use_profile:
                prompt = template.format(
                    profile=profile,
                    Question=row["Question"],
                    Answer=row["Answer"],
                    Incorrect1=row["Incorrect Answer 1"],
                    Incorrect2=row["Incorrect Answer 2"],
                    Incorrect3=row["Incorrect Answer 3"],
                    Incorrect4=row["Incorrect Answer 4"]
                )
            else:
                prompt = template.format(
                    Question=row["Question"],
                    Answer=row["Answer"],
                    Incorrect1=row["Incorrect Answer 1"],
                    Incorrect2=row["Incorrect Answer 2"],
                    Incorrect3=row["Incorrect Answer 3"],
                    Incorrect4=row["Incorrect Answer 4"]
                )

            raw_output = query_gpt(prompt, api_key=api_key)
            answers = [line.split(": ", 1)[1] for line in raw_output.split("\n") if line.startswith("Incorrect Answer")]
            answers += [""] * (4 - len(answers))

            entry = {
                "Question": row["Question"],
                "Answer": row["Answer"],
                "Incorrect Answer 1": row["Incorrect Answer 1"],
                "Incorrect Answer 2": row["Incorrect Answer 2"],
                "Incorrect Answer 3": row["Incorrect Answer 3"],
                "Incorrect Answer 4": row["Incorrect Answer 4"],
                "Incorrect Answer 5": answers[0],
                "Incorrect Answer 6": answers[1],
                "Incorrect Answer 7": answers[2],
                "Incorrect Answer 8": answers[3],
            }

            if type_name.strip().lower() == "fact":
                entry["Incorrect Answer 9"] = "I can not answer that question."

            result_data.append(entry)

        filename = f"{name}_{type_name}_2.json" if use_profile else f"noprofile_{type_name}_2.json"
        output_path = os.path.join(output_dir, filename)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result_data, f, ensure_ascii=False, indent=2)
        print(f"Saved: {output_path}")


def generate_step3(input_dir, output_dir, api_key, names, profiles, type_name, use_profile):
    if use_profile:
        template_path = f"./prompt/neg_3_profile.txt"
    else:
        template_path = f"./prompt/neg_3_nonprofile.txt"
    template = load_template(template_path)

    for i in range(len(names)):
        name = names[i]
        profile = profiles[i]
        filename = f"{name}_{type_name}_2.json" if use_profile else f"noprofile_{type_name}_2.json"
        input_file = os.path.join(input_dir, filename)
        df = pd.read_json(input_file)
        result_data = []

        for _, row in tqdm(df.iterrows(), total=len(df), desc=f"Step3 - {name if use_profile else 'NoProfile'}"):
            if use_profile:
                prompt = template.format(
                    profile=profile,
                    Question=row["Question"],
                    Answer=row["Answer"],
                )
            else:
                prompt = template.format(
                    Question=row["Question"],
                    Answer=row["Answer"],
                )

            raw_output = query_gpt(prompt, api_key=api_key)
            answers = [line.split(": ", 1)[1] for line in raw_output.split("\n") if line.startswith("Incorrect Answer")]
            answers += [""] * (2 - len(answers))

            entry = {
                "Question": row["Question"],
                "Answer": row["Answer"],
                "Incorrect Answer 1": row["Incorrect Answer 1"],
                "Incorrect Answer 2": row["Incorrect Answer 2"],
                "Incorrect Answer 3": row["Incorrect Answer 3"],
                "Incorrect Answer 4": row["Incorrect Answer 4"],
                "Incorrect Answer 5": row["Incorrect Answer 5"],
                "Incorrect Answer 6": row["Incorrect Answer 6"],
                "Incorrect Answer 7": row["Incorrect Answer 7"],
                "Incorrect Answer 8": row["Incorrect Answer 8"],
                "Incorrect Answer 9": answers[0],
                "Incorrect Answer 10": answers[1],
            }

            result_data.append(entry)

        filename = f"{name}_{type_name}_3.json" if use_profile else f"noprofile_{type_name}_3.json"
        output_path = os.path.join(output_dir, filename)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result_data, f, ensure_ascii=False, indent=2)
        print(f"Saved: {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate MC dataset using OpenAI GPT API.")
    parser.add_argument("--input_dir", type=str, required=True, help="Path to the input Excel file.")
    parser.add_argument("--api_key", type=str, required=True, help="Your OpenAI API key.")
    parser.add_argument("--output_dir", type=str, default="data", help="Directory to save output files.")
    parser.add_argument("--character_file", type=str, default="", help="Path to character JSON file.")
    parser.add_argument("--type", type=str, required=True, help="Prefix for file naming (e.g., temporal, cultural, cross etc.)")
    parser.add_argument("--use_profile", action="store_true", help="Whether to use character profiles")

    args = parser.parse_args()
    os.makedirs(args.output_dir, exist_ok=True)

    use_profile = args.use_profile
    print("main\n")

    if use_profile:
        # print("a :", use_profile)
        names, profiles = load_characters(args.character_file)
    else:
        # print("b :", use_profile)
        names = [""]
        profiles = [""]

    generate_step1(args.input_dir, args.output_dir, args.api_key, names, profiles, args.type, args.use_profile)
    generate_step2(args.output_dir, args.output_dir, args.api_key, names, profiles, args.type, use_profile)
    if args.type.strip().lower() != "fact":
        generate_step3(args.output_dir, args.output_dir, args.api_key, names, profiles, args.type, use_profile)
    
    print("done")
