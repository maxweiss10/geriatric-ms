#!/usr/bin/env python3
import math, html, random, os
random.seed(42)

ENT = {"·":"&middot;","–":"&ndash;","—":"&mdash;","“":"&ldquo;","”":"&rdquo;","’":"&rsquo;","‘":"&lsquo;","≥":"&ge;"}
def ent(s):
    for k,v in ENT.items(): s = s.replace(k,v)
    return s
def esc(s): return ent(html.escape(s, quote=False))
def esq(s): return ent(html.escape(s, quote=True))
def f(x): return f"{x:.1f}"

W = 1040
CX, CY = 520.0, 255.0

# ------------------------------------------------------------------ icons
HEART = "M0,30 C-4,26 -34,8 -34,-10 C-34,-22 -24,-30 -14,-30 C-6,-30 -2,-26 0,-22 C2,-26 6,-30 14,-30 C24,-30 34,-22 34,-10 C34,8 4,26 0,30 Z"
HEART_LEFT = "M0,30 C-4,26 -34,8 -34,-10 C-34,-22 -24,-30 -14,-30 C-6,-30 -2,-26 0,-22 Z"

def spiral_points(turns=3.2, rmax=30, n=96):
    pts=[]
    for i in range(n+1):
        t=i/n; a=t*turns*2*math.pi; r=2+(rmax-2)*t
        pts.append(f"{r*math.cos(a):.1f},{r*math.sin(a):.1f}")
    return " ".join(pts)

def network_icon():
    o=['<circle r="9"/>']
    for a in range(0,360,45):
        x=27*math.cos(math.radians(a)); y=27*math.sin(math.radians(a))
        o.append(f'<line x1="0" y1="0" x2="{x:.1f}" y2="{y:.1f}" stroke="currentColor" stroke-width="3"/><circle cx="{x:.1f}" cy="{y:.1f}" r="5.5"/>')
    return "".join(o)

SYMBOLS = {
 'walk': '<circle cx="4" cy="-27" r="8"/><path d="M0,-16 L-3,4 M-3,4 L12,12 L10,30 M-3,4 L-13,28 M0,-13 L15,-2 M0,-13 L-15,-4" fill="none" stroke="currentColor" stroke-width="7.5" stroke-linecap="round" stroke-linejoin="round"/>',
 'hug': '<circle cx="-11" cy="-19" r="9"/><circle cx="12" cy="-15" r="8"/><path d="M-28,26 C-28,2 -20,-6 -11,-6 C-4,-6 0,-2 2,2 C6,-2 10,-3 12,-3 C22,-3 28,6 28,26 Z"/>',
 'pills': '<rect x="4" y="-22" width="24" height="48" rx="3"/><rect x="1" y="-30" width="30" height="9" rx="2"/><rect x="8" y="-8" width="16" height="14" fill="#fff" opacity=".35"/><g transform="translate(-16,10) rotate(-35)"><rect x="-16" y="-7" width="32" height="14" rx="7"/></g><g transform="translate(-20,-14) rotate(-35)"><rect x="-13" y="-6" width="26" height="12" rx="6"/></g>',
 'read': '<circle cx="-9" cy="-23" r="8.5"/><path d="M-30,28 C-30,4 -18,-6 -9,-6 C-1,-6 5,0 6,8 L6,28 Z"/><path d="M4,10 L31,2 L31,20 L4,28 Z"/>',
 'headgear': '<path d="M-24,32 L-24,4 C-26,-18 -10,-34 8,-34 C26,-34 34,-20 32,-8 L38,0 L32,3 L32,12 C32,18 26,20 19,20 L15,32 Z"/><circle cx="2" cy="-10" r="8" fill="none" stroke="var(--paper)" stroke-width="4.5" stroke-dasharray="3.2 3.2"/><circle cx="2" cy="-10" r="3" fill="var(--paper)"/><circle cx="16" cy="3" r="5" fill="none" stroke="var(--paper)" stroke-width="3.5" stroke-dasharray="2.4 2.4"/><circle cx="16" cy="3" r="1.8" fill="var(--paper)"/>',
 'capsule': '<g transform="rotate(-40)"><rect x="-32" y="-14" width="64" height="28" rx="14"/><path d="M0,-14 H18 A14,14 0 0 1 18,14 H0 Z" fill="#fff" opacity=".42"/></g>',
 'network': network_icon(),
 'heart': f'<path d="{HEART}"/>',
 'heartdash': f'<path d="{HEART}" fill="none" stroke="currentColor" stroke-width="4.5" stroke-dasharray="7 5"/>',
 'hearthalf': f'<path d="{HEART}" fill="none" stroke="currentColor" stroke-width="4"/><path d="{HEART_LEFT}"/>',
 'money': '<circle r="29"/><text y="12" font-size="36" font-weight="700" text-anchor="middle" fill="var(--paper)" font-family="IBM Plex Sans, system-ui, sans-serif">$</text>',
 'maint': '<path d="M24,-10 A26,26 0 1 0 24,10" fill="none" stroke="currentColor" stroke-width="8.5" stroke-linecap="round"/><path d="M12,-22 L32,-10 L14,4 Z"/>',
 'house': '<path d="M-34,0 L0,-32 L34,0 L26,0 L26,30 L-26,30 L-26,0 Z"/><rect x="-7" y="10" width="14" height="20" fill="var(--paper)"/>',
 'brain': '<path d="M-2,-30 C-20,-30 -32,-18 -30,-4 C-34,6 -26,20 -12,22 C-6,30 4,30 8,24 C22,26 32,14 30,2 C34,-10 26,-26 10,-28 C6,-32 0,-32 -2,-30 Z"/><path d="M-1,-28 L-1,26 M-18,-14 C-10,-10 -8,0 -16,6 M14,-16 C6,-10 8,2 16,8" fill="none" stroke="var(--paper)" stroke-width="3"/>',
 'drop': '<path d="M0,-32 C0,-32 -24,-2 -24,10 A24,24 0 0 0 24,10 C24,-2 0,-32 0,-32 Z"/>',
 'bottle': '<rect x="-15" y="-13" width="30" height="42" rx="5"/><rect x="-9" y="-29" width="18" height="14" rx="2"/>',
 'magnet': '<path d="M-17,-30 V-4 A17,17 0 0 0 17,-4 V-30" fill="none" stroke="#D0342C" stroke-width="14"/><rect x="-24" y="-34" width="14" height="12" fill="#B8BCC6"/><rect x="10" y="-34" width="14" height="12" fill="#B8BCC6"/>',
 'skull': '<circle cy="-8" r="23" fill="#F2F2F2"/><rect x="-13" y="6" width="26" height="18" rx="4" fill="#F2F2F2"/><circle cx="-8.5" cy="-10" r="5.5" fill="#111"/><circle cx="8.5" cy="-10" r="5.5" fill="#111"/><path d="M-3,0 L0,6 L3,0 Z" fill="#111"/><path d="M-7,12 V24 M-1,12 V24 M5,12 V24" stroke="#111" stroke-width="2" fill="none"/>',
 'spiral': f'<polyline points="{spiral_points()}" fill="none" stroke="currentColor" stroke-width="4" stroke-linecap="round"/>',
}

def symbols_svg():
    o=['<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>']
    for k,v in SYMBOLS.items():
        o.append(f'<symbol id="ic-{k}" viewBox="-40 -40 80 80" fill="currentColor">{v}</symbol>')
    o.append('</defs></svg>')
    return "".join(o)

MS = {
 'mind':     dict(label='Mind',            icon='headgear',  color='#D4731C'),
 'mobility': dict(label='Mobility',        icon='walk',      color='#8C2A2A'),
 'meds':     dict(label='Medications',     icon='capsule',   color='#7A9A2E'),
 'multi':    dict(label='Multicomplexity', icon='network',   color='#2F6FA8'),
 'matters':  dict(label='Matters Most',    icon='heart',     color='#5B3F7A'),
 'money':    dict(label='Money',           icon='money',     color='#C48A12'),
 'maint':    dict(label='Maintenance',     icon='maint',     color='#1F8A8A'),
 'milieu':   dict(label='Milieu',          icon='house',     color='#8B5E3C'),
 'mental':   dict(label='Mental',          icon='brain',     color='#D6336C'),
 'mict':     dict(label='Micturition',     icon='drop',      color='#E3B505'),
 'least':    dict(label='Matters Least',   icon='heartdash', color='#8A8F98'),
 'miralax':  dict(label='Miralax',         icon='bottle',    color='#22C55E'),
 'middle':   dict(label='Matters Middle',  icon='hearthalf', color='#9A86C8'),
 'magnets':  dict(label='Magnets',         icon='magnet',    color='#D0342C'),
 'morbid':   dict(label='Multimorbidity',  icon='skull',     color='#111111'),
 'verse':    dict(label='Multiverse',      icon='spiral',    color='#8E5BD9'),
}

# ------------------------------------------------------------------ primitives
def text(x, y, s, cls="lbl", size=14, fill=None, anchor="middle", extra=""):
    fa = f' fill="{fill}"' if fill else ""
    lines = s.split("|")
    if len(lines)==1:
        return f'<text x="{f(x)}" y="{f(y)}" class="{cls}" font-size="{size}" text-anchor="{anchor}"{fa}{extra}>{esc(s)}</text>'
    lh=size*1.15; y0=y-(len(lines)-1)*lh/2
    o=[f'<text class="{cls}" font-size="{size}" text-anchor="{anchor}"{fa}{extra}>']
    for i,ln in enumerate(lines): o.append(f'<tspan x="{f(x)}" y="{f(y0+i*lh)}">{esc(ln)}</tspan>')
    o.append('</text>'); return "".join(o)

def icon(name, cx, cy, size, color=None, extra=""):
    st = f' style="color:{color}"' if color else ""
    return f'<use href="#ic-{name}" x="{f(cx-size/2)}" y="{f(cy-size/2)}" width="{f(size)}" height="{f(size)}"{st}{extra}/>'

def slot(key, cx, cy, size=84, scale=1.0, label=True, lcls="lbl", dy_label=None):
    m=MS[key]; s=size*scale
    out=icon(m['icon'], cx, cy, s, m['color'])
    if label:
        ly = (cy + s/2 + 18) if dy_label is None else (cy + dy_label)
        out += text(cx, ly, m['label'], cls=lcls, size=14)
    return out

def marker_def(id_, color="currentColor"):
    return (f'<marker id="{id_}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="8" markerHeight="8" '
            f'orient="auto-start-reverse" markerUnits="userSpaceOnUse"><path d="M0,0 L10,5 L0,10 Z" fill="{color}"/></marker>')

def arrow(p1, p2, r1, r2, out=0.0, label=None, marker="ah", cls="arrow", lcls="arrow-lbl", gap1=4, gap2=8):
    (x1,y1),(x2,y2) = p1,p2
    dx,dy = x2-x1, y2-y1
    L = math.hypot(dx,dy); ux,uy = dx/L, dy/L
    px,py = -uy, ux
    mx,my = (x1+x2)/2, (y1+y2)/2
    if (mx-CX)*px + (my-CY)*py < 0: px,py = -px,-py
    qx,qy = mx+px*out, my+py*out
    def toward(ax,ay,bx,by,d):
        ddx,ddy = bx-ax, by-ay; l = math.hypot(ddx,ddy) or 1
        return (ax+ddx/l*d, ay+ddy/l*d)
    s = toward(x1,y1,qx,qy, r1+gap1); e = toward(x2,y2,qx,qy, r2+gap2)
    o = f'<path d="M{f(s[0])},{f(s[1])} Q{f(qx)},{f(qy)} {f(e[0])},{f(e[1])}" class="{cls}" marker-end="url(#{marker})"/>'
    if label:
        lx = 0.25*s[0] + 0.5*qx + 0.25*e[0]; ly = 0.25*s[1] + 0.5*qy + 0.25*e[1]
        o += f'<text x="{f(lx+px*12)}" y="{f(ly+py*12+4)}" class="{lcls}" font-size="11" text-anchor="middle">{esc(label)}</text>'
    return o

def arrow_q(p1, p2, r1, r2, ctrl, label=None, lpos=None, marker="ah", cls="arrow", lcls="arrow-lbl", gap1=4, gap2=8):
    (x1,y1),(x2,y2) = p1,p2; qx,qy = ctrl
    def toward(ax,ay,bx,by,d):
        ddx,ddy = bx-ax, by-ay; l = math.hypot(ddx,ddy) or 1
        return (ax+ddx/l*d, ay+ddy/l*d)
    s = toward(x1,y1,qx,qy, r1+gap1); e = toward(x2,y2,qx,qy, r2+gap2)
    o = f'<path d="M{f(s[0])},{f(s[1])} Q{f(qx)},{f(qy)} {f(e[0])},{f(e[1])}" class="{cls}" marker-end="url(#{marker})"/>'
    if label and lpos:
        o += f'<text x="{f(lpos[0])}" y="{f(lpos[1])}" class="{lcls}" font-size="11" text-anchor="middle">{esc(label)}</text>'
    return o

def star(cx, cy, r1, r2, n, fill, lines, lsize=8, lfill="#fff", rot=0):
    pts=[]
    for k in range(2*n):
        a = -math.pi/2 + math.pi*k/n
        rr = r1 if k%2==0 else r2
        pts.append(f"{f(cx+rr*math.cos(a))},{f(cy+rr*math.sin(a))}")
    return (f'<g transform="rotate({rot} {f(cx)} {f(cy)})"><polygon points="{" ".join(pts)}" fill="{fill}"/>'
            + text(cx, cy+3, "|".join(lines), cls="lbl", size=lsize, fill=lfill) + '</g>')

def svg_wrap(inner, aria, vb, defs="", cls="", id_=""):
    idattr = f' id="{id_}"' if id_ else ""
    d = f"<defs>{defs}</defs>" if defs else ""
    c = f' {cls}' if cls else ""
    x,y,w,h = vb
    return f'<svg class="fig-svg{c}" viewBox="{x} {y} {w} {h}" role="img" aria-label="{esq(aria)}"{idattr}>{d}{inner}</svg>'

# ------------------------------------------------------------------ Figure 1: IHI 4Ms
def fig_ihi():
    s=[]
    s.append('<circle cx="300" cy="300" r="232" class="disk"/>')
    items=[("What|Matters",300,100,"#1B7EA3","hug"),("Medication",500,300,"#3E7F66","pills"),
           ("Mentation",300,500,"#1A4A6B","read"),("Mobility",100,300,"#E8622A","walk")]
    for lab,cx,cy,col,ic in items:
        s.append(f'<circle cx="{cx}" cy="{cy}" r="92" fill="{col}" stroke="var(--paper)" stroke-width="4"/>')
        two = "|" in lab
        s.append(text(cx, cy-46 if two else cy-38, lab, cls="ihi-lbl", size=18, fill="#fff"))
        s.append(icon(ic, cx, cy+30 if two else cy+24, 66, "#fff"))
    s.append(text(300, 292, "4Ms", cls="ihi-center", size=32))
    s.append(text(300, 328, "Framework", cls="ihi-center", size=32))
    return svg_wrap("".join(s), "Four colored circles on a pale blue disk, What Matters at the top, Medication right, Mentation bottom, Mobility left, each with a white pictogram, and the words 4Ms Framework in the center.", (0,0,600,600))

# ------------------------------------------------------------------ Figures 2 to 13: the growing row
def positions(L):
    P={}
    if L==5:
        for i,k in enumerate(['mind','mobility','meds','multi','matters']): P[k]=(520+(i-2)*170, 110)
    elif L==6:
        for i,k in enumerate(['mind','mobility','meds','multi','matters','money']): P[k]=(520+(i-2.5)*150, 110)
    else:
        for i,k in enumerate(['mind','mobility','meds','multi']): P[k]=(520+(i-1.5)*180, 170)
        row1=['matters','money','maint']+(['mict'] if L>=10 else [])
        n=len(row1)
        for i,k in enumerate(row1): P[k]=(520+(i-(n-1)/2)*180, 340)
    return P

VB = {5:(0,45,W,150), 6:(0,45,W,150), 7:(0,70,W,350), 8:(0,0,W,440), 9:(0,0,W,440), 10:(0,0,W,440)}
for L in range(11,17): VB[L]=(0,0,W,585)

def draw(L):
    P=positions(L); s=[]; defs=[marker_def(f"ah{L}")]
    # field lines (behind everything)
    if L>=14:
        for r in (70,150,250,370,520,700):
            s.append(f'<path d="M975,{f(250-r)} A{f(r*0.9)},{f(r)} 0 0 0 975,{f(250+r)}" class="field"/>')
    # house
    if L>=8:
        s.append('<path d="M130,68 L520,12 L910,68 Z" class="house"/><rect x="130" y="68" width="780" height="352" class="house"/>')
        s.append(icon('house',474,44,34,MS['milieu']['color']) + text(497,49,'Milieu',cls='lbl',size=13,anchor='start'))
    # Venn: Mind / Mental
    if L>=9:
        mx,my=P['mind']; c=MS['mental']['color']; ox,oy=44,14
        s.append(f'<circle cx="{f(mx)}" cy="{f(my)}" r="48" class="venn"/>')
        s.append(f'<circle cx="{f(mx+ox)}" cy="{f(my+oy)}" r="48" class="venn" style="stroke:{c}"/>')
        defs.append(f'<mask id="mk9-{L}" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="600"><rect x="0" y="0" width="{W}" height="600" fill="#fff"/><circle cx="{f(mx)}" cy="{f(my)}" r="48" fill="#000"/></mask>')
        s.append(f'<circle cx="{f(mx+ox)}" cy="{f(my+oy)}" r="48" fill="{c}" opacity=".32" mask="url(#mk9-{L})"/>')
        s.append(icon('brain', mx+68, my+22, 32, c))
        s.append(text(mx+ox, my+oy+66, 'Mental', size=14))
        s.append(f'<path d="M{f(mx+84)},{f(my+36)} L{f(mx+110)},{f(my+92)}" class="hair"/>')
        s.append(f'<text x="{f(mx+114)}" y="{f(my+96)}" class="marker" font-size="13" fill="{c}">the difference</text>')
    # Venn: Multicomplexity / Multimorbidity (upper-right, clear of the Multicomplexity label)
    if L>=15:
        cx,cy=P['multi']; ox,oy=44,-16
        s.append(f'<circle cx="{f(cx)}" cy="{f(cy)}" r="48" class="venn"/>')
        defs.append(f'<mask id="mk15-{L}" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="600"><rect x="0" y="0" width="{W}" height="600" fill="#fff"/><circle cx="{f(cx)}" cy="{f(cy)}" r="48" fill="#000"/></mask>')
        s.append(f'<circle cx="{f(cx+ox)}" cy="{f(cy+oy)}" r="48" fill="#111" opacity=".92" stroke="var(--ink)" stroke-width="1" mask="url(#mk15-{L})"/>')
        s.append(icon('skull', cx+67, cy-24, 32))
        s.append(text(cx+ox, cy-74, 'Multimorbidity', cls='creep', size=17))
        s.append(f'<path d="M{f(cx-4)},{f(cy-55)} L{f(cx+26)},{f(cy-60)}" class="hair"/>')
        s.append(f'<text x="{f(cx-10)}" y="{f(cy-52)}" class="marker" font-size="13" fill="var(--ink)" text-anchor="end">more morbid</text>')
    # Maintenance loop
    if L>=7:
        mx,my = P['maint']; top=my-52
        if L>=10:
            d=f"M{f(mx)},{f(top)} C{f(mx)},{f(top-30)} 700,{f(top-20)} 700,{f(top-56)} L700,124 Q700,100 676,100 L274,100 Q250,100 250,110"
        else:
            d=f"M{f(mx)},{f(top)} L700,124 Q700,100 676,100 L274,100 Q250,100 250,110"
        s.append(f'<path d="{d}" class="arrow" marker-end="url(#ah{L})"/>')
        s.append(text(475, 92, 'is this sustainable?', cls='arrow-lbl it', size=12))
    # contributes
    if L>=10:
        s.append(arrow_q(P['mobility'], P['mict'], 50, 62, (560,300), label='contributes', lpos=(548,262), marker=f'ah{L}'))
        s.append(arrow_q(P['meds'], P['mict'], 50, 62, (735,232), label='also', lpos=(736,266), marker=f'ah{L}'))
    # axis
    if L>=11:
        s.append('<line x1="250" y1="412" x2="250" y2="478" class="tie"/>')
        s.append(f'<path d="M262,488 L935,488" class="axis" marker-start="url(#ah{L})" marker-end="url(#ah{L})"/>')
        s.append(text(262, 508, 'most', cls='axis-lbl', size=10, anchor='start'))
        s.append(text(935, 508, 'least', cls='axis-lbl', size=10, anchor='end'))
        s.append(slot('least', 975, 488, size=60))
        s.append(text(975, 566, '(do not think about this)', cls='arrow-lbl it', size=10))
    # monitor
    if L>=12:
        s.append('<rect x="14" y="436" width="208" height="112" rx="6" class="monitor"/>')
        for i,(a,b) in enumerate([("HR","72"),("BP","128/76"),("RR","16"),("Temp","36.8"),("SpO2","96%")]):
            y=456+i*16
            s.append(f'<text x="26" y="{y}" class="mono" font-size="11.5" fill="#22C55E">{a}</text><text x="80" y="{y}" class="mono" font-size="11.5" fill="#22C55E">{b}</text>')
        s.append('<text x="26" y="538" class="mono" font-size="11.5" font-weight="700" fill="#FACC15">MiraLAX</text><text x="80" y="538" class="mono" font-size="11.5" font-weight="700" fill="#FACC15">17 g daily</text>')
        s.append('<polyline points="148,462 156,462 160,450 164,474 168,462 176,462 180,456 184,468 188,462 200,462" fill="none" stroke="#22C55E" stroke-width="1.5"/>')
        s.append(icon('bottle', 190, 500, 40, '#FACC15'))
        s.append(text(118, 566, 'Miralax', size=14))
    # middle
    if L>=13:
        s.append('<path d="M300,462 V456 H925 V462" class="bracket"/>')
        s.append(text(470, 447, 'everything in between', cls='arrow-lbl it', size=11))
        s.append(slot('middle', 612, 488, size=60))
        for k,ax in (('money',380),('maint',612),('mict',300)):
            x,y=P[k]
            s.append(f'<line x1="{f(x)}" y1="421" x2="{ax}" y2="482" class="tie"/><circle cx="{ax}" cy="484" r="2.5" fill="var(--muted)"/>')
    # magnets
    if L>=14:
        s.append(slot('magnets', 975, 250, size=76, label=False))
        s.append('<circle cx="975" cy="250" r="50" class="lens"/><line x1="1011" y1="286" x2="1032" y2="308" class="lens-h"/>')
        s.append(text(975, 322, 'Magnets', size=14))
        s.append(text(975, 337, 'mechanism: undecided', cls='arrow-lbl it', size=10))
        s.append(text(975, 351, "via the patient's lens", cls='arrow-lbl it', size=10))
    # starburst
    if L>=10:
        s.append(star(868, 386, 34, 21, 12, '#D0342C', ['VERY','IMPORTANT'], lsize=8))
    # slots
    for k,(x,y) in P.items():
        if k=='mict': s.append(slot('mict', x, y, scale=1.3, dy_label=70))
        else: s.append(slot(k, x, y))
    # multiverse spiral
    if L>=16:
        s.append(f'<g class="spin"><g transform="translate(520,255)">{icon("spiral",0,0,64,MS["verse"]["color"])}</g></g>')
        s.append(text(520, 306, 'Multiverse', size=14))
    return "".join(s), "".join(defs)

ARIA = {
 5:"Five flat icons in a row with labels beneath: Mind, Mobility, Medications, Multicomplexity, Matters Most.",
 6:"Six icons in a row: the five Ms plus a gold coin labeled Money.",
 7:"Seven icons in two rows. A long arrow loops from Maintenance up and over the top row back to Mind, labeled is this sustainable.",
 8:"The two rows of icons now sit inside a house outline labeled Milieu. The loop arrow remains.",
 9:"Inside the house, a pink circle labeled Mental overlaps the circle around Mind. The sliver that does not overlap is labeled the difference.",
 10:"Micturition, a yellow drop drawn larger than the other icons, joins the bottom row with a red starburst reading Very Important. Arrows from Mobility and Medications point to it, labeled contributes.",
 11:"Below the house, an axis runs from most to least. Matters Least, a dashed grey heart, sits outside the house at the far end.",
 12:"A black monitor below the house lists five vital signs and, highlighted in yellow, MiraLAX 17 g daily.",
 13:"Matters Middle, a half-filled heart, sits at the midpoint of the axis under a bracket labeled everything in between. Dotted lines tie three Ms to the axis.",
 14:"A horseshoe magnet outside the house, seen through a magnifying lens, sends dashed field lines through the house and everything in it.",
 15:"A black circle with a skull labeled Multimorbidity overlaps the circle around Multicomplexity. The overhang is labeled more morbid.",
 16:"The entire fifteen-M figure, drawn several times over itself in shifted, tinted copies, with a spiral labeled Multiverse at the center.",
}

def fig_row(L):
    inner, defs = draw(L)
    return svg_wrap(inner, ARIA[L], VB[L], defs=defs)

def fig_multiverse():
    inner, defs = draw(16)
    ghosts = []
    for (dx,dy,rot,sc,hue) in [(-46,-28,-4,0.985,110),(52,34,5,1.01,230),(-18,52,-2,0.97,320)]:
        ghosts.append(f'<use href="#core13" transform="translate({dx} {dy}) translate(520 300) rotate({rot}) scale({sc}) translate(-520 -300)" style="opacity:.28;filter:hue-rotate({hue}deg)"/>')
    body = "".join(ghosts) + f'<g id="core13">{inner}</g>'
    return svg_wrap(body, ARIA[16], VB[16], defs=defs, id_="svg13")

# ------------------------------------------------------------------ page assembly
def new_m(key, desc):
    m=MS[key]
    return (f'<dl class="new" style="border-left-color:{m["color"]}"><dt><span class="chip" style="background:{m["color"]}"></span>{esc(m["label"])}</dt>'
            f'<dd>{esc(desc)}</dd></dl>')

def section(num, eyebrow, title, source, svg, caption, body_html="", raw_caption=False, h2id="", wide=False, body_after=False, after_html=""):
    cap = caption if raw_caption else esc(caption)
    h2i = f' id="{h2id}"' if h2id else ""
    cls = "fig fig-wide" if wide else "fig"
    return f'''
<section class="{cls}" id="fig{num}">
  <header>
    <p class="eyebrow">{esc(eyebrow)}</p>
    <h2{h2i}>{esc(title)}</h2>
    <p class="source">{esc(source)}</p>
  </header>
  {"" if body_after else body_html}
  <figure>
    {svg}
    <figcaption>{cap}</figcaption>
  </figure>
  {body_html if body_after else ""}{after_html}
</section>'''

DL4 = "".join(f'<div class="row"><dt><span class="bar" style="background:{c}">{esc(t)}</span></dt><dd>{esc(d)}</dd></div>' for t,d,c in [
 ("What Matters","Know and align care with each older adult's specific health outcome goals and care preferences, including day-to-day needs as well as end-of-life planning, across settings of care.","#1B7EA3"),
 ("Medication","If medication is necessary, use age-friendly medications that do not interfere with What Matters to the older adult, Mobility, or Mentation across settings of care.","#3E7F66"),
 ("Mentation","Prevent, identify, treat, and manage dementia, depression, and delirium across settings of care.","#1A4A6B"),
 ("Mobility","Ensure that older adults move safely every day in order to maintain function and do What Matters.","#E8622A"),
])
DL5 = "".join(f'<div class="row"><dt style="color:{MS[k]["color"]}">{esc(MS[k]["label"])}</dt><dd>{esc(d)}</dd></div>' for k,d in [
 ("mind","Mentation, dementia, delirium, depression."),
 ("mobility","Impaired gait and balance; fall injury prevention."),
 ("meds","Polypharmacy, deprescribing, optimal prescribing; adverse effects and medication burden."),
 ("multi","Multimorbidity; complex bio-psycho-social situations."),
 ("matters","Each individual's own meaningful health outcome goals and care preferences."),
])

sections = "".join([
 section(1,"Figure 1 · Canonical","The 4Ms",
   "Age-Friendly Health Systems. The John A. Hartford Foundation, the Institute for Healthcare Improvement, and the American Hospital Association.",
   fig_ihi(),
   "The 4Ms Framework, redrawn from the IHI graphic: four circles on a pale disk, What Matters on top, a pictogram in each. Reproduced without comment.",
   body_html=f'<dl class="ms ihi">{DL4}</dl>'),
 section(2,"Figure 2 · Canonical","The 5Ms",
   "Tinetti M, Huang A, Molnar F. J Am Geriatr Soc. 2017;65(9):2115. Icons after the Stanford and VA Boston teaching slides.",
   fig_row(5),
   "The Geriatric 5Ms, redrawn from the teaching slide everyone lifts: five icons in a row, one color each. Also reproduced without comment.",
   body_html=f'<dl class="ms five">{DL5}</dl>', wide=True, body_after=True),
 section(3,"Figure 3 · Proposed","The 6Ms",
   "Proposed. Reviewer 2 found it reasonable, which in retrospect was the warning.",
   fig_row(6),
   "The 6Ms. The row has been extended by one coin. Everything else is unchanged, including the spacing, which has been reduced.",
   body_html=new_m('money',"Financial considerations. Whether the patient can afford what you just recommended, and whether anyone checked."), wide=True),
 section(4,"Figure 4 · Under review","The 7Ms",
   "Under review. Reviewer 2 asked whether the review process itself was sustainable.",
   fig_row(7),
   "The 7Ms. The row now wraps. Maintenance is connected back to the beginning by an arrow asking whether any of this is sustainable. The arrow has not been answered.",
   body_html=new_m('maint',"Is this sustainable. Not the patient: the plan. Also the patient."), wide=True),
 section(5,"Figure 5 · Revised","The 8Ms",
   "Revised. The figure has been moved indoors.",
   fig_row(8),
   "The 8Ms. All previous Ms now take place inside a house. The house is Milieu. The arrow is still there.",
   body_html=new_m('milieu',"Environment. Everything now takes place inside a house. The house is also an M."), wide=True),
 section(6,"Figure 6 · Revised again","The 9Ms",
   "Revised again. Reviewer 2 asked what the difference was. It has been labeled.",
   fig_row(9),
   "The 9Ms. Mental has been added next to Mind, overlapping it. The part that does not overlap is the difference. It is labeled.",
   body_html=new_m('mental',"Doubling down on Mind, because it is important. There is a difference. The difference has been labeled."), wide=True),
 section(7,"Figure 7 · Very important","The 10Ms",
   "Accepted in principle. Reviewer 2 agreed this one was important and asked why it took ten.",
   fig_row(10),
   "The 10Ms. Micturition has been added at 1.3 times the size of the other Ms and marked Very Important. Mobility and Medications contribute, which is true.",
   body_html=new_m('mict',"A very important topic in geriatrics. Marked accordingly."), wide=True),
 section(8,"Figure 8 · Not under review","The 11Ms",
   "Not under review. Reviewer 2 has been placed outside the house.",
   fig_row(11),
   "The 11Ms. An axis now runs from Matters Most to Matters Least. Matters Least sits outside the house, where it does not need to be thought about, and is labeled so that you can think about it.",
   body_html=new_m('least',"What we do not need to think about, now thought about and placed outside the house."), wide=True),
 section(9,"Figure 9 · Vital","The 12Ms",
   "Nursing has signed off. Nursing signed off first, in fact.",
   fig_row(12),
   "The 12Ms. A monitor has been installed below the house. It shows five vital signs and Miralax. Miralax is highlighted.",
   body_html=new_m('miralax',"The sixth vital sign. Displayed on the monitor with the other five."), wide=True),
 section(10,"Figure 10 · Interpolated","The 13Ms",
   "Interpolated. No new data were collected.",
   fig_row(13),
   "The 13Ms. Matters Middle has been placed at the midpoint of the axis. A bracket indicates that everything else is in between, and dotted lines confirm this for three of them.",
   body_html=new_m('middle',"Everything between Least and Most, which on inspection is everything."), wide=True),
 section(11,"Figure 11 · Undecided","The 14Ms",
   "Undecided. Physics was consulted and declined to comment.",
   fig_row(14),
   "The 14Ms. A magnet has been placed outside the house. Its field lines pass through the house, the Ms, and the axis. A lens has been provided so the magnet can be considered from the patient's point of view. Its mechanism remains undecided.",
   body_html=new_m('magnets',"The scientific community remains undecided on how they work. Please consider them through the lens of your patient. A lens has been provided."), wide=True),
 section(12,"Figure 12 · Morbid","The 15Ms",
   "Preprint. Laminated. Black.",
   fig_row(15),
   "The 15Ms. Multimorbidity has been added on top of Multicomplexity, from which it differs by being more morbid. The part that is more morbid is labeled.",
   body_html=new_m('morbid',"Like Multicomplexity, but more morbid."), wide=True),
 section(13,"Figure 13 · N","The NMs",
   "Found, in several places at once.",
   fig_multiverse(),
   'The NMs. Figure 12, in every universe. Each additional universe adds one M. <span id="ncount">N = 16</span>. Variations considered so far: <span id="considered">1</span>.',
   body_html=new_m('verse',"Have you considered all multiversal variations of all possible Ms of the patient? Consider one more below."),
   after_html='<div class="actions"><button type="button" id="addU">Consider another universe</button><span class="hint" id="hint"></span></div>',
   raw_caption=True, wide=True),
])

FONTS = "https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;0,6..72,600;1,6..72,400&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;700&family=Permanent+Marker&family=Creepster&display=swap"

CSS = '''
:root{--paper:#F4F6F3;--surface:#FFFFFF;--ink:#1A222B;--muted:#5B6672;--line:#CFD7D3;--accent:#146C7A;--accent-soft:#D7E9EC;--disk:#E3F0F9;color-scheme:light}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--paper:#0F1518;--surface:#182126;--ink:#E7ECEA;--muted:#97A4AA;--line:#2A3538;--accent:#4FB3C1;--accent-soft:#173C43;--disk:#16232D;color-scheme:dark}}
:root[data-theme="dark"]{--paper:#0F1518;--surface:#182126;--ink:#E7ECEA;--muted:#97A4AA;--line:#2A3538;--accent:#4FB3C1;--accent-soft:#173C43;--disk:#16232D;color-scheme:dark}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);font-family:'Newsreader',Georgia,'Times New Roman',serif;font-size:17px;line-height:1.5;-webkit-font-smoothing:antialiased}
.page{max-width:1040px;margin:0 auto;padding:44px 24px 80px}
.eyebrow{font-family:'IBM Plex Sans',system-ui,sans-serif;font-size:12px;font-weight:600;letter-spacing:.12em;text-transform:uppercase;color:var(--accent);margin:0 0 10px}
h1{font-family:'Newsreader',Georgia,serif;font-weight:500;font-size:clamp(36px,5vw,54px);line-height:1.02;letter-spacing:-.012em;margin:0 0 10px;text-wrap:balance}
.dek{font-size:21px;color:var(--muted);margin:0 0 26px;font-style:italic}
.abstract{max-width:68ch;margin:0;padding:18px 0 0;border-top:1px solid var(--line)}
.abstract p{margin:0 0 8px}
.abstract strong{font-family:'IBM Plex Sans',system-ui,sans-serif;font-weight:600;font-size:14px;letter-spacing:.02em}
.fig{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:18px 44px;padding:44px 0 52px;border-top:1px solid var(--line);margin-top:40px;align-items:start}
.fig>header{grid-column:1/-1}
.fig-wide{grid-template-columns:1fr}
.fig h2{font-family:'Newsreader',Georgia,serif;font-weight:500;font-size:34px;line-height:1.1;margin:0 0 6px;letter-spacing:-.01em}
.fig .source{margin:0;font-style:italic;color:var(--muted);font-size:16px;max-width:70ch}
figure{margin:0;min-width:0}
svg.fig-svg{display:block;width:100%;height:auto;color:var(--muted)}
#fig1 svg.fig-svg{max-width:520px}
figcaption{margin-top:12px;font-size:15px;line-height:1.45;color:var(--muted);font-style:italic;max-width:74ch}
.ms{margin:0;display:grid;gap:12px 20px;align-content:start}
.ms .row{display:grid;grid-template-columns:1fr;gap:4px}
.ms dt{font-family:'IBM Plex Sans',system-ui,sans-serif;font-weight:600;font-size:14px;line-height:1.4}
.ms dd{margin:0;font-size:16px;line-height:1.45}
.ms.ihi .bar{display:inline-block;color:#fff;padding:4px 10px;font-size:16px;font-weight:600}
.ms.five{grid-template-columns:repeat(5,minmax(0,1fr))}
.new{margin:0;display:grid;grid-template-columns:max-content 1fr;gap:6px 18px;align-items:baseline;padding:12px 18px;border-left:4px solid var(--accent);background:var(--surface);max-width:86ch}
.new dt{font-family:'IBM Plex Sans',system-ui,sans-serif;font-weight:600;font-size:15px;display:flex;align-items:center;gap:8px}
.new .chip{width:10px;height:10px;border-radius:50%;display:inline-block}
.new dd{margin:0;font-size:17px}
.actions{display:flex;gap:14px;align-items:center;flex-wrap:wrap}
.hint{font-family:'IBM Plex Sans',system-ui,sans-serif;font-size:13px;color:var(--muted)}
button{font-family:'IBM Plex Sans',system-ui,sans-serif;font-weight:600;font-size:14px;color:var(--accent);background:var(--surface);border:1.5px solid var(--accent);border-radius:999px;padding:10px 18px;cursor:pointer}
button:hover{background:var(--accent-soft)}
button:focus-visible{outline:3px solid var(--accent);outline-offset:2px}
button:disabled{opacity:.6;cursor:default}
footer{margin-top:56px;padding-top:18px;border-top:1px solid var(--line);font-family:'IBM Plex Sans',system-ui,sans-serif;font-size:13px;color:var(--muted);line-height:1.7}
footer p{margin:0}
footer a{color:var(--accent)}
/* svg */
.lbl{font-family:'IBM Plex Sans',system-ui,sans-serif;font-weight:500;fill:var(--ink)}
.ihi-lbl{font-family:'IBM Plex Sans',system-ui,sans-serif;font-weight:700}
.ihi-center{font-family:'IBM Plex Sans',system-ui,sans-serif;font-weight:700;fill:var(--ink);opacity:.8}
.disk{fill:var(--disk)}
.arrow{fill:none;stroke:currentColor;stroke-width:1.8}
.arrow-lbl{font-family:'IBM Plex Sans',system-ui,sans-serif;fill:currentColor}
.it{font-style:italic}
.axis{fill:none;stroke:var(--ink);stroke-width:2}
.axis-lbl{font-family:'IBM Plex Sans',system-ui,sans-serif;fill:var(--muted);letter-spacing:.14em;text-transform:uppercase}
.tie{stroke:var(--muted);stroke-width:1.2;stroke-dasharray:2 4;fill:none}
.bracket{fill:none;stroke:var(--muted);stroke-width:1.2}
.house{fill:none;stroke:var(--ink);stroke-width:2.2;stroke-linejoin:round}
.venn{fill:none;stroke:var(--muted);stroke-width:1.4}
.hair{stroke:var(--muted);stroke-width:1;fill:none}
.field{fill:none;stroke:var(--muted);stroke-width:1.2;stroke-dasharray:4 5;opacity:.75}
.lens{fill:none;stroke:var(--accent);stroke-width:4}
.lens-h{stroke:var(--accent);stroke-width:9;stroke-linecap:round}
.monitor{fill:#0F1518;stroke:#22C55E;stroke-width:1.5}
.mono{font-family:'IBM Plex Mono',ui-monospace,Menlo,monospace}
.marker{font-family:'Permanent Marker',cursive}
.creep{font-family:'Creepster',Impact,fantasy;fill:var(--ink)}
.spin{transform-box:view-box;transform-origin:520px 255px;animation:spin 30s linear infinite}
@keyframes spin{to{transform:rotate(360deg)}}
@media (prefers-reduced-motion:reduce){.spin{animation:none}}
@media (max-width:760px){.page{padding:32px 18px 60px}.fig{grid-template-columns:1fr;gap:16px;padding:36px 0 40px}.fig h2{font-size:30px}.ms.five{grid-template-columns:1fr 1fr}.new{grid-template-columns:1fr;gap:2px}}
'''

HEAD_INNER = f'''<title>The Ms of Geriatrics</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="{FONTS}">
<style>{CSS}</style>'''

BODY = symbols_svg() + '''
<main class="page">
<header class="masthead">
  <p class="eyebrow">Supplement &middot; Figures 1&ndash;13</p>
  <h1>The Ms of Geriatrics</h1>
  <p class="dek">From four to N, one M at a time.</p>
  <div class="abstract">
    <p><strong>Background</strong> Older adults are complex. The supply of clinically relevant words beginning with M is finite but, it turns out, larger than five.</p>
    <p><strong>Methods</strong> Beginning from the 4Ms of an Age-Friendly Health System (Figure 1) and the Geriatric 5Ms (Figure 2), one M was added per figure. Each figure introduces only its new M; the earlier Ms are assumed, as in practice.</p>
    <p><strong>Results</strong> Fifteen Ms, then all of them. Figures 1 and 2 are real. Figures 3 through 13 are not, although Figure 7 has a point.</p>
    <p><strong>Conclusions</strong> See Figure 13. See all of them.</p>
  </div>
</header>
''' + sections + '''
<footer>
  <p>Conflicts of interest: the authors own several magnets and have considered them through the lens of a patient.</p>
  <p>Funding: none (see Money).</p>
  <p>Correspondence: M, all universes.</p>
</footer>
</main>
<script>
(function(){
  var NS='http://www.w3.org/2000/svg';
  var svg=document.getElementById('svg13'), core=document.getElementById('core13'), btn=document.getElementById('addU'),
      nlab=document.getElementById('ncount'), cons=document.getElementById('considered'), hint=document.getElementById('hint');
  if(!svg||!core||!btn) return;
  var N=16, k=1;
  btn.addEventListener('click',function(){
    var u=document.createElementNS(NS,'use');
    u.setAttribute('href','#core13');
    var dx=(Math.random()*200-100).toFixed(1), dy=(Math.random()*120-60).toFixed(1), rot=(Math.random()*16-8).toFixed(1), sc=(0.93+Math.random()*0.14).toFixed(3);
    u.setAttribute('transform','translate('+dx+' '+dy+') translate(520 300) rotate('+rot+') scale('+sc+') translate(-520 -300)');
    u.setAttribute('style','opacity:'+(0.18+Math.random()*0.16).toFixed(2)+';filter:hue-rotate('+Math.floor(Math.random()*360)+'deg)');
    svg.insertBefore(u, svg.firstElementChild.nextSibling);
    N++; k++;
    nlab.textContent='N = '+N; cons.textContent=k;
    btn.textContent = N<20 ? 'Consider another universe' : N<26 ? 'Consider another universe (they keep coming)' : N<34 ? 'Consider another universe (please)' : 'Consider another universe (the authors have dispersed)';
    hint.textContent = N===17 ? 'Each universe adds one M. This is not explained anywhere.' : '';
    if(N>=40){btn.disabled=true; btn.textContent='All universes considered. N = 40.'; hint.textContent='';}
  });
})();
</script>
'''

FRAGMENT = HEAD_INNER + "\n" + BODY
STANDALONE = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n'
              '<meta name="description" content="The Ms of Geriatrics: the real 4Ms and 5Ms, then one M per figure until the multiverse.">\n'
              + HEAD_INNER + '\n</head>\n<body>\n' + BODY + '\n</body>\n</html>\n')

with open("geriatric-ms.html","w",encoding="utf-8") as fh: fh.write(FRAGMENT)
os.makedirs("site", exist_ok=True)
with open("site/index.html","w",encoding="utf-8") as fh: fh.write(STANDALONE)
print("fragment", len(FRAGMENT), "standalone", len(STANDALONE))
