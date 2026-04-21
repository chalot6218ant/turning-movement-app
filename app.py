import streamlit as st
import numpy as np

st.set_page_config(layout="wide", page_title="Traffic Analysis")

# --- Sidebar ---
with st.sidebar:
    st.header("📝 Edit Road Names")
    title_text = st.text_input("Chart Title", "Traffic Movement Diagram")
    n_road = st.text_input("North Road", "ติวานนท์ (N)")
    s_road = st.text_input("South Road", "ติวานนท์ (S)")
    e_road = st.text_input("East Road", "งามวงศ์วาน")
    w_road = st.text_input("West Road", "รัตนาธิเบศร์")

# --- Input ---
st.subheader("📊 ป้อนปริมาณจราจร (PCU/Hr)")
col1, col2, col3, col4 = st.columns(4)
with col1:
    in_n, out_n = st.number_input(f"In {n_road}", value=3577), st.number_input(f"Out {n_road}", value=1632)
with col2:
    in_s, out_s = st.number_input(f"In {s_road}", value=2234), st.number_input(f"Out {s_road}", value=2458)
with col3:
    in_e, out_e = st.number_input(f"In {e_road}", value=3628), st.number_input(f"Out {e_road}", value=7989)
with col4:
    in_w, out_w = st.number_input(f"In {w_road}", value=4488), st.number_input(f"Out {w_road}", value=1847)

# --- Calculation ---
t_in = np.array([in_n, in_s, in_e, in_w])
t_out = np.array([out_n, out_s, out_e, out_w])
seed = np.array([[0, 0.7, 0.15, 0.15], [0.7, 0, 0.15, 0.15], [0.15, 0.15, 0, 0.7], [0.15, 0.15, 0.7, 0]])
mat = seed.copy()
for _ in range(20):
    mat = (mat.T * (t_in / np.maximum(mat.sum(axis=1), 1))).T
    mat = mat * (t_out / np.maximum(mat.sum(axis=0), 1))

def gv(o, d): return int(round(mat[o, d]))
sum_in, sum_out = int(t_in.sum()), int(t_out.sum())

v = {
    'nl': gv(0, 2), 'nt': gv(0, 1), 'nr': gv(0, 3),
    'sl': gv(1, 3), 'st': gv(1, 0), 'sr': gv(1, 2),
    'el': gv(2, 1), 'et': gv(2, 3), 'er': gv(2, 0),
    'wl': gv(3, 0), 'wt': gv(3, 2), 'wr': gv(3, 1)
}

# --- SVG Drawing ---
svg_content = f"""
<div style="display: flex; justify-content: center;">
<svg viewBox="0 0 800 700" xmlns="http://www.w3.org/2000/svg" style="background:white; border:1px solid #333;">
    <rect width="800" height="60" fill="#f0f0f0" />
    <text x="400" y="38" text-anchor="middle" font-size="22" font-weight="bold" fill="#333">{title_text}</text>
    
    <path d="M 320 60 V 250 M 480 60 V 250 M 320 450 V 620 M 480 450 V 620" stroke="black" stroke-width="2.5" fill="none"/>
    <path d="M 50 250 H 320 M 50 450 H 320 M 480 250 H 750 M 480 450 H 750" stroke="black" stroke-width="2.5" fill="none"/>
    
    <line x1="400" y1="60" x2="400" y2="250" stroke="#aaa" stroke-dasharray="5,5" />
    <line x1="400" y1="450" x2="400" y2="620" stroke="#aaa" stroke-dasharray="5,5" />
    <line x1="50" y1="350" x2="320" y2="350" stroke="#aaa" stroke-dasharray="5,5" />
    <line x1="480" y1="350" x2="750" y2="350" stroke="#aaa" stroke-dasharray="5,5" />

    <text x="415" y="110" transform="rotate(-90 415,110)" font-size="14" font-weight="bold" fill="blue">{n_road}</text>
    <text x="415" y="550" transform="rotate(-90 415,550)" font-size="14" font-weight="bold" fill="blue">{s_road}</text>
    <text x="630" y="340" font-size="14" font-weight="bold" fill="blue">{e_road}</text>
    <text x="110" y="340" font-size="14" font-weight="bold" fill="blue">{w_road}</text>

    <g font-size="11" font-weight="bold">
        <rect x="330" y="65" width="65" height="25" fill="#ffdada" stroke="#000"/><text x="362.5" y="82" text-anchor="middle">Out:{out_n}</text>
        <rect x="405" y="65" width="65" height="25" fill="#daffda" stroke="#000"/><text x="437.5" y="82" text-anchor="middle">In:{in_n}</text>
        <rect x="330" y="585" width="65" height="25" fill="#daffda" stroke="#000"/><text x="362.5" y="602" text-anchor="middle">In:{in_s}</text>
        <rect x="405" y="585" width="65" height="25" fill="#ffdada" stroke="#000"/><text x="437.5" y="602" text-anchor="middle">Out:{out_s}</text>
        <rect x="55" y="260" width="65" height="25" fill="#daffda" stroke="#000"/><text x="87.5" y="277" text-anchor="middle">In:{in_w}</text>
        <rect x="55" y="415" width="65" height="25" fill="#ffdada" stroke="#000"/><text x="87.5" y="432" text-anchor="middle">Out:{out_w}</text>
        <rect x="680" y="260" width="65" height="25" fill="#daffda" stroke="#000"/><text x="712.5" y="277" text-anchor="middle">In:{in_e}</text>
        <rect x="680" y="415" width="65" height="25" fill="#ffdada" stroke="#000"/><text x="712.5" y="432" text-anchor="middle">Out:{out_e}</text>
    </g>

    <g font-size="12" font-weight="bold" fill="#333">
        <text x="405" y="240">↰ {v['nl']}</text>
        <text x="435" y="240">↓ {v['nt']}</text>
        <text x="462" y="240">↱ {v['nr']}</text>
    </g>

    <g font-size="12" font-weight="bold" fill="#333">
        <text x="325" y="465">↰ {v['sr']}</text>
        <text x="352" y="465">↑ {v['st']}</text>
        <text x="380" y="465">↱ {v['sl']}</text>
    </g>

    <g font-size="12" font-weight="bold" fill="#333">
        <text x="280" y="375">↱ {v['wr']}</text>
        <text x="280" y="405">→ {v['wt']}</text>
        <text x="280" y="435">↳ {v['wl']}</text>
    </g>

    <g font-size="12" font-weight="bold" fill="#333" text-anchor="end">
        <text x="520" y="275">{v['er']} ↰</text>
        <text x="520" y="305">{v['et']} ←</text>
        <text x="520" y="335">{v['el']} ↲</text>
    </g>

    <rect x="580" y="520" width="190" height="90" fill="#fdfdfd" stroke="#333" rx="5" stroke-width="1"/>
    <text x="675" y="540" text-anchor="middle" font-size="13" font-weight="bold">Summary Total</text>
    <line x1="590" y1="545" x2="760" y2="545" stroke="#eee" />
    <text x="595" y="565" font-size="11" fill="green">Total In: {sum_in:,}</text>
    <text x="595" y="583" font-size="11" fill="red">Total Out: {sum_out:,}</text>
    <text x="595" y="602" font-size="12" font-weight="bold">Grand Total: {sum_in + sum_out:,}</text>

    <g transform="translate(740, 100)"><circle r="18" fill="none" stroke="#666"/><path d="M 0 -14 L 3 0 L -3 0 Z" fill="red"/><text y="15" text-anchor="middle" font-size="9" font-weight="bold">N</text></g>
</svg>
</div>
"""

st.components.v1.html(svg_content, height=720)
