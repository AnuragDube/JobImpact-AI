import streamlit as st
import pandas as pd
import plotly.express as px
from config.settings import APP_NAME
from utils.validators import validate_job_input
from modules.job_decomposition import decompose
from modules.task_classification import classify
from modules.skill_matching import match_skills
from modules.skills_gap import summarize_gaps
from modules.reskilling import make_roadmap
from modules.infographic import roadmap_png
from modules.responsible_ai import consistency_check

st.set_page_config(page_title=APP_NAME,page_icon="🧭",layout="wide",initial_sidebar_state="expanded")
st.markdown("""<style>
.stApp{background:#f6f8fc;color:#16243a}.block-container{padding-top:2rem;max-width:1440px}
[data-testid=stSidebar]{background:#101b31}.hero{padding:1.3rem 1.6rem;border-radius:18px;background:linear-gradient(120deg,#17294a,#3157a5);color:white;margin-bottom:1.2rem}
.hero h1{color:white;margin:0}.hero p{color:#d7e2ff;margin:.4rem 0 0}.small-muted{color:#65738a;font-size:.9rem}
</style>""",unsafe_allow_html=True)
st.sidebar.markdown("## 🧭 JobImpact AI")
page=st.sidebar.radio("Workspace",["Overview","Job Analyzer","Task Classification","Skills Gap","Reskilling Roadmap","Responsible AI","Technical About"])
st.sidebar.caption("P59 · Track E: Responsible AI")
if "analysis" not in st.session_state: st.session_state.analysis={}
state=st.session_state.analysis

def require_data():
    if not state.get("classifications"):
        st.info("Run a job analysis first in Job Analyzer."); return False
    return True

def run_analysis(raw,compare):
    job=validate_job_input(raw)
    state.pop("few_tasks",None)
    with st.spinner("Breaking the role into responsibilities…"):
        tasks,lat,source=decompose(job,False)
        if compare:
            few,flat,fsource=decompose(job,True); state.update(few_tasks=few,few_latency=flat,few_source=fsource)
        classified,clat,csource=classify(tasks)
        matches,engine=match_skills(tasks)
        gaps=summarize_gaps(matches)
        stages,rlat,rsource,priorities=make_roadmap(gaps)
    state.update(job=job,tasks=tasks,latency=lat,source=source,classifications=classified,class_latency=clat,class_source=csource,matches=matches,skill_engine=engine,gaps=gaps,stages=stages,roadmap_source=rsource,priorities=priorities,consistent=consistency_check(classified))
    st.success("Analysis complete. Review the mode labels and model explanations before using results.")

st.markdown(f'<div class="hero"><h1>{APP_NAME}</h1><p>Understand how AI may change work, task by task — with skills and human oversight in view.</p></div>',unsafe_allow_html=True)
if page=="Overview":
    st.subheader("Overview dashboard")
    if state.get("classifications"):
        df=pd.DataFrame(state["classifications"]); counts=df.label.value_counts().reindex(["Automate","Augment","Human-led"],fill_value=0).rename_axis("Exposure").reset_index(name="Tasks")
        a,b,c=st.columns(3); a.metric("Tasks analysed",len(df)); b.metric("Skill priorities",len(state.get("priorities",[]))); c.metric("Analysis mode", "Gemini" if "API" in state.get("class_source","") else "Demo")
        col1,col2=st.columns([1,1]); col1.plotly_chart(px.pie(counts,names="Exposure",values="Tasks",hole=.52,color="Exposure",color_discrete_map={"Automate":"#5b8def","Augment":"#f0aa45","Human-led":"#43a784"}),use_container_width=True); col2.plotly_chart(px.bar(counts,x="Exposure",y="Tasks",color="Exposure",color_discrete_map={"Automate":"#5b8def","Augment":"#f0aa45","Human-led":"#43a784"}),use_container_width=True)
        st.markdown("**Highest-priority skills**"); st.write(", ".join(state.get("priorities",[])))
        import json
        report=json.dumps({k:state.get(k) for k in ["job","tasks","source","classifications","class_source","matches","skill_engine","gaps","stages","roadmap_source","priorities","consistent"]},indent=2,ensure_ascii=False)
        st.download_button("Download analysis report (JSON)",report,"jobimpact_analysis.json","application/json")
        st.caption("Task exposure is an exploratory estimate, not a prediction that a job will disappear.")
    else:
        st.write("Start with a job title or job description. The workflow decomposes tasks, classifies exposure, matches skills, and builds a reskilling plan.")
        st.info("Without a Gemini key, the app uses clearly labelled illustrative demo outputs. Sentence-BERT is loaded locally when available.")
elif page=="Job Analyzer":
    st.subheader("Job Analyzer · U1")
    with st.form("job_form"):
        raw=st.text_area("Job title or description",height=170,placeholder="e.g., Data analyst responsible for validating datasets, building dashboards, and explaining findings…")
        compare=st.checkbox("Compare zero-shot and few-shot prompting",True)
        submitted=st.form_submit_button("Analyze job",type="primary")
    if submitted:
        try: run_analysis(raw,compare)
        except Exception as exc: st.error(str(exc))
    if state.get("tasks"):
        st.caption(f"Decomposition source: {state['source']}")
        st.code(__import__('modules.job_decomposition',fromlist=['decomposition_prompt']).decomposition_prompt(state['job']),language="text")
        st.dataframe(pd.DataFrame(state["tasks"]),use_container_width=True,hide_index=True)
        if state.get("few_tasks"):
            with st.expander("Few-shot output and comparison",expanded=True):
                from modules.job_decomposition import decomposition_prompt
                st.code(decomposition_prompt(state["job"],True),language="text")
                st.write(f"Few-shot source: {state['few_source']}")
                st.dataframe(pd.DataFrame(state["few_tasks"]),use_container_width=True,hide_index=True)
                st.metric("Task count difference",len(state["tasks"])-len(state["few_tasks"]))
elif page=="Task Classification":
    st.subheader("Task Classification · U2")
    if require_data():
        st.caption(f"Classification source: {state['class_source']}")
        st.dataframe(pd.DataFrame(state["classifications"]),use_container_width=True,hide_index=True)
        with st.expander("Prompt-based learning vs fine-tuning"):
            st.write("This application uses prompt-based inference through Gemini. It does not fine-tune model weights. Fine-tuning would require curated labelled examples, training, validation, and separate evaluation.")
elif page=="Skills Gap":
    st.subheader("Skills Gap Analysis · U3")
    if require_data():
        st.caption(f"Matching engine: {state['skill_engine']}. Similarity is semantic proximity, not a probability or competence score.")
        if state["gaps"]:
            choices=[x["skill"] for x in state["gaps"]]
            prof={s:st.slider(f"Self-rated proficiency · {s}",0,100,0,step=10,key="prof_"+s) for s in choices[:10]}
            gaps=summarize_gaps(state["matches"],prof); state["gaps"]=gaps
            st.dataframe(pd.DataFrame(gaps),use_container_width=True,hide_index=True)
        st.subheader("Task-to-skill matches")
        for row in state["matches"]:
            st.markdown(f"**{row['task']}**")
            st.write(" · ".join(f"{s['skill']} ({s['similarity']:.2f})" for s in row["skills"]))
elif page=="Reskilling Roadmap":
    st.subheader("Reskilling Roadmap · U4")
    if require_data():
        st.caption(f"Roadmap source: {state['roadmap_source']}")
        for stage in state["stages"]:
            with st.expander(f"{stage.get('stage','Stage')} · {stage.get('duration','')}",expanded=True):
                st.write("Goals: "+"; ".join(stage.get("goals",[]))); st.write(stage.get("practice",""))
        png=roadmap_png(state["stages"],state["priorities"],"Reskilling plan · "+state.get("job","Role")[:50])
        st.image(png,caption="Generated from the current analysis",use_container_width=True)
        st.download_button("Download roadmap infographic (PNG)",png,"jobimpact_roadmap.png","image/png")
elif page=="Responsible AI":
    st.subheader("Responsible AI & Bias Analysis · U5")
    if require_data():
        st.write("Structural consistency check"); st.json(state["consistent"])
    if st.button("Run controlled wording audit"):
        with st.spinner("Evaluating matched demographic wordings…"):
            from modules.responsible_ai import run_bias_audit
            state["bias_audit"]=run_bias_audit()
    if state.get("bias_audit"):
        st.dataframe(pd.DataFrame(state["bias_audit"]),use_container_width=True,hide_index=True)
        st.caption("This controlled probe is small and prompt-dependent; it does not establish population-level fairness. Demo mode uses simple rules and is not a model bias measurement.")
    with st.expander("Limitations, oversight and societal impact",expanded=True):
        st.write("Exposure labels describe task characteristics under a particular description and present tool capabilities. They do not forecast layoffs, wages, or adoption. Real outcomes depend on organization, regulation, access, and workflow redesign.")
        st.write("Job descriptions may contain personal or confidential information. Avoid pasting sensitive data; the app does not persist descriptions to a database, though Gemini requests are sent to Google when configured. Human review is necessary, especially for high-stakes roles.")
elif page=="Technical About":
    st.subheader("Technical Information")
    st.markdown("**Generative vs discriminative AI:** a generative model estimates patterns that can produce new sequences; a discriminative model learns to distinguish labels or outcomes. **Transformer attention:** token representations are combined using query–key relevance weights, helping the model condition on context. **GPT vs BERT:** GPT-style decoders generate autoregressively; BERT encoders contextualize tokens bidirectionally. Sentence-BERT encodes texts into vectors for similarity.")
    st.markdown("**Generation lifecycle:** frame the task → prompt/context → model inference → validate outputs → human review → iterate. The latent-space panel below is a conceptual normal distribution, not a visualization of Gemini's private internal state.")
    import numpy as np
    x=np.linspace(-3,3,250); y=np.exp(-x*x/2)/np.sqrt(2*np.pi)
    st.plotly_chart(px.area(x=x,y=y,labels={"x":"Latent variable (conceptual)","y":"Density"},title="Illustrative latent-variable distribution"),use_container_width=True)
    st.markdown("**PyTorch:** Sentence Transformers runs a pretrained transformer through its PyTorch backend where installed; this project does not train or fine-tune model weights.")

