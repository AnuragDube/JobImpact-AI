"""Simple user self-assessment comparison against role skill requirements."""
def summarize_gaps(matches, proficiency=None):
    proficiency=proficiency or {}
    scores={}
    for row in matches:
        for item in row["skills"]:
            name=item["skill"]
            scores[name]=max(scores.get(name,0),float(item["similarity"]))
    return [{"skill":k,"relevance":v,"proficiency":int(proficiency.get(k,0)),"gap":max(0,100-int(proficiency.get(k,0)))} for k,v in sorted(scores.items(),key=lambda x:x[1],reverse=True)]
