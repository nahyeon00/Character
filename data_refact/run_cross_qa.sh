#!/bin/bash

INPUT_DIR="/path/characters"
COUNTRIES=("korea" "en" "china" "mexico" "spain")

for COUNTRY in "${COUNTRIES[@]}"
do
  echo "===== Generating cross-universe questions for $COUNTRY ====="
  OUTPUT_DIR="./data/cross_before/${COUNTRY}"
  
  python cross_qa.py \
    --country "$COUNTRY" \
    --input_dir "$INPUT_DIR" \
    --output_dir "$OUTPUT_DIR"

  echo "===== Done: $COUNTRY ====="
done
