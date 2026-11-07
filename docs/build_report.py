"""Create the student submission PDF with executed demo-mode evaluation metrics."""
import sys
import time
import textwrap
from pathlib import Path
import pandas as pd
from sklearn.metrics import accuracy_score, confusion_matrix
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from modules.task_classification import demo_classify, LABELS

OUT=ROOT/"59_Anurag_Chotulal_Dube"/"59_Anurag_Chotulal_Dube_P59.pdf"

def page(pdf,title,paragraphs):
    fig=plt.figure(figsize=(8.27,11.69),facecolor="white")
    fig.text(.08,.94,title,fontsize=20,fontweight="bold",color="#17294a",va="top")
    y=.88
    for heading,body in paragraphs:
        fig.text(.08,y,heading,fontsize=12,fontweight="bold",color="#3157a5",va="top"); y-=.026
        for line in body.split("\n"):
            for wrapped in textwrap.wrap(line,width=88) or [""]:
                fig.text(.08,y,wrapped,fontsize=9.5,color="#263449",va="top"); y-=.021
            if y<.07: break
        y-=.02
    fig.text(.08,.035,f"JobImpact AI · P59 · Educational analysis; human review required · Page {pdf.get_pagecount()+1}",fontsize=8,color="#69778b")
    pdf.savefig(fig); plt.close(fig)

def architecture_page(pdf):
    fig=plt.figure(figsize=(8.27,11.69),facecolor="white")
    ax=fig.add_axes([0,0,1,1]); ax.set_axis_off()
    fig.text(.08,.94,"System architecture",fontsize=20,fontweight="bold",color="#17294a",va="top")
    nodes=[("1 · Role input","Job title or description; bounded validation"),("2 · Job decomposition","Gemini zero-shot and few-shot prompts"),("3 · Task exposure","Automate · Augment · Human-led with explanations"),("4 · Skills matching","Sentence-BERT embeddings and similarity scores"),("5 · Skills gap and roadmap","Self-rating, learning stages, generated infographic"),("6 · Responsible AI","Wording probes, output checks, privacy and human review")]
    ys=[.82,.69,.56,.43,.30,.17]
    for idx,((title,sub),y) in enumerate(zip(nodes,ys)):
        fig.text(.18,y,title,fontsize=12,fontweight="bold",color="#17294a",ha="left",va="center",bbox=dict(boxstyle="round,pad=.65",facecolor="#eaf0ff" if idx%2==0 else "#edf7f4",edgecolor="#9eb5e8"))
        fig.text(.52,y,sub,fontsize=9,color="#34445b",ha="left",va="center")
        if idx < len(nodes)-1:
            ax.annotate("",xy=(.14,ys[idx+1]+.04),xytext=(.14,y-.04),xycoords="axes fraction",arrowprops=dict(arrowstyle="->",color="#4263eb",lw=1.6))
    fig.text(.08,.035,f"JobImpact AI · P59 · Educational analysis; human review required · Page {pdf.get_pagecount()+1}",fontsize=8,color="#69778b")
    pdf.savefig(fig); plt.close(fig)

def build():
    df=pd.read_csv(ROOT/"evaluation"/"test_dataset.csv")
    started=time.perf_counter()
    pred=[demo_classify([{"task":t}])[0]["label"] for t in df.task]
    latency=(time.perf_counter()-started)/len(df)
    acc=accuracy_score(df.reference_label,pred); cm=confusion_matrix(df.reference_label,pred,labels=LABELS)
    OUT.parent.mkdir(parents=True,exist_ok=True)
    with PdfPages(OUT) as pdf:
        page(pdf,"JobImpact AI | P59",[("Job Task Exposure Analyzer","Track E: Responsible AI\nAnurag Chotulal Dube · Roll 59\nMIT ADT University · B.Tech Computer Science Engineering"),("Objective","Break a job into responsibilities, assess task exposure, identify related skills and outline reskilling steps. This is educational decision support, not an employment prediction tool."),("Problem statement","AI affects tasks differently. Routine repeatable work may be automated; some work is augmented by tools; contextual judgment, empathy, accountability, and physical work often remain human-led."),("Scope","The project implements task decomposition, exposure classification, semantic skill matching, proficiency self-assessment, roadmap generation, dynamic infographic generation, and controlled responsible-AI probes.")])
        page(pdf,"Tools and model status",[("Technology","Python, Streamlit, Gemini API (optional), Sentence-BERT all-MiniLM-L6-v2, PyTorch runtime, Pandas, NumPy, scikit-learn, Plotly, Matplotlib and Pillow."),("Data","The evaluation CSV contains 19 manually labelled educational examples across Software Developer, Data Analyst and Digital Marketing Specialist. It is a small classroom reference set, not occupational ground truth."),("Model status","No model fine-tuning is performed or claimed. Without Gemini credentials, clearly labelled illustrative fallbacks are used. Sentence-BERT may fall back to TF-IDF if the model cannot load.")])
        architecture_page(pdf)
        page(pdf,"Implementation and responsible use",[("U1–U2","Prompt comparison shows zero-shot versus few-shot decomposition. Classification uses task-level categories: Automate, Augment, and Human-led, with explanations. Prompting is inference; fine-tuning would need training data and validation."),("U3–U4","Sentence embeddings match responsibilities to a structured skill vocabulary. Similarity is semantic proximity, not a probability or proficiency. Self-ratings inform priorities; a staged plan and image are generated from analysis results."),("U5","Controlled demographic wording probes detect changes in model output on a tiny set; they cannot certify fairness. Structural checks confirm allowed labels and explanations, not factual correctness."),("Privacy and oversight","Descriptions are not stored in an application database. With Gemini configured, entered text is sent to Google's API. Avoid personal or confidential details. A human must review all outputs; do not use the system for employment decisions."),("Limitations","Role descriptions omit context; skills list is incomplete; models can hallucinate; API model availability changes; similarity and exposure are not calibrated. The system does not forecast layoffs, adoption, or wages.")])
        page(pdf,"Executed evaluation results",[("Run mode","Rule-based illustrative demo fallback (not Gemini). Executed against the manually labelled educational set."),("Dataset and accuracy",f"{len(df)} examples; {acc:.4f} ({acc*100:.2f}%) accuracy on this small educational dataset."),("Mean latency",f"{latency:.6f} seconds per row (local demo loop; excludes UI and network). Not a Gemini inference latency."),("Confusion matrix","Rows: reference labels; columns: predictions; order: "+", ".join(LABELS)+"\n"+str(cm)),("Failure examples","".join(f"{r.role}: {r.task} — expected {r.reference_label}, got {p}.\n" for (_,r),p in zip(df.iterrows(),pred) if r.reference_label!=p)[:1300]),("Interpretation","This measures only the simple demo rules against hand-labelled examples developed with the project, not Gemini or Sentence-BERT performance. Results are not statistically representative and should not be generalized.")])
        page(pdf,"Conclusion and demonstration evidence",[("Conclusion","JobImpact AI demonstrates an end-to-end, task-level educational workflow from role input to exposure analysis, skill gaps, and reskilling support. Keeping assumptions visible and requiring human review are core design decisions."),("Screenshots","No screenshots are included because a full Streamlit runtime was unavailable during this build session. Capture genuine screenshots after installing dependencies and running the application."),("Repository","Git repository initialized locally. GitHub URL and live deployment: not created or verified."),("Next steps","Install dependencies in Python 3.11, configure Gemini secret if desired, run every page, capture genuine screenshots, execute both live and fallback evaluations, and update this report with final runtime/model details.")])
    print(OUT)
    print(f"Rows={len(df)}; demo accuracy={acc:.4f}; confusion_matrix={cm.tolist()}")

if __name__=="__main__": build()
