"""Create a downloadable infographic from current analysis results."""
import io
import matplotlib.pyplot as plt

def roadmap_png(stages, priorities, title="Personalized reskilling roadmap"):
    fig,ax=plt.subplots(figsize=(10,5.6)); ax.axis("off"); fig.patch.set_facecolor("#f7f9fc")
    ax.text(.04,.92,title,fontsize=19,fontweight="bold",color="#16243a",transform=ax.transAxes)
    for i,stage in enumerate(stages[:4]):
        y=.73-i*.2
        ax.text(.05,y,f"0{i+1}",fontsize=16,fontweight="bold",color="white",bbox=dict(boxstyle="round,pad=.45",fc="#4263eb",ec="none"),transform=ax.transAxes)
        ax.text(.16,y+.025,stage.get("stage","Stage"),fontsize=13,fontweight="bold",color="#16243a",transform=ax.transAxes)
        ax.text(.16,y-.045,f"{stage.get('duration','')}: {', '.join(stage.get('goals',[])[:2])}",fontsize=9,color="#526174",transform=ax.transAxes,wrap=True)
    ax.text(.05,.08,"Priority skills: "+", ".join(priorities[:8]),fontsize=10,color="#34445b",transform=ax.transAxes)
    buf=io.BytesIO(); fig.savefig(buf,format="png",dpi=160,bbox_inches="tight",facecolor=fig.get_facecolor()); plt.close(fig); buf.seek(0); return buf.getvalue()
