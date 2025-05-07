import os
import json
import pandas as pd
from sklearn.metrics import accuracy_score

def compute_accuracy_per_file(results_dir, output_excel_path):
    summary = []

    all_files = [f for f in os.listdir(results_dir) if f.endswith(".json")]

    for file in sorted(all_files):
        file_path = os.path.join(results_dir, file)
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        y_true = []
        y_pred = []

        for item in data:
            true_label = str(item.get("True Label")).strip()
            model_answer = str(item.get("model_answer")).strip()
            y_true.append(true_label)
            y_pred.append(model_answer)

        if y_true:
            acc = accuracy_score(y_true, y_pred)
            correct = sum([yt == yp for yt, yp in zip(y_true, y_pred)])
            total = len(y_true)
            summary.append({
                "file": file,
                "accuracy": round(acc * 100, 2),
                "correct": correct,
                "total": total
            })
            print(f"[{file}] Accuracy: {acc * 100:.2f}% ({correct}/{total})")
        else:
            print(f"[{file}] No valid data found.")

    # Save summary to Excel
    summary_df = pd.DataFrame(summary)
    os.makedirs(os.path.dirname(output_excel_path), exist_ok=True)
    summary_df.to_excel(output_excel_path, index=False)
    print(f"\n Accuracy summary saved to: {output_excel_path}")

# 예시 실행
results_dir = "/workspace/data_refact/results"
output_excel_path = os.path.join(results_dir, "accuracy_summary_2.xlsx")
compute_accuracy_per_file(results_dir, output_excel_path)
