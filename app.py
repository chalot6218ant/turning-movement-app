import streamlit as st
import numpy as np

st.set_page_config(layout="wide", page_title="Traffic Turning Estimator")

# --- Sidebar: Edit Names ---
with st.sidebar:
    st.header("⚙️ Settings")
    title_text = st.text_input("Chart Title", "Year 2006 AM")
    n_name = st.text_input("North Road", "ติวานนท์")
    s_name = st.text_input("South Road", "ติวานนท์")
    e_name = st.text_input("East Road", "งามวงศ์วาน")
    w_name = st.text_input("West Road", "รัตนาธิเบศร์")

# --- Input Section ---
st.subheader("📊 ป้อนข้อมูลรวม ขาเข้า และ ขาออก")
c1, c2, c3, c4 = st.columns(4)
with c1:
    in_n = st.number_input(f"In {n_name}", value=3577)
    out_n = st.number_input(f"Out {n_name}", value=1632)
with c2:
    in_s = st.number_input(f"In {s_name}", value=2234)
    out_s = st.number_input(f"Out {s_name}", value=2458)
with c3:
    in_e = st.number_input(f"In {e_name}", value=3628)
    out_e = st.number_input(f"Out {e_name}", value=7989)
with c4:
    in_w = st.number_input(f"In {w_name}", value=4488)
    out_w = st.number_input(f"Out {w_name}", value=1847)

# --- Calculation: Fratar Balancing ---
seed = np.array([[0, 0.7, 0.15, 0.15], [0.7, 0, 0.15, 0.15], [0.15, 0.15, 0, 0.7], [0.15, 0.15, 0.7, 0]])
t_in = np.array([in_n, in_s, in_e, in_w])
t_out = np.array([out_n, out_s, out_e, out_w])
mat = seed.copy()
for _ in range(20):
    mat = (mat.T * (t_in / np.maximum(mat.sum(axis=1), 1))).T
    mat = mat * (t_out / np.maximum(mat.sum(axis=0), 1))
def gv(o, d): return int(round(mat[o, d]))

# Map: N->E(L), N->S(T), N->W(R) | S->W(L), S->N(T), S->E(R) | E->S(L), E->W(T), E->N(R) | W->N(L), W->E(T), W->S(R)
vals = {
    'nl': gv(0, 2), 'nt': gv(0, 1), 'nr': gv(0, 3),
    'sl': gv(1, 3), 'st': gv(1, 0), 'sr': gv(1, 2),
    'el': gv(2, 1), 'et': gv(2, 3), 'er': gv(2, 0),
    'wl': gv(3, 0), 'wt': gv(3, 2), 'wr': gv(3, 1)
}

# --- SVG Drawing ---
svg = f"""
<div style="display: flex; justify-content: center;">
<svg viewBox="0 0 800 650" xmlns="http://www.w3.org/2000/svg" style="width: 100%; max-width: 800px; background: white; border: 1px solid #ccc;">
    <rect width="100%" height="100%" fill="white" />
    <text x="400" y="40" text-anchor="middle" font-size="22" font-weight="bold">{title_text}</text>

    <path d="M 330 50 V 250 M 470 50 V 250 M 330 400 V 600 M 470 400 V 600" stroke="black" stroke-width="2" fill="none"/>
    <path d="M 50 250 H 330 M 50 400 H 330 M 470 250 H 750 M 470 400 H 750" stroke="black" stroke-width="2" fill="none"/>
    <line x1="400" y1="50" x2="400" y2="250" stroke="#ccc" stroke-dasharray="5,5" />
    <line x1="400" y1="400" x2="400" y2="600" stroke="#ccc" stroke-dasharray="5,5" />
    <line x1="50" y1="325" x2="330" y2="325" stroke="#ccc" stroke-dasharray="5,5" />
    <line x1="470" y1="325" x2="750" y2="325" stroke="#ccc" stroke-dasharray="5,5" />

    <text x="415" y="150" transform="rotate(-90 415,150)" font-size="14" font-weight="bold" fill="blue">{n_name}</text>
    <text x="415" y="500" transform="rotate(-90 415,500)" font-size="14" font-weight="bold" fill="blue">{s_name}</text>
    <text x="610" y="315" font-size="14" font-weight="bold" fill="blue">{e_name}</text>
    <text x="130" y="315" font-size="14" font-weight="bold" fill="blue">{w_name}</text>

    <rect x="340" y="60" width="55" height="25" fill="#f8d7da" stroke="black"/><text x="367.5" y="77" text-anchor="middle" font-size="11">Out:{out_n}</text>
    <rect x="405" y="60" width="55" height="25" fill="#d4edda" stroke="black"/><text x="432.5" y="77" text-anchor="middle" font-size="11">In:{in_n}</text>
    
    <rect x="340" y="565" width="55" height="25" fill="#d4edda" stroke="black"/><text x="367.5" y="582" text-anchor="middle" font-size="11">In:{in_s}</text>
    <rect x="405" y="565" width="55" height="25" fill="#f8d7da" stroke="black"/><text x="432.5" y="582" text-anchor="middle" font-size="11">Out:{out_s}</text>

    <g transform="translate(410,210)">
        <rect width="25" height="20" fill="white" stroke="black"/><text x="12.5" y="14" text-anchor="middle" font-size="10">{vals['nl']}</text>
        <path d="M 12 25 v 10 h 15" fill="none" stroke="red" stroke-width="2" marker-end="url(#arrowred)"/>
    </g>
    <g transform="translate(440,210)">
        <rect width="25" height="20" fill="white" stroke="black"/><text x="12.5" y="14" text-anchor="middle" font-size="10">{vals['nt']}</text>
        <path d="M 12 25 v 15" fill="none" stroke="red" stroke-width="2" marker-end="url(#arrowred)"/>
    </g>
    <g transform="translate(470,210)">
        <rect width="25" height="20" fill="white" stroke="black"/><text x="12.5" y="14" text-anchor="middle" font-size="10">{vals['nr']}</text>
        <path d="M 12 25 v 10 h -15" fill="none" stroke="red" stroke-width="2" marker-end="url(#arrowred)"/>
    </g>

    <g transform="translate(305,420)">
        <rect width="25" height="20" fill="white" stroke="black"/><text x="12.5" y="14" text-anchor="middle" font-size="10">{vals['sr']}</text>
        <path d="M 12 -5 v -10 h 15" fill="none" stroke="green" stroke-width="2" marker-end="url(#arrowgreen)"/>
    </g>
    <g transform="translate(335,420)">
        <rect width="25" height="20" fill="white" stroke="black"/><text x="12.5" y="14" text-anchor="middle" font-size="10">{vals['st']}</text>
        <path d="M 12 -5 v -15" fill="none" stroke="green" stroke-width="2" marker-end="url(#arrowgreen)"/>
    </g>
    <g transform="translate(365,420)">
        <rect width="25" height="20" fill="white" stroke="black"/><text x="12.5" y="14" text-anchor="middle" font-size="10">{vals['sl']}</text>
        <path d="M 12 -5 v -10 h -15" fill="none" stroke="green" stroke-width="2" marker-end="url(#arrowgreen)"/>
    </g>

    <g transform="translate(300,260)">
        <rect width="25" height="20" fill="white" stroke="black"/><text x="12.5" y="14" text-anchor="middle" font-size="10">{vals['wr']}</text>
        <path d="M 30 10 h 10 v 15" fill="none" stroke="orange" stroke-width="2" marker-end="url(#arroworange)"/>
    </g>
    <g transform="translate(300,285)">
        <rect width="25" height="20" fill="white" stroke="black"/><text x="12.5" y="14" text-anchor="middle" font-size="10">{vals['wt']}</text>
        <path d="M 30 10 h 15" fill="none" stroke="orange" stroke-width="2" marker-end="url(#arroworange)"/>
    </g>
    <g transform="translate(300,310)">
        <rect width="25" height="20" fill="white" stroke="black"/><text x="12.5" y="14" text-anchor="middle" font-size="10">{vals['wl']}</text>
        <path d="M 30 10 h 10 v -15" fill="none" stroke="orange" stroke-width="2" marker-end="url(#arroworange)"/>
    </g>

    <g transform="translate(475,340)">
        <rect width="25" height="20" fill="white" stroke="black"/><text x="12.5" y="14" text-anchor="middle" font-size="10">{vals['er']}</text>
        <path d="M -5 10 h -10 v -15" fill="none" stroke="purple" stroke-width="2" marker-end="url(#arrowpurple)"/>
    </g>
    <g transform="translate(475,365)">
        <rect width="25" height="20" fill="white" stroke="black"/><text x="12.5" y="14" text-anchor="middle" font-size="10">{vals['et']}</text>
        <path d="M -5 10 h -15" fill="none" stroke="purple" stroke-width="2" marker-end="url(#arrowpurple)"/>
    </g>
    <g transform="translate(475,390)">
        <rect width="25" height="20" fill="white" stroke="black"/><text x="12.5" y="14" text-anchor="middle" font-size="10">{vals['el']}</text>
        <path d="M -5 10 h -10 v 15" fill="none" stroke="purple" stroke-width="2" marker-end="url(#arrowpurple)"/>
    </g>

    <defs>
        <marker id="arrowred" markerWidth="10" markerHeight="10" refX="5" refY="5" orient="auto"><path d="M0
