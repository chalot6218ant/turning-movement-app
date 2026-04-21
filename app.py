import streamlit as st
import numpy as np

st.set_page_config(layout="wide", page_title="Traffic Turning Estimator")

# --- Sidebar ---
with st.sidebar:
    st.header("📍 Edit Road Names")
    title_text = st.text_input("หัวข้อแผนภูมิ", "Traffic Movement Diagram")
    n_name = st.text_input("ทิศเหนือ (North)", "ติวานนท์")
    s_name = st.text_input("ทิศใต้ (South)", "ติวานนท์")
    e_name = st.text_input("ทิศตะวันออก (East)", "งามวงศ์วาน")
    w_name = st.text_input("ทิศตะวันตก (West)", "รัตนาธิเบศร์")

# --- Input ---
st.subheader("📊 ป้อนปริมาณจราจร ขาเข้า และ ขาออก (PCU/Hr.)")
c1, c2, c3, c4 = st.columns(4)
with c1:
    in_n, out_n = st.number_input(f"In {n_name}", value=3577), st.number_input(f"Out {n_name}", value=1632)
with c2:
    in_s, out_s = st.number_input(f"In {s_name}", value=2234), st.number_input(f"Out {s_name}", value=2458)
with c3:
    in_e, out_e = st.number_input(f"In {e_name}", value=3628), st.number_input(f"Out {e_name}", value=7989)
with c4:
    in_w, out_w = st.number_input(f"In {w_name}", value=4488), st.number_input(f"Out {w_name}", value=1847)

# --- Algorithm: Fratar Method ---
seed = np.array([[0, 0.7, 0.15, 0.15], [0.7, 0, 0.15, 0.15], [0.15, 0.15, 0, 0.7], [0.15, 0.15, 0.7, 0]])
targets_in = np.array([in_n, in_s, in_e, in_w])
targets_out = np.array([out_n, out_s, out_e, out_w])
matrix = seed.copy()
for _ in range(15):
    matrix = (matrix.T * (targets_in / np.maximum(matrix.sum(axis=1), 1))).T
    matrix = matrix * (targets_out / np.maximum(matrix.sum(axis=0), 1))

def gv(o, d): return int(round(matrix[o, d]))

# คำนวณค่า Turning
nl, nt, nr = gv(0, 2), gv(0, 1), gv(0, 3) # From N
sl, st, sr = gv(1, 3), gv(1, 0), gv(1, 2) # From S
el, et, er = gv(2, 1), gv(2, 3), gv(2, 0) # From E
wl, wt, wr = gv(3, 0), gv(3, 2), gv(3, 1) # From W

# --- SVG Drawing ---
svg = f"""
<div style="display: flex; justify-content: center;">
<svg viewBox="0 0 800 650" xmlns="http://www.w3.org/2000/svg" style="width: 100%; max-width: 800px; background: white; border: 1px solid #ccc;">
    <defs>
        <marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto">
            <path d="M0,0 L10,5 L0,10 Z" fill="#555" />
        </marker>
    </defs>
    <rect width="100%" height="100%" fill="white" />
    <text x="400" y="40" text-anchor="middle" font-size="20" font-weight="bold">{title_text}</text>

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

    <g transform="translate(340, 60)"><rect width="55" height="25" fill="white" stroke="black"/><text x="27.5" y="17" text-anchor="middle" font-size="10">Out:{out_n}</text></g>
    <g transform="translate(405, 60)"><rect width="55" height="25" fill="white" stroke="black"/><text x="27.5" y="17" text-anchor="middle" font-size="10">In:{in_n}</text></g>
    <g transform="translate(340, 565)"><rect width="55" height="25" fill="white" stroke="black"/><text x="27.5" y="17" text-anchor="middle" font-size="10">In:{in_s}</text></g>
    <g transform="translate(405, 565)"><rect width="55" height="25" fill="white" stroke="black"/><text x="27.5" y="17" text-anchor="middle" font-size="10">Out:{out_s}</text></g>

    <rect x="405" y="215" width="20" height="18" fill="white" stroke="black"/><text x="415" y="228" text-anchor="middle" font-size="9">{nl}</text>
    <path d="M 415 233 v 25 h 40" fill="none" stroke="#555" stroke-width="1.5" marker-end="url(#arrow)"/>
    <rect x="428" y="215" width="25" height="18" fill="white" stroke="black"/><text x="440.5" y="228" text-anchor="middle" font-size="9">{nt}</text>
    <path d="M 440 233 v 40" fill="none" stroke="#555" stroke-width="1.5" marker-end="url(#arrow)"/>
    <rect x="456" y="215" width="20" height="18" fill="white" stroke="black"/><text x="466" y="228" text-anchor="middle" font-size="9">{nr}</text>
    <path d="M 466 233 v 15 h -120" fill="none" stroke="#555" stroke-width="1.5" marker-end="url(#arrow)"/>

    <rect x="325" y="417" width="20" height="18" fill="white" stroke="black"/><text x="335" y="430" text-anchor="middle" font-size="9">{sr}</text>
    <path d="M 335 417 v -15 h 120" fill="none" stroke="#555" stroke-width="1.5" marker-end="url(#arrow)"/>
    <rect x="348" y="417" width="25" height="18" fill="white" stroke="black"/><text x="360.5" y="430" text-anchor="middle" font-size="9">{st}</text>
    <path d="M 360 417 v -40" fill="none" stroke="#555" stroke-width="1.5" marker-end="url(#arrow)"/>
    <rect x="376" y="417" width="20" height="18" fill="white" stroke="black"/><text x="386" y="430" text-anchor="middle" font-size="9">{sl}</text>
    <path d="M 386 417 v -25 h -40" fill="none" stroke="#555" stroke-width="1.5" marker-end="url(#arrow)"/>

    <rect x="275" y="303" width="25" height="18" fill="white" stroke="black"/><text x="287.5" y="316" text-anchor="middle" font-size="9">{wl}</text>
    <path d="M 300 312 h 25 v -50" fill="none" stroke="#555" stroke-width="1.5" marker-end="url(#arrow)"/>
    <rect x="275" y="280" width="25" height="18" fill="white" stroke="black"/><text x="287.5" y="293" text-anchor="middle" font-size="9">{wt}</text>
    <path d="M 300 289 h 150" fill="none" stroke="#555" stroke-width="1.5" marker-end="url(#arrow)"/>
    <rect x="275" y="257" width="25" height="18" fill="white" stroke="black"/><text x="287.5" y="270" text-anchor="middle" font-size="9">{wr}</text>
    <path d="M 300 266 h 40 v 120" fill="none" stroke="#555" stroke-width="1.5" marker-end="url(#arrow)"/>

    <rect x="500" y="328" width="25" height="18" fill="white" stroke="black"/><text x="512.5" y="341" text-anchor="middle" font-size="9">{er}</text>
    <path d="M 500 337 h -45 v -70" fill="none" stroke="#555" stroke-width="1.5" marker-end="url(#arrow)"/>
    <rect x="500" y="351" width="25" height="18" fill="white" stroke="black"/><text x="512.5" y="364" text-anchor="middle" font-size="9">{et}</text>
    <path d="M 500 360 h -150" fill="none" stroke="#555" stroke-width="1.5" marker-end="url(#arrow)"/>
    <rect x="500" y="374" width="25" height="18" fill="white" stroke="black"/><text x="512.5" y="387" text-anchor="middle" font-size="9">{el}</text>
    <path d="M 500 383 h -25 v 40" fill="none" stroke="#555" stroke-width="1.5" marker-end="url(#arrow)"/>

    <g transform="translate(720, 80)"><circle r="25" fill="none" stroke="black"/><path d="M 0 -20 L 5 0 L -5 0 Z" fill="red"/><text y="15" text-anchor="middle" font-weight="bold">N</text></g>
</svg>
</div>
"""

st.components.v1.html(svg, height=650)
