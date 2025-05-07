#!/bin/bash

# 입력 디렉토리와 출력 디렉토리 설정
INPUT_DIR="./data"
OUTPUT_DIR="./data/shuffled"

# 디렉토리가 없으면 생성
mkdir -p "$OUTPUT_DIR"

# 처리할 파일 자동 감지
for FILE in "$INPUT_DIR"/*_2.json; do
  FILENAME=$(basename "$FILE")
  OUTPUT_PATH="$OUTPUT_DIR/${FILENAME/_2.json/_shuffled.json}"

  # 캐릭터 이름 추출 (no_profile이면 이름 없음)
  if [[ "$FILENAME" == no_profile* ]]; then
    NAME=""
  else
    NAME="${FILENAME%%_*}"
  fi

  echo "Processing $FILENAME as character: ${NAME:-NoProfile}"
  python shuffle_mc.py \
    --input_file "$FILE" \
    --output_file "$OUTPUT_PATH" \
    --name "$NAME"
done
