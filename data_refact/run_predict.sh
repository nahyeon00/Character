#!/bin/bash

# 설정
API_KEY=
MODEL_NAME="gpt-4o"
TEMPLATE_PATH="./prompt/mc_eval_template.txt"
CHARACTER_FILE="./characters.json"
TYPE="temporal"

# 캐릭터 (use_profile)
# python mc_eval.py \
#   --input_file "./data/shuffled/{name}_${TYPE}_shuffled.json" \
#   --output_file "./results/{name}_${MODEL_NAME}_${TYPE}_predict_long.json" \
#   --template_path "$TEMPLATE_PATH" \
#   --api_key "$API_KEY" \
#   --model "$MODEL_NAME" \
#   --type "$TYPE"  \
#   --use_profile \
#   --character_file "$CHARACTER_FILE"

## cultural

# 평가 타입 설정
# python mc_eval.py \
#   --input_file "./data/shuffled/{country}_cultural_shuffled.json" \
#   --output_file "./results/{name}_{model}_{country}_predict_long.json" \
#   --template_path "./prompt/mc_eval_template.txt" \
#   --api_key "$API_KEY" \
#   --model "$MODEL_NAME" \
#   --type "$TYPE" \
#   --use_profile \
#   --character_file "$CHARACTER_FILE" \
#   --eval_countries China South_Korea US

# # 템포럴 
python mc_eval.py \
  --input_file "./data/shuffled/no_profile_temporal_shuffled.json" \
  --output_file "./results/{name}_${MODEL_NAME}_${TYPE}_predict_long.json" \
  --template_path "$TEMPLATE_PATH" \
  --api_key "$API_KEY" \
  --model "$MODEL_NAME"\
  --type "$TYPE" \
  --use_profile \
  --character_file "$CHARACTER_FILE" \
