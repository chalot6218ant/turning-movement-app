import streamlit as st
import numpy as np

st.set_page_config(layout="wide", page_title="Traffic Movement Analysis")

# --- Sidebar: สำหรับแก้ไขชื่อถนน ---
with st.sidebar:
    st.header("📝 Edit Road Names")
    title_text = st.text_input("Chart Title", "Year 2006 AM")
    n_road = st.text_input("North Road", "ติวานนท์ (N)")
    s_road = st.text_input("South Road", "ติวานนท์ (S)")
    e_road = st.text_input("East Road", "งามวงศ์วาน")
    w_road = st.text_input("West Road", "รัตนาธิเบศร์")

# --- ส่วนรับข้อมูล Inbound/Outbound ---
st.subheader("🚗 Input Traffic Volume (PCU/Hr)")
col1, col2, col3, col4 = st.columns(4)
with col1:
    in_n = st.number_input(f"Inbound {n_road}", value=3577)
    out_n = st.number_input(f"Outbound {n_road}", value=1632)
with col2:
    in_s = st.number_input(f"Inbound {s_road}", value=2234)
    out_s = st.number_input(f"Outbound {s_road}", value=2458)
with col3:
    in_e = st.number_input(f"Inbound {e_road}", value=3628)
    out_e = st.number_input(f"Outbound {e_road}", value=7989)
with col4:
    in_w = st.number_input(f"Inbound {w_road}", value=4488)
    out_w = st.number_input(f"Outbound {w_road}", value=1847)

# --- Calculation: Fratar Balancing ---
t_in = np.array([in_n, in_s, in_e, in_w])
t_out = np.array([out_n, out_s, out_e, out_w])
# Seed matrix: Rows N,S,E,W | Cols N,S,E,W
seed = np.array([[0, 0.7, 0.15, 0.15], [0.7, 0, 0.15, 0.15], [0.15, 0.15, 0, 0.7], [0.15, 0.15, 0.7, 0]])
mat = seed.copy()
for _ in range(20):
    mat = (mat.T * (t_in / np.maximum(mat.sum(axis=1), 1))).T
    mat = mat * (t_out / np.maximum(mat.sum(axis=0), 1))

def gv(o, d): return int(round(mat[o, d]))
sum_in = int(t_in.sum())
sum_out = int(t_out.sum())

# Mapping Turning values
v = {
    'nl': gv(0, 2), 'nt': gv(0, 1), 'nr': gv(0, 3), # North
    'sl': gv(1, 3), 'st': gv(1, 0), 'sr': gv(1, 2), # South
    'el': gv(2, 1), 'et': gv(2, 3), 'er': gv(2, 0), # East
    'wl': gv(3, 0), 'wt': gv(3, 2), 'wr': gv(3, 1)  # West
}

# --- SVG Design with Double Box style ---
final_svg = f"""
<div style="display: flex; justify-content: center;">
<svg viewBox="0 0 800 650" xmlns="http://www.w3.org/2000/svg" style="width: 100%; max-width: 800px; background:white; border:1px solid #ccc;">
    <rect width="800" height="60" fill="#f4f4f4" />
    <text x="400" y="38" text-anchor="middle" font-size="22" font-weight="bold" fill="#333">{title_text}</text>
    
    <path d="M 330 60 V 230 M 470 60 V 230 M 330 400 V 580 M 470 400 V 580" stroke="#000" stroke-width="2.5" fill="none"/>
    <path d="M 50 230 H 330 M 50 400 H 330 M 470 230 H 750 M 470 400 H 750" stroke="#000" stroke-width="2.5" fill="none"/>
    <line x1="400" y1="60" x2="400" y2="230" stroke="#aaa" stroke-dasharray="5,5" />
    <line x1="400" y1="400" x2="400" y2="580" stroke="#aaa" stroke-dasharray="5,5" />
    <line x1="50" y1="315" x2="330" y2="315" stroke="#aaa" stroke-dasharray="5,5" />
    <line x1="470" y1="315" x2="750" y2="315" stroke="#aaa" stroke-dasharray="5,5" />

    <text x="415" y="140" transform="rotate(-90 415,140)" font-size="14" font-weight="bold" fill="blue">{n_road}</text>
    <text x="415" y="500" transform="rotate(-90 415,500)" font-size="14" font-weight="bold" fill="blue">{s_road}</text>
    <text x="610" y="305" font-size="14" font-weight="bold" fill="blue">{e_road}</text>
    <text x="130" y="305" font-size="14" font-weight="bold" fill="blue">{w_road}</text>

    <rect x="330" y="70" width="60" height="25" fill="white" stroke="black"/><text x="360" y="87" text-anchor="middle" font-size="11">Out:{out_n}</text>
    <rect x="410" y="70" width="60" height="25" fill="white" stroke="black"/><text x="440" y="87" text-anchor="middle" font-size="11">In:{in_n}</text>
    <rect x="330" y="545" width="60" height="25" fill="white" stroke="black"/><text x="360" y="562" text-anchor="middle" font-size="11">In:{in_s}</text>
    <rect x="410" y="545" width="60" height="25" fill="white" stroke="black"/><text x="440" y="562" text-anchor="middle" font-size="11">Out:{out_s}</text>
    <rect x="60" y="240" width="65" height="25" fill="white" stroke="black"/><text x="92.5" y="257" text-anchor="middle" font-size="11">In:{in_w}</text>
    <rect x="60" y="365" width="65" height="25" fill="white" stroke="black"/><text x="92.5" y="382" text-anchor="middle" font-size="11">Out:{out_w}</text>
    <rect x="675" y="240" width="65" height="25" fill="white" stroke="black"/><text x="707.5" y="257" text-anchor="middle" font-size="11">In:{in_e}</text>
    <rect x="675" y="365" width="65" height="25" fill="white" stroke="black"/><text x="707.5" y="382" text-anchor="middle" font-size="11">Out:{out_e}</text>

    <g font-size="13" font-weight="bold" fill="#333">
        <text x="412" y="195">↰</text><text x="412" y="220" font-size="11">{v['nl']}</text>
        <text x="438" y="195">↓</text><text x="438" y="220" font-size="11">{v['nt']}</text>
        <text x="465" y="195">↱</text><text x="465" y="220" font-size="11">{v['nr']}</text>
    </g>

    <g font-size="13" font-weight="bold" fill="#333">
        <text x="330" y="420">↰</text><text x="330" y="445" font-size="11">{v['sr']}</text>
        <text x="355" y="420">↑</text><text x="355" y="445" font-size="11">{v['st']}</text>
        <text x="382" y="420">↱</text><text x="382" y="445" font-size="11">{v['sl']}</text>
    </g>

    <rect x="580" y="480" width="180" height="90" fill="#f9f9f9" stroke="#333" rx="5"/>
    <text x="670" y="500" text-anchor="middle" font-size="14" font-weight="bold">Summary (PCU/Hr)</text>
    <text x="595" y="525" font-size="12" fill="green">Total In: {sum_in:,}</text>
    <text x="595" y="545" font-size="12" fill="red">Total Out: {sum_out:,}</text>
    <text x="595" y="562" font-size="13" font-weight="bold">Grand Total: {sum_in + sum_out:,}</text>

    <g transform="translate(740, 95)"><circle r="18" fill="none" stroke="#666"/><path d="M 0 -14 L 3 0 L -3 0 Z" fill="red"/><text y="15" text-anchor="middle" font-size="9" font-weight="bold">N</text></g>
</svg>
</div>
"""

st.components.v1.html(final_svg, height=650)
