import os
import json
import argparse
import pandas as pd
from tqdm import tqdm
from openai import OpenAI
from transformers import AutoTokenizer, pipeline
import torch
import random


def load_template(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def load_characters(path):
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    names = [c["name"] for c in data]
    # profiles = [c["profile"] for c in data]
    profiles = [c["long"] for c in data]
    return names, profiles

def run_mc_evaluation(input_file_template, output_file_template, template_path, api_key, model_name, use_profile, names, profiles, eval_countries, eval_type):
    template = load_template(template_path)
    client = OpenAI(api_key=api_key)

    for i, name in enumerate(names):
        profile = profiles[i] if use_profile and profiles else ""

        countries = eval_countries if eval_type == "cultural" else [None]

        for country in countries:
            format_kwargs = {"name": name, "type": eval_type, "model": model_name}
            if country:
                format_kwargs["country"] = country

            input_file = input_file_template.format(**format_kwargs)
            df = pd.read_json(input_file)

            print(f"\nEvaluating: {name} - {country if country else eval_type}")
            result_data = []

            for idx, row in tqdm(df.iterrows(), total=len(df), desc=f"Evaluating for {name}", unit="questions"):
                question = row['Question']
                answer1 = row['one']
                answer2 = row['two']
                answer3 = row['three']
                answer4 = row['four']
                answer5 = row['five']

                if use_profile and profile:
                    prompt = template.format(
                        character=name,
                        profile=profile,
                        Question=question,
                        answer1=answer1,
                        answer2=answer2,
                        answer3=answer3,
                        answer4=answer4,
                        answer5=answer5,
                    )
                else:
                    prompt = template.format(
                        character=name,
                        Question=question,
                        answer1=answer1,
                        answer2=answer2,
                        answer3=answer3,
                        answer4=answer4,
                        answer5=answer5,
                    )

                messages = [
                    {"role": "system", "content": f"I want you to act like {name}"},
                    {"role": "user", "content": prompt},
                ]

                if "gpt" in model_name.lower():
                    outputs = client.chat.completions.create(
                        model=model_name,
                        messages=messages,
                        temperature=0.0,
                        max_tokens=512,
                        n=1,
                        top_p=0.95,
                    )
                    response = outputs.choices[0].message.content.strip()
                elif "llama" in model_name.lower():
                    pipe = pipeline("text-generation", model=model_name, model_kwargs={"torch_dtype": torch.bfloat16}, device_map="auto")
                    tokenizer = AutoTokenizer.from_pretrained(model_name)
                    terminators = [
                        tokenizer.eos_token_id,
                        tokenizer.convert_tokens_to_ids("<|eot_id|>")
                    ]
                    prompt_for_llama = f"System: I want you to act like {name}\nUser: {prompt}"
                    outputs = pipe(
                        prompt_for_llama,
                        max_new_tokens=512,
                        do_sample=True,
                        temperature=0.1,
                        top_p=0.2,
                        eos_token_id=terminators,
                    )
                    response = outputs[0]["generated_text"].strip()
                else:
                    raise ValueError("Unsupported model name.")

                model_answer = response.split("\n")[-1]

                result_data.append({
                    "Question": question,
                    "True Label": row['True Label'],
                    "one": answer1,
                    "two": answer2,
                    "three": answer3,
                    "four": answer4,
                    "five": answer5,
                    "gpt_result": response,
                    "model_answer": model_answer,
                })

            output_file = output_file_template.format(**format_kwargs)
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(result_data, f, ensure_ascii=False, indent=2)
            print(f"Results saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run GPT MC evaluation")
    parser.add_argument("--input_file", type=str, required=True, help="Path to JSON input file with {name}, {country}, etc.")
    parser.add_argument("--output_file", type=str, required=True, help="Output file template with {name}, {model}, and {type} or {country}")
    parser.add_argument("--template_path", type=str, required=True, help="Prompt template file path")
    parser.add_argument("--api_key", type=str, required=True, help="OpenAI API key")
    parser.add_argument("--model", type=str, default="gpt-4o", help="Model name")
    parser.add_argument("--type", type=str, required=True, help="Prefix for file naming (e.g., temporal, cultural, cross etc.)")
    parser.add_argument("--use_profile", action='store_true', help="Whether to use character profile")
    parser.add_argument("--character_file", type=str, default="", help="Path to character JSON if use_profile")
    parser.add_argument("--eval_countries", nargs='*', default=[], help="List of countries for cultural type")

    args = parser.parse_args()

    names = []
    profiles = []

    names, profiles = load_characters(args.character_file)
    # if args.use_profile:
    #     names, profiles = load_characters(args.character_file)
    # else:
    #     for file in os.listdir("./data/shuffled"):
    #         if file.endswith("_shuffled.json") and file.startswith(args.type):
    #             name = file.replace("_shuffled.json", "")
    #             names.append(name)
    #             profiles.append("")

    run_mc_evaluation(
        input_file_template=args.input_file,
        output_file_template=args.output_file,
        template_path=args.template_path,
        api_key=args.api_key,
        model_name=args.model,
        use_profile=args.use_profile,
        names=names,
        profiles=profiles,
        eval_countries=args.eval_countries,
        eval_type=args.type
    )
