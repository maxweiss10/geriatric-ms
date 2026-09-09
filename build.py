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
 'lion': '<polygon points="0.0,-33.0 5.3,-24.5 13.4,-30.3 15.0,-20.4 24.7,-22.7 22.4,-13.0 32.3,-11.4 26.5,-3.3 35.0,2.0 26.5,7.3 32.3,15.4 22.4,17.0 24.7,26.7 15.0,24.4 13.4,34.3 5.3,28.5 0.0,37.0 -5.3,28.5 -13.4,34.3 -15.0,24.4 -24.7,26.7 -22.4,17.0 -32.3,15.4 -26.5,7.3 -35.0,2.0 -26.5,-3.3 -32.3,-11.4 -22.4,-13.0 -24.7,-22.7 -15.0,-20.4 -13.4,-30.3 -5.3,-24.5" fill="#C8742A"/><circle cx="-14" cy="-16" r="6.5" fill="#C8742A"/><circle cx="14" cy="-16" r="6.5" fill="#C8742A"/><circle cy="3" r="19" fill="#E8B458"/><circle cx="-7" cy="-1" r="2.4" fill="#3B2A14"/><circle cx="7" cy="-1" r="2.4" fill="#3B2A14"/><path d="M-4,8 L4,8 L0,13 Z" fill="#3B2A14"/><path d="M0,13 L0,17 M-6,19 C-3,22 3,22 6,19" fill="none" stroke="#3B2A14" stroke-width="1.6" stroke-linecap="round"/>',
 'poop': '<ellipse cx="0" cy="21" rx="31" ry="12"/><ellipse cx="0" cy="8" rx="24" ry="11"/><ellipse cx="0" cy="-5" rx="17" ry="9"/><path d="M-9,-10 C-12,-19 -4,-31 6,-31 C13,-31 12,-22 5,-17 C1,-14 -4,-12 -9,-10 Z"/><circle cx="-8" cy="10" r="3.2" fill="var(--paper)"/><circle cx="8" cy="10" r="3.2" fill="var(--paper)"/><path d="M-7,17 Q0,23 7,17" fill="none" stroke="var(--paper)" stroke-width="2" stroke-linecap="round"/>',
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
 'miralax':  dict(label='Miralax',         icon='poop',      color='#8B5A2B'),
 'middle':   dict(label='Matters Middle',  icon='hearthalf', color='#9A86C8'),
 'magnets':  dict(label='Magnets',         icon='magnet',    color='#D0342C'),
 'morbid':   dict(label='Multimorbidity',  icon='skull',     color='#111111'),
 'mufasa':   dict(label='Mufasa',          icon='lion',      color='#C8742A'),
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

def toward(ax,ay,bx,by,d):
    ddx,ddy = bx-ax, by-ay; l = math.hypot(ddx,ddy) or 1
    return (ax+ddx/l*d, ay+ddy/l*d)

def qarrow(p1, p2, r1, r2, ctrl, marker, cls="arrow", gap1=4, gap2=8):
    (x1,y1),(x2,y2) = p1,p2; qx,qy = ctrl
    s = toward(x1,y1,qx,qy, r1+gap1); e = toward(x2,y2,qx,qy, r2+gap2)
    path = f'<path d="M{f(s[0])},{f(s[1])} Q{f(qx)},{f(qy)} {f(e[0])},{f(e[1])}" class="{cls}" marker-end="url(#{marker})"/>'
    mid = (0.25*s[0]+0.5*qx+0.25*e[0], 0.25*s[1]+0.5*qy+0.25*e[1])
    return path, mid

def alabel(x, y, s, anchor="middle", cls="arrow-lbl"):
    return f'<text x="{f(x)}" y="{f(y)}" class="{cls}" font-size="11" text-anchor="{anchor}">{esc(s)}</text>'

def star(cx, cy, r1, r2, n, fill, lines, lsize=8, lfill="#fff", rot=0):
    pts=[]
    for k in range(2*n):
        a = -math.pi/2 + math.pi*k/n
        rr = r1 if k%2==0 else r2
        pts.append(f"{f(cx+rr*math.cos(a))},{f(cy+rr*math.sin(a))}")
    return (f'<g transform="rotate({rot} {f(cx)} {f(cy)})"><polygon points="{" ".join(pts)}" fill="{fill}"/>'
            + text(cx, cy+3, "|".join(lines), cls="lbl", size=lsize, fill=lfill, extra=' font-weight="700" stroke="#7A0000" stroke-width="0.5" paint-order="stroke"') + '</g>')

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

# ------------------------------------------------------------------ Figures 2 to 13
Y0, Y1 = 165, 340
FLOOR, BUS_TOP, BUS_BOT, RISER = 468, 95, 433, 175
def positions(L):
    P={}
    if L==5:
        for i,k in enumerate(['mind','mobility','meds','multi','matters']): P[k]=(520+(i-2)*170, 110)
    elif L==6:
        for i,k in enumerate(['mind','mobility','meds','multi','matters','money']): P[k]=(520+(i-2.5)*150, 110)
    else:
        for i,k in enumerate(['mind','mobility','meds','multi']): P[k]=(520+(i-1.5)*180, Y0)
        row1=['matters','maint','money']+(['mict'] if L>=10 else [])
        n=len(row1)
        for i,k in enumerate(row1): P[k]=(520+(i-(n-1)/2)*180, Y1)
    return P

VB = {5:(90,-15,870,210), 6:(90,-15,870,210), 7:(130,70,780,382), 8:(110,0,820,482), 9:(110,0,820,482), 10:(110,0,820,482)}
for L in range(11,16): VB[L]=(110,0,930,545)
VB[16]=(110,-100,930,645); VB[17]=(110,-100,930,645)

MULTI_OFF = (40,-14); VR = 46   # Venn chain offset and radius
def chain_center(base, k):
    return (base[0]+MULTI_OFF[0]*k, base[1]+MULTI_OFF[1]*k)

def badge(x,y):
    return (f'<circle cx="{f(x)}" cy="{f(y)}" r="10" fill="#C48A12" stroke="var(--paper)" stroke-width="1.5"/>'
            f'<text x="{f(x)}" y="{f(y+4.2)}" class="lbl" font-size="12" font-weight="700" text-anchor="middle" fill="var(--paper)">$</text>')

def crown(x, ytop):
    pts=[(-22,6),(-22,-10),(-11,-1),(0,-15),(11,-1),(22,-10),(22,6)]
    p=" ".join(f"{f(x+dx)},{f(ytop-8+dy)}" for dx,dy in pts)
    return f'<polygon points="{p}" fill="#E0B62B" stroke="#8A6A00" stroke-width="1" stroke-linejoin="round"/>'

BIG = 1.3
def draw(L):
    P=positions(L); s=[]; defs=[marker_def(f"ah{L}")]
    mk=f"ah{L}"
    big = {'matters', 'mict'}
    def rad(k): return 42*BIG if k in big else 42
    # field lines (behind everything)
    if L>=14:
        for r in (70,150,250,370,520,700):
            s.append(f'<path d="M975,{f(250-r)} A{f(r*0.9)},{f(r)} 0 0 0 975,{f(250+r)}" class="field"/>')
    # Multicomplexity web: relational lines to every other M
    mx,my=P['multi']
    for k,(x,y) in P.items():
        if k=='multi': continue
        if L<=6:
            h = 26 + abs(x-mx)*0.09
            s.append(f'<path d="M{f(mx)},{f(my-40)} Q{f((mx+x)/2)},{f(my-40-h)} {f(x)},{f(y-rad(k)+2)}" class="web"/>')
        else:
            s.append(f'<line x1="{f(mx)}" y1="{f(my)}" x2="{f(x)}" y2="{f(y)}" class="web"/>')
    # house
    if L>=8:
        s.append(f'<path d="M130,68 L520,12 L910,68 Z" class="house"/><rect x="130" y="68" width="780" height="{FLOOR-68}" class="house"/>')
        s.append(icon('house',474,44,34,MS['milieu']['color']) + text(497,49,'Milieu',cls='lbl',size=13,anchor='start'))
    # Maintenance circuit
    if L>=7:
        s.append(f'<path d="M{RISER},{BUS_TOP} L805,{BUS_TOP} M{RISER},{BUS_TOP} L{RISER},{BUS_BOT} L805,{BUS_BOT}" class="bus"/>')
        for k in ('mind','mobility','meds','multi'):
            x,y=P[k]; s.append(f'<path d="M{f(x)},{BUS_TOP} L{f(x)},{f(y-46)}" class="bus" marker-end="url(#{mk})"/>')
        for k,(x,y) in P.items():
            if k in ('mind','mobility','meds','multi'): continue
            lab_bottom = y+ (74 if k in big else 64)
            if k=='maint':
                s.append(f'<path d="M{f(x)},{f(lab_bottom)} L{f(x)},{BUS_BOT}" class="bus"/>')
            else:
                s.append(f'<path d="M{f(x)},{BUS_BOT} L{f(x)},{f(lab_bottom+4)}" class="bus" marker-end="url(#{mk})"/>')
    # Venn: Mind / Mental
    if L>=9:
        mx0,my0=P['mind']; c=MS['mental']['color']; cx2,cy2 = mx0+40, my0+14
        s.append(f'<circle cx="{f(mx0)}" cy="{f(my0)}" r="{VR}" class="venn"/>')
        s.append(f'<circle cx="{f(cx2)}" cy="{f(cy2)}" r="{VR}" class="venn" style="stroke:{c}"/>')
        defs.append(f'<mask id="mk9-{L}" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="600"><rect x="0" y="0" width="{W}" height="600" fill="#fff"/><circle cx="{f(mx0)}" cy="{f(my0)}" r="{VR}" fill="#000"/></mask>')
        s.append(f'<circle cx="{f(cx2)}" cy="{f(cy2)}" r="{VR}" fill="{c}" opacity=".32" mask="url(#mk9-{L})"/>')
        s.append(icon('brain', mx0+64, my0+22, 30, c))
        s.append(text(cx2, cy2+64, 'Mental', size=14))
        s.append(f'<path d="M{f(mx0+88)},{f(my0+35)} L{f(mx0+102)},{f(my0+85)}" class="hair"/>')
        s.append(f'<text x="{f(mx0+106)}" y="{f(my0+96)}" class="marker" font-size="13" fill="{c}">the difference</text>')
    # Multi- chain: Multimorbidity, Multiverse
    if L>=15:
        bx,by=P['multi']
        s.append(f'<circle cx="{f(bx)}" cy="{f(by)}" r="{VR}" class="venn"/>')
        c1=chain_center((bx,by),1)
        defs.append(f'<mask id="mk15-{L}" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="600"><rect x="0" y="0" width="{W}" height="600" fill="#fff"/><circle cx="{f(bx)}" cy="{f(by)}" r="{VR}" fill="#000"/></mask>')
        s.append(f'<circle cx="{f(c1[0])}" cy="{f(c1[1])}" r="{VR}" fill="#111" opacity=".92" stroke="var(--ink)" stroke-width="1" mask="url(#mk15-{L})"/>')
        s.append(icon('skull', bx+63, by-22, 30))
        s.append(text(c1[0], by+47, 'Multimorbidity', cls='creep', size=15))
    # Mufasa
    if L>=16:
        s.append('<g transform="translate(300,-38)" opacity=".95"><rect x="-56" y="6" width="112" height="22" rx="11" class="cloud"/><circle cx="-38" cy="8" r="22" class="cloud"/><circle cx="-12" cy="-10" r="30" class="cloud"/><circle cx="20" cy="-4" r="27" class="cloud"/><circle cx="44" cy="10" r="20" class="cloud"/></g>')
        s.append(icon('lion', 300, -40, 66))
        s.append(text(300, 20, 'Mufasa', size=14))
        mx0,my0=P['mind']
        s.append(f'<path d="M318,-2 L{f(mx0+26)},{f(my0-44)}" class="beam" marker-end="url(#{mk})"/>')
        s.append('<text x="376" y="-30" class="marker" font-size="15" fill="#C8742A">Remember who you are.</text>')
    if L>=17:
        bx,by=P['multi']; c1=chain_center((bx,by),1); c2=chain_center((bx,by),2)
        defs.append(f'<mask id="mk17-{L}" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="600"><rect x="0" y="0" width="{W}" height="600" fill="#fff"/><circle cx="{f(c1[0])}" cy="{f(c1[1])}" r="{VR}" fill="#000"/><circle cx="{f(bx)}" cy="{f(by)}" r="{VR}" fill="#000"/></mask>')
        s.append(f'<circle cx="{f(c2[0])}" cy="{f(c2[1])}" r="{VR}" fill="#3B1F6E" opacity=".94" stroke="#C9A7FF" stroke-width="1" mask="url(#mk17-{L})"/>')
        sx,sy = c1[0]+62, c1[1]-22
        s.append(f'<g class="spin" style="transform-origin:{f(sx)}px {f(sy)}px"><g transform="translate({f(sx)},{f(sy)})">{icon("spiral",0,0,30,"#D4BBFF")}</g></g>')
        s.append(text(c2[0]+4, by+31, 'Multiverse', cls='creep', size=15, fill='#8E5BD9'))
    # Micturition arrows (Medications, Mobility, Mind/Mental)
    if L>=10:
        path,_ = qarrow(P['meds'], P['mict'], 50, 70, (735,235), mk); s.append(path)
        path,_ = qarrow(P['mobility'], P['mict'], 50, 70, (560,295), mk); s.append(path)
        mx0,my0=P['mind']
        path,_ = qarrow((mx0+40,my0+14), P['mict'], VR, 70, (560,235), mk, cls="arrow dotted"); s.append(path)
    # Axis along the floor
    if L>=11:
        s.append(f'<path d="M262,{FLOOR} L935,{FLOOR}" class="axis" marker-start="url(#{mk})" marker-end="url(#{mk})"/>')
        s.append(text(262, FLOOR+18, 'most', cls='axis-lbl', size=10, anchor='start'))
        s.append(text(935, FLOOR+18, 'least', cls='axis-lbl', size=10, anchor='end'))
        s.append(slot('least', 975, FLOOR, size=58, dy_label=55))
    # Miralax: subgroup of Medications
    if L>=12:
        s.append(f'<path d="M543,{Y0+27} L569,{Y0+23}" class="hair dotted"/>')
        s.append(icon('poop', 525, Y0+31, 34, MS['miralax']['color']))
        s.append(text(525, Y0+8, 'Miralax', size=13))
    # Matters Middle straddling the floor
    if L>=13:
        s.append(slot('middle', 612, FLOOR, size=56, dy_label=55))
    # Magnets
    if L>=14:
        s.append(slot('magnets', 975, 250, size=76, label=False))
        s.append('<circle cx="975" cy="250" r="50" class="lens"/><line x1="1011" y1="286" x2="1032" y2="308" class="lens-h"/>')
        s.append(text(975, 322, 'Magnets', size=14))
    # starburst
    if L>=10:
        s.append(star(866, 350, 44, 28, 12, '#E11D1D', ['VERY','IMPORTANT'], lsize=10.5))
    # slots
    for k,(x,y) in P.items():
        if k in big: s.append(slot(k, x, y, scale=BIG, dy_label=70))
        else: s.append(slot(k, x, y))
    # Matters Most crown (most important, from the start)
    x,y=P['matters']; s.append(crown(x, y-42*BIG+4))
    # Money tags: every other M can cost money
    if L>=6:
        for k,(x,y) in P.items():
            if k=='money': continue
            off = 46 if k in big else 36
            s.append(badge(x+off, y-off+2))
        if L>=8: s.append(badge(456, 32))                      # Milieu
        if L>=9:
            mx0,my0=P['mind']; s.append(badge(mx0+80, my0-16))  # Mental
        if L>=11: s.append(badge(1001, FLOOR-26))              # Matters Least
        if L>=12: s.append(badge(546, Y0+47))                  # Miralax
        if L>=13: s.append(badge(640, FLOOR-22))               # Matters Middle
        if L>=14: s.append(badge(1013, 212))                   # Magnets
        if L>=15:
            bx,by=P['multi']; s.append(badge(bx+78, by+25))     # Multimorbidity
        if L>=16: s.append(badge(352, -66))                    # Mufasa
        if L>=17:
            bx,by=P['multi']; c2=chain_center((bx,by),2); s.append(badge(c2[0]+35, c2[1]-32))  # Multiverse
    return "".join(s), "".join(defs)

ARIA = {
 5:"Five flat icons in a row with labels beneath: Mind, Mobility, Medications, Multicomplexity, and Matters Most, which is drawn larger with a gold crown. Dotted arcs connect Multicomplexity to each of the others.",
 6:"Six icons in a row: the five Ms plus a gold coin labeled Money. A small gold dollar tag sits on every other M.",
 7:"Seven icons in two rows. A circuit from Maintenance runs above the top row and below the bottom row with an arrowhead to every M.",
 8:"The two rows of icons now sit inside a house outline labeled Milieu.",
 9:"Inside the house, a pink circle labeled Mental overlaps the circle around Mind. The sliver that does not overlap is labeled the difference.",
 10:"Micturition, a yellow drop drawn larger than the other icons, joins the bottom row with a red starburst reading Very Important. Arrows from Medications, Mobility, and the Mind and Mental pair point to it.",
 11:"An axis runs along the house floor from most to least. Matters Least, a dashed grey heart, sits outside the house at the far end.",
 12:"A small brown poop icon labeled Miralax sits beside the Medications capsule, joined to it by a dotted line.",
 13:"Matters Middle, a half-filled heart, straddles the floor line at the midpoint of the axis.",
 14:"A horseshoe magnet outside the house, seen through a magnifying lens, sends dashed field lines through the house and everything in it.",
 15:"A black circle with a skull labeled Multimorbidity overlaps the circle around Multicomplexity. The overhang is labeled more morbid.",
 16:"A cloud above the roof holds a lion's face labeled Mufasa. A dashed golden beam runs from the cloud down to Mind, with the words Remember who you are.",
 17:"A purple circle with a spinning spiral labeled Multiverse overlaps Multimorbidity in turn, and the entire figure is drawn again in shifted, tinted copies fanning out from it.",
}

def fig_row(L):
    inner, defs = draw(L)
    return svg_wrap(inner, ARIA[L], VB[L], defs=defs)

def fig_multiverse():
    inner, defs = draw(17)
    ox,oy = chain_center(positions(17)['multi'],2)
    ghosts=[]
    for (dx,dy,rot,sc,hue) in [(-30,-18,-5,0.985,110),(26,22,4,1.01,230),(-12,30,-2,0.97,320)]:
        ghosts.append(f'<use href="#core13" transform="translate({dx} {dy}) translate({f(ox)} {f(oy)}) rotate({rot}) scale({sc}) translate({f(-ox)} {f(-oy)})" style="opacity:.28;filter:hue-rotate({hue}deg)"/>')
    body = "".join(ghosts) + f'<g id="core13">{inner}</g>'
    return svg_wrap(body, ARIA[17], VB[17], defs=defs, id_="svg13")

# ------------------------------------------------------------------ page assembly
def new_m(key, desc):
    m=MS[key]
    return (f'<dl class="new" style="border-left-color:{m["color"]}"><dt><span class="chip" style="background:{m["color"]}"></span>{esc(m["label"])}</dt>'
            f'<dd>{esc(desc)}</dd></dl>')

def section(num, title, svg, source="", body_html="", wide=False, body_after=False, after_html=""):
    cls = ("fig fig-wide" if wide else "fig") + (" active" if num==1 else "")
    src_html = f'<p class="source">{esc(source)}</p>' if source else ""
    return f"""
<section class="{cls}" id="s{num}">
  <header>
    <p class="eyebrow">Figure {num}</p>
    <h2>{esc(title)}</h2>
    {src_html}
  </header>
  {"" if body_after else body_html}
  <figure>
    {svg}
  </figure>
  {body_html if body_after else ""}{after_html}
</section>"""

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
 section(1,"The 4Ms", fig_ihi(), source="Age-Friendly Health Systems. The John A. Hartford Foundation, the Institute for Healthcare Improvement, and the American Hospital Association.",
   body_html=f'<dl class="ms ihi">{DL4}</dl>'),
 section(2,"The 5Ms", fig_row(5), source="Tinetti M, Huang A, Molnar F. J Am Geriatr Soc. 2017;65(9):2115.",
   body_html=f'<dl class="ms five">{DL5}</dl>', wide=True, body_after=True),
 section(3,"The 6Ms", fig_row(6), body_html=new_m('money',"Financial considerations. Not all patients, families, or systems will have the resources to optimize each of these considerations."), wide=True),
 section(4,"The 7Ms", fig_row(7), body_html=new_m('maint',"Is this actually sustainable? Also the S in SMART goals. Ask this question of every M; each M should have a SMART goal: Specific, Measurable, Achievable, Relevant, Time-bound."), wide=True),
 section(5,"The 8Ms", fig_row(8), body_html=new_m('milieu',"Consider the milieu: the environment, systems, and context in which the patient and the other components exist. Context is vital to understanding the patient."), wide=True),
 section(6,"The 9Ms", fig_row(9), body_html=new_m('mental',"Similar to Mind, but also slightly different. Consider each."), wide=True),
 section(7,"The 10Ms", fig_row(10), body_html=new_m('mict',"Often considered the sixth vital sign in medicine. Especially important in geriatric patients."), wide=True),
 section(8,"The 11Ms", fig_row(11), body_html=new_m('least',"We have considered what Matters Most, but we also need to think about what we do not need to think about."), wide=True),
 section(9,"The 12Ms", fig_row(12), body_html=new_m('miralax',"Some scholars consider it encompassed by Medications, but it is a vital one. Easily missed on review, since it tends to pass right through."), wide=True),
 section(10,"The 13Ms", fig_row(13), body_html=new_m('middle',"Everything between Matters Most and Matters Least."), wide=True),
 section(11,"The 14Ms", fig_row(14), body_html=new_m('magnets',"The scientific community remains undecided on how they work. Consider them through the lens of your patient."), wide=True),
 section(12,"The 15Ms", fig_row(15), body_html=new_m('morbid',"Like Multicomplexity, but more morbid."), wide=True),
 section(13,"The 16Ms", fig_row(16), body_html=new_m('mufasa',"Father of Simba, brother of Scar. Sadly, Mufasa passed away at the hands of his brother, and this was witnessed by Simba."), wide=True),
 section(14,"The N Ms", fig_multiverse(),
   body_html=new_m('verse',"Like Multimorbidity, but more verse. Have you considered all multiversal variations of all possible Ms of the patient? Consider one more below."),
   after_html='<div class="actions"><button type="button" id="addU">Consider another universe</button><span class="hint" id="ncount">N = 17</span></div>', wide=True),
])

FONTS = "https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;0,6..72,600;1,6..72,400&family=IBM+Plex+Sans:wght@400;500;600&family=Permanent+Marker&family=Creepster&display=swap"

CSS = '''
:root{--paper:#F4F6F3;--surface:#FFFFFF;--ink:#1A222B;--muted:#5B6672;--line:#CFD7D3;--accent:#146C7A;--accent-soft:#D7E9EC;--disk:#E3F0F9;color-scheme:light}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--paper:#0F1518;--surface:#182126;--ink:#E7ECEA;--muted:#97A4AA;--line:#2A3538;--accent:#4FB3C1;--accent-soft:#173C43;--disk:#16232D;color-scheme:dark}}
:root[data-theme="dark"]{--paper:#0F1518;--surface:#182126;--ink:#E7ECEA;--muted:#97A4AA;--line:#2A3538;--accent:#4FB3C1;--accent-soft:#173C43;--disk:#16232D;color-scheme:dark}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);font-family:'Newsreader',Georgia,'Times New Roman',serif;font-size:17px;line-height:1.5;-webkit-font-smoothing:antialiased}
.page{max-width:1180px;margin:0 auto;padding:36px 24px 120px}
.masthead{display:flex;align-items:baseline;justify-content:space-between;gap:16px;flex-wrap:wrap;border-bottom:1px solid var(--line);padding-bottom:14px}
.masthead h1{font-size:clamp(28px,4vw,40px);margin:0}
.masthead .eyebrow{margin:0}
.stepper{position:fixed;left:0;right:0;bottom:0;z-index:5;background:var(--surface);border-top:1px solid var(--line);box-shadow:0 -6px 24px rgba(0,0,0,.06)}
.stepper .in{max-width:1180px;margin:0 auto;padding:12px 24px;display:grid;grid-template-columns:auto 1fr auto;gap:16px;align-items:center}
.stepper .prog{text-align:center;font-family:'IBM Plex Sans',system-ui,sans-serif;font-size:13px;color:var(--muted);display:flex;flex-direction:column;align-items:center;gap:6px;min-width:0}
.stepper .prog b{color:var(--ink);font-weight:600}
.dots{display:flex;gap:6px;flex-wrap:wrap;justify-content:center}
.dots button{width:12px;height:12px;padding:0;border-radius:50%;border:1.5px solid var(--accent);background:transparent;cursor:pointer}
.dots button.on{background:var(--accent)}
.dots button.done{background:var(--accent-soft)}
.navbtn{font-family:'IBM Plex Sans',system-ui,sans-serif;font-weight:600;font-size:16px;border-radius:999px;padding:12px 22px;cursor:pointer;border:1.5px solid var(--accent);background:var(--surface);color:var(--accent);white-space:nowrap}
.navbtn.next{background:var(--accent);color:#fff;font-size:17px;padding:14px 26px;box-shadow:0 4px 14px rgba(20,108,122,.25)}
.navbtn.next:hover{filter:brightness(1.08)}
.navbtn:disabled{opacity:.35;cursor:default;box-shadow:none}
.navbtn:focus-visible{outline:3px solid var(--accent);outline-offset:2px}
.kbd{font-family:'IBM Plex Sans',system-ui,sans-serif;font-size:11px;color:var(--muted)}
.kbd kbd{border:1px solid var(--line);border-radius:4px;padding:0 5px;font-family:inherit}
.eyebrow{font-family:'IBM Plex Sans',system-ui,sans-serif;font-size:12px;font-weight:600;letter-spacing:.12em;text-transform:uppercase;color:var(--accent);margin:0 0 10px}
h1{font-family:'Newsreader',Georgia,serif;font-weight:500;font-size:clamp(36px,5vw,54px);line-height:1.02;letter-spacing:-.012em;margin:0 0 10px;text-wrap:balance}
.dek{font-size:21px;color:var(--muted);margin:0 0 26px;font-style:italic}
.abstract{max-width:68ch;margin:0;padding:18px 0 0;border-top:1px solid var(--line)}
.abstract p{margin:0 0 8px}
.abstract strong{font-family:'IBM Plex Sans',system-ui,sans-serif;font-weight:600;font-size:14px;letter-spacing:.02em}
.fig{display:none;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:18px 44px;padding:28px 0 40px;align-items:start}
.fig.active{display:grid}
.fig>header{grid-column:1/-1}
.fig-wide{grid-template-columns:1fr}
.fig h2{font-family:'Newsreader',Georgia,serif;font-weight:500;font-size:34px;line-height:1.1;margin:0 0 6px;letter-spacing:-.01em}
.fig .source{margin:0;font-style:italic;color:var(--muted);font-size:16px;max-width:70ch}
figure{margin:0;min-width:0}
svg.fig-svg{display:block;width:100%;height:auto;color:var(--muted)}
#s1 svg.fig-svg{max-width:620px}
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
.actions{display:flex;gap:14px;align-items:center;flex-wrap:wrap;margin-top:14px}
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
.hair.dotted{stroke-dasharray:2 3}
.field{fill:none;stroke:var(--muted);stroke-width:1.2;stroke-dasharray:4 5;opacity:.75}
.lens{fill:none;stroke:var(--accent);stroke-width:4}
.lens-h{stroke:var(--accent);stroke-width:9;stroke-linecap:round}
.bus{fill:none;stroke:var(--muted);stroke-width:1.6}
.web{fill:none;stroke:#2F6FA8;stroke-width:1.3;stroke-dasharray:2 4;opacity:.6}
.cloud{fill:#FFF7E0;stroke:#E0B62B;stroke-width:1.2}
.beam{fill:none;stroke:#C8742A;stroke-width:1.6;stroke-dasharray:6 5}
.marker{font-family:'Permanent Marker',cursive}
.creep{font-family:'Creepster',Impact,fantasy;fill:var(--ink)}
.spin{transform-box:view-box;animation:spin 24s linear infinite}
@keyframes spin{to{transform:rotate(360deg)}}
@media (prefers-reduced-motion:reduce){.spin{animation:none}}
@media (max-width:760px){.page{padding:24px 18px 140px}.stepper .in{grid-template-columns:auto 1fr auto;padding:10px 14px;gap:10px}.navbtn{padding:10px 14px;font-size:14px}.navbtn.next{font-size:15px;padding:12px 16px}.kbd{display:none}.fig{grid-template-columns:1fr;gap:16px;padding:36px 0 40px}.fig h2{font-size:30px}.ms.five{grid-template-columns:1fr 1fr}.new{grid-template-columns:1fr;gap:2px}}
'''

HEAD_INNER = f"""<title>The Ms of Geriatrics</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="{FONTS}">
<style>{CSS}</style>"""

BODY = symbols_svg() + """
<main class="page">
<header class="masthead">
  <h1>The Ms of Geriatrics</h1>
  <p class="eyebrow">One M at a time</p>
</header>
""" + sections + """
</main>
<nav class="stepper" aria-label="Figure navigation">
  <div class="in">
    <button type="button" class="navbtn" id="prev" aria-label="Previous figure">&larr; Back</button>
    <div class="prog"><div><b id="ptitle">The 4Ms</b> &middot; <span id="pcount">Figure 1 of 13</span></div><div class="dots" id="dots"></div><div class="kbd">Use <kbd>&rarr;</kbd> and <kbd>&larr;</kbd> keys</div></div>
    <button type="button" class="navbtn next" id="next" aria-label="Next figure">Next: The 5Ms &rarr;</button>
  </div>
</nav>
<script>
(function(){
  var figs=Array.prototype.slice.call(document.querySelectorAll('section.fig'));
  var titles=figs.map(function(s){return s.querySelector('h2').textContent;});
  var prev=document.getElementById('prev'), next=document.getElementById('next'), ptitle=document.getElementById('ptitle'), pcount=document.getElementById('pcount'), dots=document.getElementById('dots');
  var cur=0;
  figs.forEach(function(s,i){var b=document.createElement('button'); b.type='button'; b.title=titles[i]; b.setAttribute('aria-label',titles[i]); b.addEventListener('click',function(){go(i);}); dots.appendChild(b);});
  function go(i, quiet){
    if(i<0||i>=figs.length) return;
    cur=i;
    figs.forEach(function(s,k){ s.classList.toggle('active', k===i); });
    Array.prototype.forEach.call(dots.children,function(b,k){ b.classList.toggle('on',k===i); b.classList.toggle('done',k<i); });
    ptitle.textContent=titles[i]; pcount.textContent='Figure '+(i+1)+' of '+figs.length;
    prev.disabled = i===0;
    if(i===figs.length-1){ next.disabled=true; next.textContent='That is all of them'; }
    else { next.disabled=false; next.innerHTML='Next: '+titles[i+1]+' &rarr;'; }
    if(!quiet){ try{ history.replaceState(null,'','#fig'+(i+1)); }catch(e){} window.scrollTo({top:0,behavior:'instant'}); }
  }
  prev.addEventListener('click',function(){go(cur-1);});
  next.addEventListener('click',function(){go(cur+1);});
  document.addEventListener('keydown',function(e){
    if(e.target && /INPUT|TEXTAREA|BUTTON/.test(e.target.tagName) && e.key===' ') return;
    if(e.key==='ArrowRight'||e.key==='PageDown'){ go(cur+1); e.preventDefault(); }
    else if(e.key==='ArrowLeft'||e.key==='PageUp'){ go(cur-1); e.preventDefault(); }
  });
  var m=(location.hash||'').match(/^#fig(\\d+)$/); var start=m?Math.min(figs.length,Math.max(1,parseInt(m[1],10)))-1:0;
  go(start, true); try{window.scrollTo(0,0);}catch(e){}
  window.addEventListener('hashchange',function(){var m=(location.hash||'').match(/^#fig(\\d+)$/); if(m) go(parseInt(m[1],10)-1, true);});
})();
(function(){
  var NS='http://www.w3.org/2000/svg';
  var svg=document.getElementById('svg13'), core=document.getElementById('core13'), btn=document.getElementById('addU'), nlab=document.getElementById('ncount');
  if(!svg||!core||!btn) return;
  var OX=__OX__, OY=__OY__, N=17;
  btn.addEventListener('click',function(){
    var u=document.createElementNS(NS,'use');
    u.setAttribute('href','#core13');
    var dx=(Math.random()*120-60).toFixed(1), dy=(Math.random()*80-40).toFixed(1), rot=(Math.random()*14-7).toFixed(1), sc=(0.94+Math.random()*0.12).toFixed(3);
    u.setAttribute('transform','translate('+dx+' '+dy+') translate('+OX+' '+OY+') rotate('+rot+') scale('+sc+') translate('+(-OX)+' '+(-OY)+')');
    u.setAttribute('style','opacity:'+(0.16+Math.random()*0.16).toFixed(2)+';filter:hue-rotate('+Math.floor(Math.random()*360)+'deg)');
    svg.insertBefore(u, svg.firstElementChild.nextSibling);
    N++; nlab.textContent='N = '+N;
    if(N>=40){btn.disabled=true; btn.textContent='All universes considered.';}
  });
})();
</script>
"""
ox,oy = chain_center(positions(17)['multi'],2)
BODY = BODY.replace("__OX__", f(ox)).replace("__OY__", f(oy))

FRAGMENT = HEAD_INNER + "\n" + BODY
STANDALONE = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n'
              '<meta name="description" content="The Ms of Geriatrics: the 4Ms and 5Ms, then one M per figure.">\n'
              + HEAD_INNER + '\n</head>\n<body>\n' + BODY + '\n</body>\n</html>\n')

with open("geriatric-ms.html","w",encoding="utf-8") as fh: fh.write(FRAGMENT)
os.makedirs("site", exist_ok=True)
with open("site/index.html","w",encoding="utf-8") as fh: fh.write(STANDALONE)
print("fragment", len(FRAGMENT), "standalone", len(STANDALONE))
