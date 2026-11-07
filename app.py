"""JobImpact AI: task exposure, skills and reskilling workspace."""
import html
import json
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

from config.settings import APP_NAME, GEMINI_MODEL
from utils.validators import validate_job_input
from modules.job_decomposition import decompose, decomposition_prompt
from modules.task_classification import classify
from modules.skill_matching import match_skills
from modules.skills_gap import summarize_gaps
from modules.reskilling import make_roadmap
from modules.infographic import roadmap_png
from modules.responsible_ai import consistency_check

st.set_page_config(page_title=APP_NAME, page_icon="✳️", layout="wide", initial_sidebar_state="expanded")
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap');
:root{--ink:#162238;--muted:#68758b;--line:#e4e9f1;--paper:#f5f7fb;--blue:#5269e8}
html,body,[class*="css"]{font-family:'DM Sans',sans-serif;color:var(--ink)}
.stApp{background:var(--paper)} [data-testid="stHeader"]{background:rgba(245,247,251,.85);height:2.8rem}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#111c31,#15233d);border-right:1px solid #ffffff12}
[data-testid="stSidebar"] *{color:#e8edf7} [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p{color:#aab6ca}
[data-testid="stSidebar"] [data-testid="stRadio"] label{padding:.45rem .6rem;border-radius:9px;font-weight:500}
[data-testid="stSidebar"] [data-testid="stRadio"] label:hover{background:#ffffff12}
.block-container{max-width:1400px;padding:1.25rem 2.2rem 4rem}
h1,h2,h3{font-family:'Manrope',sans-serif;letter-spacing:-.035em;color:var(--ink)}
.brand{display:flex;align-items:center;gap:12px;padding:.3rem .15rem 1.4rem}
.brand-mark{width:40px;height:40px;display:grid;place-items:center;border-radius:13px;background:linear-gradient(135deg,#6979ff,#45c7b2);font-size:21px}
.brand-name{font:800 18px 'Manrope',sans-serif;color:#fff}.brand-sub{font-size:10px;color:#98a7be;margin-top:2px;letter-spacing:.1em;text-transform:uppercase}
.side-label{color:#71819d!important;font-size:10px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;margin:1rem 0 .25rem}
.status-pill{display:inline-flex;align-items:center;gap:7px;border-radius:99px;padding:6px 10px;background:#e9f7f3;color:#147f68;font-size:11px;font-weight:700}
.status-dot{width:7px;height:7px;border-radius:50%;background:#31b78d}
.topline{display:flex;justify-content:space-between;margin:0 0 1rem;color:#77849a;font-size:12px}
.hero{position:relative;overflow:hidden;border:1px solid #263956;border-radius:22px;background:radial-gradient(ellipse at 86% 2%,#394d91 0,transparent 34%),linear-gradient(125deg,#17243c,#1b2e50 58%,#243764);padding:2rem 2.1rem;color:white;box-shadow:0 18px 44px #19274420;margin-bottom:1.35rem}
.hero:after{content:'';position:absolute;width:220px;height:220px;border-radius:50%;border:1px solid #ffffff14;right:5%;top:12%;box-shadow:0 0 0 28px #ffffff08,0 0 0 58px #ffffff05}
.hero-kicker{font-size:10px;letter-spacing:.14em;text-transform:uppercase;font-weight:700;color:#99e4d5;margin-bottom:.7rem}
.hero-title{font:800 clamp(27px,3vw,40px)/1.12 'Manrope',sans-serif;color:#fff;letter-spacing:-.045em;margin:0;position:relative;z-index:1}
.hero-copy{font-size:14px;line-height:1.65;color:#cad5e9;max-width:720px;margin:.7rem 0 0;position:relative;z-index:1}
.hero-tags{display:flex;gap:8px;flex-wrap:wrap;margin-top:1.1rem;position:relative;z-index:1}.hero-tag{font-size:10px;color:#d9e4f5;border:1px solid #ffffff25;border-radius:99px;padding:6px 10px;background:#ffffff0b}
.section-head{margin:1.25rem 0 .75rem}.section-title{font:700 18px 'Manrope',sans-serif;color:var(--ink)}.section-sub{font-size:12px;color:var(--muted);margin-top:3px}
.panel,.metric-card,.task-row{background:#fff;border:1px solid var(--line);border-radius:15px;box-shadow:0 4px 18px #26395908}
.panel{padding:1rem 1.1rem}.metric-card{padding:14px 16px;min-height:92px}.metric-label{font-size:10px;letter-spacing:.09em;text-transform:uppercase;color:#77849a;font-weight:700}
.metric-value{font:800 26px 'Manrope',sans-serif;color:#17243c;margin-top:6px}.metric-note,.small-note{font-size:11px;color:#8792a4;line-height:1.55}
.task-row{padding:13px 15px;margin:8px 0;color:#26344a!important}.task-row b{color:#26344a!important}.task-row span:first-child{color:#7380a0!important}.badge{display:inline-flex;padding:5px 9px;border-radius:99px;font-size:10px;font-weight:700;white-space:nowrap}
.badge-auto{background:#eaf0ff;color:#425bc8}.badge-augment{background:#fff3dd;color:#a86c13}.badge-human{background:#e7f7f1;color:#168365}
div.stButton>button,div.stFormSubmitButton>button{border-radius:10px;border:1px solid #5269e8;background:#5269e8;color:white;font-weight:700;min-height:42px;box-shadow:0 6px 14px #5269e82b}
div.stButton>button:hover,div.stFormSubmitButton>button:hover{border-color:#4057d4;background:#4057d4;color:white;transform:translateY(-1px)}
div[data-testid="stDownloadButton"]>button{border-radius:10px;font-weight:700}
div[data-testid="stDownloadButton"]>button{background:#5269e8!important;color:#fff!important;border-color:#5269e8!important}
div[data-testid="stTextArea"] textarea,div[data-testid="stTextInput"] input{border:1px solid #d9e0eb;border-radius:11px;background:#fff}
div[data-testid="stTextArea"] textarea:focus,div[data-testid="stTextInput"] input:focus{border-color:#7181f0;box-shadow:0 0 0 3px #5269e81c}
div[data-testid="stDataFrame"]{border:1px solid var(--line);border-radius:12px;overflow:hidden} hr{border-color:var(--line)}
@media(max-width:750px){.block-container{padding:1rem 1rem 3rem}.hero{padding:1.4rem}.hero:after{display:none}}
</style>
""", unsafe_allow_html=True)

if "analysis" not in st.session_state:
    st.session_state.analysis = {}
state = st.session_state.analysis
NAV = ["Overview", "Job Analyzer", "Task Classification", "Skills Gap", "Reskilling Roadmap", "Responsible AI", "Technical About"]
LABELS = {"Overview":"⌂　Overview","Job Analyzer":"⌕　Job analyzer","Task Classification":"◈　Task exposure","Skills Gap":"⌁　Skills analysis","Reskilling Roadmap":"↗　Learning roadmap","Responsible AI":"◎　Responsible AI","Technical About":"ⓘ　About the project"}

with st.sidebar:
    st.markdown('<div class="brand"><div class="brand-mark">✳</div><div><div class="brand-name">JobImpact AI</div><div class="brand-sub">Workforce intelligence</div></div></div>', unsafe_allow_html=True)
    st.markdown('<div class="side-label">Workspace</div>', unsafe_allow_html=True)
    page = st.radio("Workspace", NAV, label_visibility="collapsed", format_func=lambda x: LABELS[x])
    st.markdown('<div class="side-label">Gemini connection</div>', unsafe_allow_html=True)
    st.text_input("Gemini API key", type="password", placeholder="Paste your API key", key="gemini_key_input", help="Used for this session only. Or set GEMINI_API_KEY in .env or Streamlit secrets.")
    st.text_input("Model ID", value=st.session_state.get("gemini_model_input", GEMINI_MODEL), key="gemini_model_input")
    has_key = bool(st.session_state.get("gemini_key_input", ""))
    st.markdown(f'<div class="status-pill"><span class="status-dot"></span>{"Key ready for this session" if has_key else "Demo mode · add a key to enable Gemini"}</div>', unsafe_allow_html=True)
    st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)
    st.markdown('<div class="small-note" style="color:#8291a8">P59 · Track E: Responsible AI<br>Task-level analysis with human oversight</div>', unsafe_allow_html=True)

def hero(title, copy, kicker="JOB TASK EXPOSURE ANALYZER"):
    st.markdown(f'<div class="hero"><div class="hero-kicker">{html.escape(kicker)}</div><div class="hero-title">{html.escape(title)}</div><div class="hero-copy">{html.escape(copy)}</div><div class="hero-tags"><span class="hero-tag">Automate</span><span class="hero-tag">Augment</span><span class="hero-tag">Human-led</span><span class="hero-tag">Human oversight</span></div></div>', unsafe_allow_html=True)

def section(title, subtitle=""):
    st.markdown(f'<div class="section-head"><div class="section-title">{html.escape(title)}</div><div class="section-sub">{html.escape(subtitle)}</div></div>', unsafe_allow_html=True)

def require_data():
    if not state.get("classifications"):
        st.info("Run an analysis from Overview or Job Analyzer to unlock this section.")
        return False
    return True

def run_analysis(raw, compare):
    job = validate_job_input(raw)
    state.pop("few_tasks", None)
    with st.status("Analyzing the role", expanded=True) as status:
        st.write("Decomposing responsibilities…")
        tasks, latency, source = decompose(job, False)
        if compare:
            st.write("Comparing few-shot prompting…")
            few_tasks, few_latency, few_source = decompose(job, True)
            state.update(few_tasks=few_tasks, few_latency=few_latency, few_source=few_source)
        st.write("Classifying exposure and matching skills…")
        classified, class_latency, class_source = classify(tasks)
        matches, engine = match_skills(tasks)
        gaps = summarize_gaps(matches)
        stages, roadmap_latency, roadmap_source, priorities = make_roadmap(gaps)
        state.update(job=job, tasks=tasks, latency=latency, source=source, classifications=classified,
                     class_latency=class_latency, class_source=class_source, matches=matches,
                     skill_engine=engine, gaps=gaps, stages=stages, roadmap_source=roadmap_source,
                     priorities=priorities, consistent=consistency_check(classified))
        state.pop("bias_audit", None)
        status.update(label="Analysis ready", state="complete", expanded=False)

def analysis_form(key):
    with st.form(key, clear_on_submit=False):
        raw = st.text_area("Job title or description", height=125, placeholder="Example: Data analyst responsible for validating datasets, building dashboards, and explaining findings…", label_visibility="collapsed")
        left, right = st.columns([1, 1])
        with left:
            compare = st.checkbox("Compare zero-shot and few-shot prompts", True, key=f"compare_{key}")
        with right:
            submitted = st.form_submit_button("Analyze this role　→", use_container_width=True)
    if submitted:
        try:
            run_analysis(raw, compare)
        except Exception as exc:
            st.error(str(exc))

def report_download():
    report = json.dumps({k: state.get(k) for k in ["job","tasks","source","classifications","class_source","matches","skill_engine","gaps","stages","roadmap_source","priorities","consistent"]}, indent=2, ensure_ascii=False)
    st.download_button("Download analysis report", report, "jobimpact_analysis.json", "application/json")

def exposure_chart():
    frame = pd.DataFrame(state["classifications"])
    counts = frame.label.value_counts().reindex(["Automate","Augment","Human-led"], fill_value=0).rename_axis("Exposure").reset_index(name="Tasks")
    chart = px.pie(counts, names="Exposure", values="Tasks", hole=.72, color="Exposure", color_discrete_map={"Automate":"#6177eb","Augment":"#eaa94c","Human-led":"#42ae91"})
    chart.update_traces(textposition="inside", textinfo="none", marker=dict(line=dict(color="#fff",width=3)))
    chart.update_layout(showlegend=False, margin=dict(l=8,r=8,t=12,b=8), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(family="DM Sans",color="#38465d"), height=280, annotations=[dict(text=f"{len(frame)}<br><sup>tasks</sup>",x=.5,y=.5,showarrow=False,font=dict(size=22,color="#17243c"))])
    return chart, counts

def results_overview():
    chart, counts = exposure_chart()
    total = len(state["classifications"])
    a,b,c,d = st.columns(4)
    for col,label in zip([a,b,c],["Automate","Augment","Human-led"]):
        number = int(counts.loc[counts.Exposure==label,"Tasks"].iloc[0])
        col.markdown(f'<div class="metric-card"><div class="metric-label">{label}</div><div class="metric-value">{number}</div><div class="metric-note">{number/total:.0%} of analyzed tasks</div></div>',unsafe_allow_html=True)
    d.markdown(f'<div class="metric-card"><div class="metric-label">Skill priorities</div><div class="metric-value">{len(state.get("priorities",[]))}</div><div class="metric-note">matched to this role</div></div>',unsafe_allow_html=True)
    left,right=st.columns([.9,1.1],gap="large")
    with left:
        section("Exposure snapshot","Task-level view, not a job-loss forecast")
        st.plotly_chart(chart,use_container_width=True,config={"displayModeBar":False})
    with right:
        section("Top skill priorities","Skills most closely associated with this role")
        for i,skill in enumerate(state.get("priorities",[])[:6],start=1):
            st.markdown(f'<div class="task-row"><span style="color:#7380a0;font-size:12px">{i:02}</span>　<b>{html.escape(skill)}</b></div>',unsafe_allow_html=True)
        report_download()

def task_cards(rows):
    for row in rows:
        label = row.get("label","Augment")
        css = {"Automate":"badge-auto","Augment":"badge-augment","Human-led":"badge-human"}.get(label,"badge-augment")
        task, explanation = html.escape(str(row.get("task",""))), html.escape(str(row.get("explanation","")))
        st.markdown(f'<div class="task-row"><div style="display:flex;justify-content:space-between;gap:14px;align-items:flex-start"><div><b>{task}</b><div class="small-note" style="margin-top:7px">{explanation}</div></div><span class="badge {css}">{html.escape(label)}</span></div></div>',unsafe_allow_html=True)

if page == "Overview":
    st.markdown('<div class="topline"><span>Workspace　/　Overview</span><span>Responsible AI · P59</span></div>',unsafe_allow_html=True)
    hero("See how AI reshapes work.","Break a role into real responsibilities, understand where AI may help, and turn skill gaps into a practical learning plan.")
    section("Start an analysis","Paste a job title or description. Add your Gemini key in the sidebar for live results.")
    with st.container(border=True):
        analysis_form("overview_form")
    if state.get("classifications"):
        section(f"Analysis · {state['job'][:70]}",f"Decomposition: {state['source']}　·　Classification: {state['class_source']}")
        results_overview()
    else:
        st.markdown("<div style='height:16px'></div>",unsafe_allow_html=True)
        c1,c2,c3=st.columns(3)
        for col,num,title,copy in [(c1,"01","Break down the role","Turn a job description into responsibilities."),(c2,"02","Map AI exposure","Review task labels and explanations."),(c3,"03","Build next steps","Connect skill gaps to a learning plan.")]:
            with col:
                st.markdown(f'<div class="panel"><div class="metric-label">STEP {num}</div><div style="font:700 16px Manrope;margin:9px 0 5px">{title}</div><div class="small-note">{copy}</div></div>',unsafe_allow_html=True)

elif page == "Job Analyzer":
    st.markdown('<div class="topline"><span>Workspace　/　Job analyzer</span><span>U1 · Prompt comparison</span></div>',unsafe_allow_html=True)
    hero("Analyze a job, task by task.","Compare zero-shot and few-shot decomposition, then inspect each responsibility.","ANALYSIS WORKSPACE")
    with st.container(border=True):
        section("Role description","Paste a complete job description or start with a job title.")
        analysis_form("analyzer_form")
    if state.get("tasks"):
        section("Zero-shot responsibilities",f"{len(state['tasks'])} responsibilities · {state['source']}")
        st.dataframe(pd.DataFrame(state["tasks"]),use_container_width=True,hide_index=True)
        if state.get("few_tasks"):
            section("Few-shot comparison",f"{len(state['few_tasks'])} responsibilities · {state['few_source']}")
            left,right=st.columns(2)
            with left:
                st.caption("ZERO-SHOT PROMPT")
                st.code(decomposition_prompt(state["job"],False),language="text")
            with right:
                st.caption("FEW-SHOT PROMPT")
                st.code(decomposition_prompt(state["job"],True),language="text")
            st.dataframe(pd.DataFrame(state["few_tasks"]),use_container_width=True,hide_index=True)

elif page == "Task Classification":
    st.markdown('<div class="topline"><span>Workspace　/　Task exposure</span><span>U2 · Explainable classification</span></div>',unsafe_allow_html=True)
    hero("Understand each exposure label.","Review the reasoning behind each task classification. Labels do not predict whether a whole job disappears.","TASK CLASSIFICATION")
    if require_data():
        st.caption(f"Source: {state['class_source']}")
        task_cards(state["classifications"])
        with st.expander("Prompting vs fine-tuning"):
            st.write("This app uses prompt-based inference through Gemini. It does not fine-tune model weights.")

elif page == "Skills Gap":
    st.markdown('<div class="topline"><span>Workspace　/　Skills analysis</span><span>U3 · Semantic matching</span></div>',unsafe_allow_html=True)
    hero("Make the skill gap actionable.","Explore skills connected to this role, then self-rate proficiency to surface learning priorities.","SKILLS INTELLIGENCE")
    if require_data():
        st.caption(f"Matching engine: {state['skill_engine']} · Similarity is semantic proximity, not competence.")
        if state["gaps"]:
            choices=[x["skill"] for x in state["gaps"]]
            section("Your proficiency","Adjust the sliders to personalize priorities.")
            cols=st.columns(2); proficiency={}
            for idx,skill in enumerate(choices[:10]):
                with cols[idx%2]: proficiency[skill]=st.slider(skill,0,100,0,step=10,key="prof_"+skill)
            state["gaps"]=summarize_gaps(state["matches"],proficiency)
            st.dataframe(pd.DataFrame(state["gaps"]),use_container_width=True,hide_index=True)
        section("Task-to-skill matches","Sentence-BERT or labelled fallback similarity matches.")
        for row in state["matches"]:
            with st.expander(row["task"]): st.dataframe(pd.DataFrame(row["skills"]),use_container_width=True,hide_index=True)

elif page == "Reskilling Roadmap":
    st.markdown('<div class="topline"><span>Workspace　/　Learning roadmap</span><span>U4 · Personalized next steps</span></div>',unsafe_allow_html=True)
    hero("Turn priorities into a plan.","A staged roadmap connects role skills to practical learning goals and a downloadable infographic.","RESKILLING ROADMAP")
    if require_data():
        st.caption(f"Plan source: {state['roadmap_source']}")
        for idx,stage in enumerate(state["stages"],start=1):
            with st.container(border=True):
                st.markdown(f'<div class="metric-label">STAGE {idx}　·　{html.escape(stage.get("duration",""))}</div><h3>{html.escape(stage.get("stage","Learning stage"))}</h3>',unsafe_allow_html=True)
                st.write("**Goals**")
                for goal in stage.get("goals",[]): st.markdown(f"- {goal}")
                st.info(stage.get("practice",""))
        png=roadmap_png(state["stages"],state["priorities"],"Reskilling plan · "+state.get("job","Role")[:50])
        section("Your infographic","Generated from this analysis")
        st.image(png,use_container_width=True)
        st.download_button("Download roadmap infographic",png,"jobimpact_roadmap.png","image/png")

elif page == "Responsible AI":
    st.markdown('<div class="topline"><span>Workspace　/　Responsible AI</span><span>U5 · Bias and limitations</span></div>',unsafe_allow_html=True)
    hero("Keep people in the loop.","Probe wording sensitivity, inspect consistency, and understand limits before using an estimate.","RESPONSIBLE AI")
    if require_data():
        section("Output validation","Structural checks validate formatting, not truth.")
        st.json(state["consistent"])
    if st.button("Run controlled wording audit"):
        with st.spinner("Evaluating matched demographic wordings…"):
            from modules.responsible_ai import run_bias_audit
            state["bias_audit"]=run_bias_audit()
    if state.get("bias_audit"):
        st.dataframe(pd.DataFrame(state["bias_audit"]),use_container_width=True,hide_index=True)
        st.caption("This small controlled probe is prompt-dependent; it cannot establish population-level fairness.")
    with st.expander("Limitations, privacy and human oversight",expanded=True):
        st.write("Exposure labels describe task characteristics under a particular description and current tools. They do not forecast layoffs, wages, or adoption.")
        st.write("Avoid confidential input. With Gemini configured, text is sent to Google's API. Outputs require human review and must not be used alone for employment decisions.")

elif page == "Technical About":
    st.markdown('<div class="topline"><span>Workspace　/　About</span><span>Technical overview</span></div>',unsafe_allow_html=True)
    hero("Built for a clear technical story.","Prompt engineering, task-level analysis, semantic matching, evaluation, and responsible use.","PROJECT OVERVIEW")
    with st.expander("Generative vs discriminative AI",expanded=True): st.write("Generative models produce new sequences; discriminative models learn to distinguish labels or outcomes.")
    with st.expander("Transformer attention"): st.write("Queries, keys and values give context-aware token representations. This app does not expose Gemini's internal attention maps.")
    with st.expander("GPT, BERT and Sentence-BERT"): st.write("GPT-style decoders generate autoregressively. BERT encoders contextualize bidirectionally. Sentence-BERT creates sentence vectors useful for similarity.")
    st.markdown("**Generation lifecycle:** define task → prompt → model inference → validate → human review → iterate. This latent-space chart is conceptual, not Gemini's internal state.")
    x=np.linspace(-3,3,250); y=np.exp(-x*x/2)/np.sqrt(2*np.pi)
    fig=px.area(x=x,y=y,labels={"x":"Latent variable (conceptual)","y":"Density"},title="Illustrative latent-variable distribution")
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",font=dict(family="DM Sans",color="#38465d"))
    st.plotly_chart(fig,use_container_width=True)
    st.caption("Sentence Transformers uses a pretrained PyTorch model when available. This project does not train or fine-tune weights.")
