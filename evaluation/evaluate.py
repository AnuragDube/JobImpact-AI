"""Reproducible evaluation of the labelled reference set.

Usage: python -m evaluation.evaluate --demo
Without --demo, uses the configured Gemini API for predictions.
"""
import argparse, time
import pandas as pd
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from modules.task_classification import classify, demo_classify, LABELS

def evaluate(demo=False):
    df=pd.read_csv("evaluation/test_dataset.csv")
    pred=[]; started=time.perf_counter()
    for _,row in df.iterrows():
        result=demo_classify([{"task":row.task}]) if demo else classify([{"task":row.task}])[0]
        pred.append(result[0]["label"])
    latency=(time.perf_counter()-started)/len(df)
    print(f"Mode: {'rule-based demo (not Gemini)' if demo else 'Gemini API'}")
    print(f"Rows: {len(df)}")
    print(f"Accuracy: {accuracy_score(df.reference_label,pred):.4f}")
    print("Confusion matrix (true rows; predicted columns; order="+", ".join(LABELS)+"):")
    print(confusion_matrix(df.reference_label,pred,labels=LABELS))
    print(classification_report(df.reference_label,pred,labels=LABELS,zero_division=0))
    print(f"Mean wall-clock latency per row: {latency:.6f} seconds (includes local loop; no network in demo mode)")
    result_df=df.copy(); result_df["prediction"]=pred
    print("\nFailure cases:")
    print(result_df[result_df.reference_label!=result_df.prediction].to_string(index=False))

if __name__=="__main__":
    parser=argparse.ArgumentParser(); parser.add_argument("--demo",action="store_true"); args=parser.parse_args(); evaluate(args.demo)
