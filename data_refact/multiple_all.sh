#!/bin/bash
set -e  # 에러 발생 시 중단

echo "Step 1: run_cross_qa.sh"
bash run_cross_qa.sh
echo "Done: run_cross_qa.sh"
echo

echo "Step 2: run_generation_factcross.sh"
bash run_generation_factcross.sh
echo "Done: run_generation_factcross.sh"
echo

echo "Step 3: run_generation_temporal.sh"
bash run_generation_temporal.sh
echo "Done: run_generation_temporal.sh"
echo

echo "Step 4: cultural_all_text.py"
python cultural_all_text.py
echo "Done: cultural_all_text.py"
echo

echo "Step 5: cultural_mix.py"
python cultural_mix.py
echo "Done: cultural_mix.py"
echo

echo "All steps completed successfully!"
