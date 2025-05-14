#!/bin/bash

# export CUDA_VISIBLE_DEVICES=2

# 공통 변수
API_KEY=""
OUTPUT_BASE="./data"
USE_PROFILE=true

# 반복할 국가 및 타입 목록
COUNTRIES=("korea" "en" "china" "mexico" "spain")
TYPES=("cross" "fact")

# 모든 타입과 국가 조합 실행
for TYPE in "${TYPES[@]}"
do
  echo "========== TYPE: $TYPE =========="

  for COUNTRY in "${COUNTRIES[@]}"
  do
    echo "===== Processing $COUNTRY for $TYPE ====="

    # 타입에 따라 INPUT_DIR 결정
    if [ "$TYPE" == "fact" ]; then
      INPUT_DIR="/path/$COUNTRY"
    elif [ "$TYPE" == "cross" ]; then
      INPUT_DIR="./data/cross_before/$COUNTRY"
    fi

    CHARACTER_FILE="/path/characters/${COUNTRY}_character.json"
    OUTPUT_DIR="${OUTPUT_BASE}/${TYPE}/${COUNTRY}"

    python auto_construct_test_0501.py \
      --country "$COUNTRY" \
      --input_dir "$INPUT_DIR" \
      --api_key "$API_KEY" \
      --output_dir "$OUTPUT_DIR" \
      --character_file "$CHARACTER_FILE" \
      --type "$TYPE" \
      $( [ "$USE_PROFILE" = true ] && echo "--use_profile" )

    echo "===== Done with $COUNTRY for $TYPE ====="
  done

  echo
done
