import streamlit as st
import numpy as np

st.set_page_config(layout="wide", page_title="Traffic Turning Estimator")

# --- Sidebar: ชื่อถนน ---
with st.sidebar:
    st.header("⚙️ Settings")
    title_text = st.text_input("Chart Title", "Year 2006 AM")
    n_name = st.text_input("North Road", "ติวานนท์")
    s_name = st.text_input("South Road", "ติวานนท์")
    e_name = st.text_input("East Road", "งามวงศ์วาน")
    w_name = st.text_input("West Road", "รัตนาธิเบศร์")

# --- Input: Inbound / Outbound ---
st.subheader("📊 ป้อนปริมาณรถ ขาเข้า และ ขาออก")
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

# --- Calculation: Fratar Balancing (ประมาณค่าการเลี้ยว) ---
seed = np.array([[0, 0.7, 0.15, 0.15], [0.7, 0, 0.15, 0.15], [0.15, 0.15, 0, 0.7], [0.15, 0.15, 0.7, 0]])
t_in = np.array([in_n, in_s, in_e, in_w])
t_out = np.array([out_n, out_s, out_e, out_w])
mat = seed.copy()
for _ in range(20):
    mat = (mat.T * (t_in / np.maximum(mat.sum(axis=1), 1))).T
    mat = mat * (t_out / np.maximum(mat.sum(axis=0), 1))

def gv(o, d): return int(round(mat[o, d]))

# Mapping: L/T/R ของแต่ละทิศ
vals = {
    'nl': gv(0, 2), 'nt': gv(0, 1), 'nr': gv(0, 3), # North
    'sl': gv(1, 3), 'st': gv(1, 0), 'sr': gv(1, 2), # South
    'el': gv(2, 1), 'et': gv(2, 3), 'er': gv(2, 0), # East
    'wl': gv(3, 0), 'wt': gv(3, 2), 'wr': gv(3, 1)  # West
}

# --- SVG Drawing ---
svg_code = f"""
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

    <text x="420" y="150" transform="rotate(-90 420,150)" font-size="14" font-weight="bold" fill="blue">{n_name}</text>
    <text x="420" y="500" transform="rotate(-90 420,500)" font-size="14" font-weight="bold" fill="blue">{s_name}</text>
    <text x="610" y="315" font-size="14" font-weight="bold" fill="blue">{e_name}</text>
    <text x="130" y="315" font-size="14" font-weight="bold" fill="blue">{w_name}</text>

    <rect x="340" y="60" width="55" height="25" fill="#f8d7da" stroke="black"/><text x="367.5" y="77" text-anchor="middle" font-size="11">Out:{out_n}</text>
    <rect x="405" y="60" width="55" height="25" fill="#d4edda" stroke="black"/><text x="432.5" y="77" text-anchor="middle" font-size="11">In:{in_n}</text>
    <rect x="340" y="565" width="55" height="25" fill="#d4edda" stroke="black"/><text x="367.5" y="582" text-anchor="middle" font-size="11">In:{in_s}</text>
    <rect x="405" y="565" width="55" height="25" fill="#f8d7da" stroke="black"/><text x="432.5" y="582" text-anchor="middle" font-size="11">Out:{out_s}</text>

    <defs>
        <marker id="ar" markerWidth="10" markerHeight="10" refX="5" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="red"/></marker>
    </defs>

    <g transform="translate(410,210)">
        <rect width="25" height="18" fill="white" stroke="black"/><text x="12.5" y="13" text-anchor="middle" font-size="9">{vals['nl']}</text>
        <path d="M 12 18 v 15 h 25" fill="none" stroke="red" stroke-width="2" marker-end="url(#ar)"/>
    </g>
    <g transform="translate(440,210)">
        <rect width="25" height="18" fill="white" stroke="black"/><text x="12.5" y="13" text-anchor="middle" font-size="9">{vals['nt']}</text>
        <path d="M 12 18 v 25" fill="none" stroke="red" stroke-width="2" marker-end="url(#ar)"/>
    </g>
    <g transform="translate(470,210)">
        <rect width="25" height="18" fill="white" stroke="black"/><text x="12.5" y="13" text-anchor="middle" font-size="9">{vals['nr']}</text>
        <path d="M 12 18 v 15 h -40" fill="none" stroke="red" stroke-width="2" marker-end="url(#ar)"/>
    </g>

    <g transform="translate(305,420)">
        <rect width="25" height="18" fill="white" stroke="black"/><text x="12.5" y="13" text-anchor="middle" font-size="9">{vals['sr']}</text>
        <path d="M 12 0 v -15 h 40" fill="none" stroke="green" stroke-width="2" marker-end="url(#ar)"/>
    </g>
    <g transform="translate(335,420)">
        <rect width="25" height="18" fill="white" stroke="black"/><text x="12.5" y="13" text-anchor="middle" font-size="9">{vals['st']}</text>
        <path d="M 12 0 v -25" fill="none" stroke="green" stroke-width="2" marker-end="url(#ar)"/>
    </g>
    <g transform="translate(365,420)">
        <rect width="25" height="18" fill="white" stroke="black"/><text x="12.5" y="13" text-anchor="middle" font-size="9">{vals['sl']}</text>
        <path d="M 12 0 v -15 h -25" fill="none" stroke="green" stroke-width="2" marker-end="url(#ar)"/>
    </g>

    <text x="700" y="80" font-size="30">🧭</text><text x="705" y="110" font-weight="bold">N</text>
</svg>
</div>
"""

st.components.v1.html(svg_code, height=650)
