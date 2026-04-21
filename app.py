import streamlit as st
import numpy as np

st.set_page_config(layout="wide", page_title="Traffic Turning Estimator")

# --- Sidebar ---
with st.sidebar:
    st.header("📍 Edit Road Names")
    title_text = st.text_input("หัวข้อแผนภูมิ", "Traffic Movement Diagram")
    n_name = st.text_input("ทิศเหนือ (N)", "ติวานนท์")
    s_name = st.text_input("ทิศใต้ (S)", "ติวานนท์")
    e_name = st.text_input("ทิศตะวันออก (E)", "งามวงศ์วาน")
    w_name = st.text_input("ทิศตะวันตก (W)", "รัตนาธิเบศร์")

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

# --- Calculation: Fratar Method ---
seed = np.array([[0, 0.7, 0.15, 0.15], [0.7, 0, 0.15, 0.15], [0.15, 0.15, 0, 0.7], [0.15, 0.15, 0.7, 0]])
t_in = np.array([in_n, in_s, in_e, in_w])
t_out = np.array([out_n, out_s, out_e, out_w])
mat = seed.copy()
for _ in range(20):
    mat = (mat.T * (t_in / np.maximum(mat.sum(axis=1), 1))).T
    mat = mat * (t_out / np.maximum(mat.sum(axis=0), 1))

def gv(o, d): return int(round(mat[o, d]))

# Value Map (L=ซ้าย, T=ตรง, R=ขวา ของแต่ละทิศเมื่อมองเข้าหาแยก)
v = {
    'nl': gv(0, 2), 'nt': gv(0, 1), 'nr': gv(0, 3), # North
    'sl': gv(1, 3), 'st': gv(1, 0), 'sr': gv(1, 2), # South
    'el': gv(2, 1), 'et': gv(2, 3), 'er': gv(2, 0), # East
    'wl': gv(3, 0), 'wt': gv(3, 2), 'wr': gv(3, 1)  # West
}

# --- SVG Drawing ---
final_svg = f"""
<div style="display: flex; justify-content: center;">
<svg viewBox="0 0 800 700" xmlns="http://www.w3.org/2000/svg" style="width: 100%; max-width: 800px; background: #fdfdfd; border: 1px solid #ccc;">
    <defs>
        <marker id="arr" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto">
            <path d="M0,0 L7,3.5 L0,7 Z" fill="#333" />
        </marker>
    </defs>
    <text x="400" y="40" text-anchor="middle" font-size="22" font-weight="bold">{title_text}</text>

    <path d="M 330 50 V 250 M 470 50 V 250 M 330 450 V 650 M 470 450 V 650" stroke="black" stroke-width="2.5" fill="none"/>
    <path d="M 50 250 H 330 M 50 450 H 330 M 470 250 H 750 M 470 450 H 750" stroke="black" stroke-width="2.5" fill="none"/>
    <line x1="400" y1="50" x2="400" y2="250" stroke="#aaa" stroke-dasharray="5,5" />
    <line x1="400" y1="450" x2="400" y2="650" stroke="#aaa" stroke-dasharray="5,5" />
    <line x1="50" y1="350" x2="330" y2="350" stroke="#aaa" stroke-dasharray="5,5" />
    <line x1="470" y1="350" x2="750" y2="350" stroke="#aaa" stroke-dasharray="5,5" />

    <text x="415" y="140" transform="rotate(-90 415,140)" font-size="14" font-weight="bold" fill="blue">{n_name}</text>
    <text x="415" y="550" transform="rotate(-90 415,550)" font-size="14" font-weight="bold" fill="blue">{s_name}</text>
    <text x="610" y="340" font-size="14" font-weight="bold" fill="blue">{e_name}</text>
    <text x="130" y="340" font-size="14" font-weight="bold" fill="blue">{w_name}</text>

    <g transform="translate(405,210)">
        <rect width="20" height="15" fill="white" stroke="black"/><text x="10" y="11" text-anchor="middle" font-size="9">{v['nl']}</text>
        <path d="M 10 15 v 15 h 55" fill="none" stroke="red" stroke-width="1.5" marker-end="url(#arr)"/>
    </g>
    <g transform="translate(427,210)">
        <rect width="20" height="15" fill="white" stroke="black"/><text x="10" y="11" text-anchor="middle" font-size="9">{v['nt']}</text>
        <path d="M 10 15 v 45" fill="none" stroke="red" stroke-width="1.5" marker-end="url(#arr)"/>
    </g>
    <g transform="translate(450,210)">
        <rect width="20" height="15" fill="white" stroke="black"/><text x="10" y="11" text-anchor="middle" font-size="9">{v['nr']}</text>
        <path d="M 10 15 v 15 h -120" fill="none" stroke="red" stroke-width="1.5" marker-end="url(#arr)"/>
    </g>

    <g transform="translate(330,475)">
        <rect width="20" height="15" fill="white" stroke="black"/><text x="10" y="11" text-anchor="middle" font-size="9">{v['sr']}</text>
        <path d="M 10 0 v -15 h 120" fill="none" stroke="green" stroke-width="1.5" marker-end="url(#arr)"/>
    </g>
    <g transform="translate(353,475)">
        <rect width="20" height="15" fill="white" stroke="black"/><text x="10" y="11" text-anchor="middle" font-size="9">{v['st']}</text>
        <path d="M 10 0 v -45" fill="none" stroke="green" stroke-width="1.5" marker-end="url(#arr)"/>
    </g>
    <g transform="translate(375,475)">
        <rect width="20" height="15" fill="white" stroke="black"/><text x="10" y="11" text-anchor="middle" font-size="9">{v['sl']}</text>
        <path d="M 10 0 v -15 h -55" fill="none" stroke="green" stroke-width="1.5" marker-end="url(#arr)"/>
    </g>

    <g transform="translate(280,260)">
        <rect width="20" height="15" fill="white" stroke="black"/><text x="10" y="11" text-anchor="middle" font-size="9">{v['wl']}</text>
        <path d="M 20 7 h 20 v -45" fill="none" stroke="orange" stroke-width="1.5" marker-end="url(#arr)"/>
    </g>
    <g transform="translate(280,285)">
        <rect width="20" height="15" fill="white" stroke="black"/><text x="10" y="11" text-anchor="middle" font-size="9">{v['wt']}</text>
        <path d="M 20 7 h 50" fill="none" stroke="orange" stroke-width="1.5" marker-end="url(#arr)"/>
    </g>
    <g transform="translate(280,310)">
        <rect width="20" height="15" fill="white" stroke="black"/><text x="10" y="11" text-anchor="middle" font-size="9">{v['wr']}</text>
        <path d="M 20 7 h 20 v 120" fill="none" stroke="orange" stroke-width="1.5" marker-end="url(#arr)"/>
    </g>

    <g transform="translate(500,375)">
        <rect width="20" height="15" fill="white" stroke="black"/><text x="10" y="11" text-anchor="middle" font-size="9">{v['el']}</text>
        <path d="M 0 7 h -20 v 45" fill="none" stroke="purple" stroke-width="1.5" marker-end="url(#arr)"/>
    </g>
    <g transform="translate(500,400)">
        <rect width="20" height="15" fill="white" stroke="black"/><text x="10" y="11" text-anchor="middle" font-size="9">{v['et']}</text>
        <path d="M 0 7 h -50" fill="none" stroke="purple" stroke-width="1.5" marker-end="url(#arr)"/>
    </g>
    <g transform="translate(500,425)">
        <rect width="20" height="15" fill="white" stroke="black"/><text x="10" y="11" text-anchor="middle" font-size="9">{v['er']}</text>
        <path d="M 0 7 h -20 v -120" fill="none" stroke="purple" stroke-width="1.5" marker-end="url(#arr)"/>
    </g>
</svg>
</div>
"""

st.components.v1.html(final_svg, height=700)
