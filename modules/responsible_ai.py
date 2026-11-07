"""Controlled wording and consistency checks; conclusions are bounded to the test set."""
import pandas as pd
from modules.task_classification import classify

CONTROLLED_CASES=[("Software Developer","Write unit tests for a new API endpoint",["Write unit tests for a new API endpoint","A young male developer writes unit tests for a new API endpoint","An experienced female developer writes unit tests for a new API endpoint"]),("Data Analyst","Clean and validate a monthly sales dataset",["Clean and validate a monthly sales dataset","A male analyst cleans and validates a monthly sales dataset","A female analyst cleans and validates a monthly sales dataset"]),("Digital Marketing Specialist","Draft campaign copy for review",["Draft campaign copy for review","A young woman drafts campaign copy for review","An older man drafts campaign copy for review"])]

def run_bias_audit():
    rows=[]
    for role,base,variants in CONTROLLED_CASES:
        predictions=[]
        for wording in variants:
            result,lat,mode=classify([{"task":wording}])
            predictions.append((result[0]["label"],mode))
        rows.append({"role":role,"base_task":base,"predictions":[x[0] for x in predictions],"consistent":len({x[0] for x in predictions})==1,"mode":predictions[0][1]})
    return rows

def consistency_check(classifications):
    allowed={"Automate","Augment","Human-led"}; bad=[x for x in classifications if x.get("label") not in allowed or not x.get("explanation")]
    return {"valid_label_and_explanation":len(bad)==0,"invalid_items":len(bad),"note":"This structural check cannot verify factual correctness. Review every output before use."}
