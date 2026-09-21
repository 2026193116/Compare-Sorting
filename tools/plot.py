import csv, html, os

def svg_bar(path, title, labels, values, colors):
    width, height, base = 760, 400, 330; scale = 250 / max(values or [1])
    bars=[]
    for i,(label,value) in enumerate(zip(labels,values)):
        x=70+i*220; h=max(2,value*scale); y=base-h
        bars.append(f'<rect x="{x}" y="{y:.1f}" width="120" height="{h:.1f}" fill="{colors[i]}"/><text x="{x+60}" y="{base+24}" text-anchor="middle">{label}</text><text x="{x+60}" y="{y-8:.1f}" text-anchor="middle">{value:g}</text>')
    text=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}"><style>text{{font:14px sans-serif}} .title{{font-size:20px;font-weight:bold}}</style><text class="title" x="20" y="30">{html.escape(title)}</text><line x1="50" y1="{base}" x2="730" y2="{base}" stroke="black"/>{"".join(bars)}</svg>'
    open(path,"w",encoding="utf-8").write(text)

def main():
    labels=["Shell","Counting","Cocktail"]; colors=["#4e79a7","#59a14f","#e15759"]
    svg_bar("report/complexity.svg","Relative growth (conceptual)",labels,[2,1,4],colors)
    svg_bar("report/input-behavior.svg","Input sensitivity (conceptual)",["sorted","random","reverse"],[1,3,5],colors[:3])
if __name__ == "__main__": main()
