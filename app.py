import streamlit as st
import numpy as np

st.set_page_config(layout="wide", page_title="Traffic turning Movement Analysis")

# --- Sidebar: สำหรับแก้ไขชื่อถนน ---
with st.sidebar:
    st.header("📝 Edit Road Names")
    title_text = st.text_input("Chart Title", "Traffic Movement Estimation 2026")
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
seed = np.array([[0, 0.7, 0.15, 0.15], [0.7, 0, 0.15, 0.15], [0.15, 0.15, 0, 0.7], [0.15, 0.15, 0.7, 0]])
mat = seed.copy()
for _ in range(20):
    mat = (mat.T * (t_in / np.maximum(mat.sum(axis=1), 1))).T
    mat = mat * (t_out / np.maximum(mat.sum(axis=0), 1))

def gv(o, d): return int(round(mat[o, d]))

# คำนวณยอดรวม
sum_in = int(t_in.sum())
sum_out = int(t_out.sum())
grand_total = sum_in + sum_out

# Mapping Turning values
v = {
    'nl': gv(0, 2), 'nt': gv(0, 1), 'nr': gv(0, 3),
    'sl': gv(1, 3), 'st': gv(1, 0), 'sr': gv(1, 2),
    'el': gv(2, 1), 'et': gv(2, 3), 'er': gv(2, 0),
    'wl': gv(3, 0), 'wt': gv(3, 2), 'wr': gv(3, 1)
}

# --- SVG Design ---
final_svg = f"""
<div style="display: flex; justify-content: center;">
<svg viewBox="0 0 800 650" xmlns="http://www.w3.org/2000/svg" style="width: 100%; max-width: 800px; background: #ffffff; border: 1px solid #333;">
    <rect width="800" height="60" fill="#f4f4f4" />
    <text x="400" y="38" text-anchor="middle" font-size="22" font-weight="bold" fill="#333">{title_text}</text>
    
    <path d="M 320 60 V 220 M 480 60 V 220 M 320 400 V 580 M 480 400 V 580" stroke="#000" stroke-width="2.5" fill="none"/>
    <path d="M 50 220 H 320 M 50 400 H 320 M 480 220 H 750 M 480 400 H 750" stroke="#000" stroke-width="2.5" fill="none"/>
    <line x1="400" y1="60" x2="400" y2="220" stroke="#aaa" stroke-dasharray="5,5" />
    <line x1="400" y1="400" x2="400" y2="580" stroke="#aaa" stroke-dasharray="5,5" />
    <line x1="50" y1="310" x2="320" y2="310" stroke="#aaa" stroke-dasharray="5,5" />
    <line x1="480" y1="310" x2="750" y2="310" stroke="#aaa" stroke-dasharray="5,5" />

    <text x="415" y="140" transform="rotate(-90 415,140)" font-size="14" font-weight="bold" fill="blue">{n_road}</text>
    <text x="415" y="500" transform="rotate(-90 415,500)" font-size="14" font-weight="bold" fill="blue">{s_road}</text>
    <text x="620" y="300" font-size="14" font-weight="bold" fill="blue">{e_road}</text>
    <text x="120" y="300" font-size="14" font-weight="bold" fill="blue">{w_road}</text>

    <g font-size="11" font-weight="bold">
        <rect x="330" y="70" width="60" height="25" fill="#ffdada" stroke="#000"/><text x="360" y="87" text-anchor="middle">Out:{out_n}</text>
        <rect x="410" y="70" width="60" height="25" fill="#daffda" stroke="#000"/><text x="440" y="87" text-anchor="middle">In:{in_n}</text>
        <rect x="330" y="540" width="60" height="25" fill="#daffda" stroke="#000"/><text x="360" y="557" text-anchor="middle">In:{in_s}</text>
        <rect x="410" y="540" width="60" height="25" fill="#ffdada" stroke="#000"/><text x="440" y="557" text-anchor="middle">Out:{out_s}</text>
        <rect x="60" y="230" width="65" height="25" fill="#daffda" stroke="#000"/><text x="92.5" y="247" text-anchor="middle">In:{in_w}</text>
        <rect x="60" y="365" width="65" height="25" fill="#ffdada" stroke="#000"/><text x="92.5" y="382" text-anchor="middle">Out:{out_w}</text>
        <rect x="675" y="230" width="65" height="25" fill="#daffda" stroke="#000"/><text x="707.5" y="247" text-anchor="middle">In:{in_e}</text>
        <rect x="675" y="365" width="65" height="25" fill="#ffdada" stroke="#000"/><text x="707.5" y="382" text-anchor="middle">Out:{out_e}</text>
    </g>

    <g font-size="12" font-weight="bold" fill="#333">
        <text x="408" y="210">↰ {v['nl']}</text>
        <text x="435" y="210">↓ {v['nt']}</text>
        <text x="462" y="210">↱ {v['nr']}</text>
    </g>
    <g font-size="12" font-weight="bold" fill="#333">
        <text x="325" y="390">↰ {v['sr']}</text>
        <text x="352" y="390">↑ {v['st']}</text>
        <text x="378" y="390">↱ {v['sl']}</text>
    </g>
    <g font-size="12" font-weight="bold" fill="#333">
        <text x="260" y="245">↱ {v['wr']}</text>
        <text x="260" y="305">→ {v['wt']}</text>
        <text x="260" y="355">↳ {v['wl']}</text>
    </g>
    <g font-size="12" font-weight="bold" fill="#333" text-anchor="end">
        <text x="540" y="265">{v['er']} ↰</text>
        <text x="540" y="315">{v['et']} ←</text>
        <text x="540" y="375">{v['el']} ↲</text>
    </g>
