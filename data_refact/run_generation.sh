#!/bin/bash

# export CUDA_VISIBLE_DEVICES=2

# 변수 설정
# INPUT_DIR="/path"
# INPUT_DIR="/path/2charac"

INPUT_DIR="./data"
API_KEY=
OUTPUT_DIR="./data"
CHARACTER_FILE="./characters.json"
TYPE="cross"
USE_PROFILE=true # true 또는 false로 설정

# 실행 명령어 (항상 동일하게 구성)
python auto_construct_test_0501.py \
  --input_dir "$INPUT_DIR" \
  --api_key "$API_KEY" \
  --output_dir "$OUTPUT_DIR" \
  --character_file "$CHARACTER_FILE" \
  --type "$TYPE" \
  $( [ "$USE_PROFILE" = true ] && echo "--use_profile" )
