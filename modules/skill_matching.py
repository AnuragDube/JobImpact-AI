"""Semantic skill matching, preferring Sentence Transformers and falling back to TF-IDF."""
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

SKILLS = ["Data analysis", "Critical thinking", "Written communication", "Verbal communication", "Project management", "Problem solving", "Customer service", "Leadership", "Team collaboration", "Python programming", "Software development", "Data visualization", "Statistical reasoning", "Digital marketing", "Content creation", "Research", "Quality assurance", "Cybersecurity awareness", "Prompt engineering", "AI literacy", "Decision making", "Empathy", "Negotiation", "Attention to detail", "Adaptability", "Time management", "Presentation skills", "Financial analysis", "Strategic planning", "Documentation"]
_model=None

def match_skills(tasks, threshold=.22):
    global _model
    texts=[(x.get("task","")+" "+x.get("context","")) if isinstance(x,dict) else str(x) for x in tasks]
    try:
        if _model is None:
            from sentence_transformers import SentenceTransformer
            _model=SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2", device="cpu")
        sims=cosine_similarity(_model.encode(texts),_model.encode(SKILLS))
        engine="Sentence-BERT: all-MiniLM-L6-v2"
    except Exception as exc:
        vec=TfidfVectorizer(ngram_range=(1,2),stop_words="english")
        mat=vec.fit_transform(texts+SKILLS)
        sims=cosine_similarity(mat[:len(texts)],mat[len(texts):])
        engine=f"TF-IDF fallback (Sentence-BERT unavailable: {exc})"
    records=[]
    for i,text in enumerate(texts):
        order=np.argsort(sims[i])[::-1][:5]
        records.append({"task":text,"skills":[{"skill":SKILLS[j],"similarity":float(sims[i,j])} for j in order if sims[i,j]>=threshold] or [{"skill":SKILLS[order[0]],"similarity":float(sims[i,order[0]])}]})
    return records,engine
