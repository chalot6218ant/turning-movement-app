import streamlit as st
import numpy as np

st.set_page_config(layout="wide", page_title="Traffic Turning Estimator")

# --- Sidebar: ชื่อถนนที่แก้ไขได้ ---
with st.sidebar:
    st.header("📍 Edit Road Names")
    title_text = st.text_input("หัวข้อแผนภูมิ", "Traffic Movement Diagram")
    n_name = st.text_input("ทิศเหนือ (North)", "ติวานนท์")
    s_name = st.text_input("ทิศใต้ (South)", "ติวานนท์")
    e_name = st.text_input("ทิศตะวันออก (East)", "งามวงศ์วาน")
    w_name = st.text_input("ทิศตะวันตก (West)", "รัตนาธิเบศร์")

# --- ส่วนกรอกข้อมูลหลัก ---
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

# --- Algorithm: Fratar Method (Balancing) ---
seed = np.array([[0, 0.7, 0.15, 0.15], [0.7, 0, 0.15, 0.15], [0.15, 0.15, 0, 0.7], [0.15, 0.15, 0.7, 0]])
targets_in = np.array([in_n, in_s, in_e, in_w])
targets_out = np.array([out_n, out_s, out_e, out_w])
matrix = seed.copy()
for _ in range(15):
    matrix = (matrix.T * (targets_in / np.maximum(matrix.sum(axis=1), 1))).T
    matrix = matrix * (targets_out / np.maximum(matrix.sum(axis=0), 1))

def gv(o, d): return int(round(matrix[o, d]))

# คำนวณ Turning (L/T/R)
n_l, n_t, n_r = gv(0, 2), gv(0, 1), gv(0, 3) # N ไป E(L), S(T), W(R)
s_l, s_t, s_r = gv(1, 3), gv(1, 0), gv(1, 2) # S ไป W(L), N(T), E(R)
e_l, e_t, e_r = gv(2, 1), gv(2, 3), gv(2, 0) # E ไป S(L), W(T), N(R)
w_l, w_t, w_r = gv(3, 0), gv(3, 2), gv(3, 1) # W ไป N(L), E(T), S(R)

# --- SVG Drawing ---
svg = f"""
<div style="display: flex; justify-content: center;">
<svg viewBox="0 0 800 650" xmlns="http://www.w3.org/2000/svg" style="width: 100%; max-width: 800px; background: white; border: 1px solid #ccc;">
    <rect width="100%" height="100%" fill="white" />
    <text x="400" y="40" text-anchor="middle" font-size="20" font-weight="bold">{title_text}</text>

    <path d="M 330 50 V 250 M 470 50 V 250 M 330 400 V 600 M 470 400 V 600" stroke="black" stroke-width="2" fill="none"/>
    <line x1="400" y1="50" x2="400" y2="250" stroke="#ccc" stroke-dasharray="5,5" />
    <line x1="400" y1="400" x2="400" y2="600" stroke="#ccc" stroke-dasharray="5,5" />

    <path d="M 50 250 H 330 M 50 400 H 330 M 470 250 H 750 M 470 400 H 750" stroke="black" stroke-width="2" fill="none"/>
    <line x1="50" y1="325" x2="330" y2="325" stroke="#ccc" stroke-dasharray="5,5" />
    <line x1="470" y1="325" x2="750" y2="325" stroke="#ccc" stroke-dasharray="5,5" />

    <text x="410" y="150" transform="rotate(-90 410,150)" font-size="14" font-weight="bold" fill="blue">{n_name}</text>
    <text x="410" y="500" transform="rotate(-90 410,500)" font-size="14" font-weight="bold" fill="blue">{s_name}</text>
    <text x="610" y="315" font-size="14" font-weight="bold" fill="blue">{e_name}</text>
    <text x="130" y="315" font-size="14" font-weight="bold" fill="blue">{w_name}</text>

    <g transform="translate(345, 60)"><rect width="50" height="25" fill="white" stroke="black"/><text x="25" y="17" text-anchor="middle" font-size="10">Out:{out_n}</text></g>
    <g transform="translate(405, 60)"><rect width="50" height="25" fill="white" stroke="black"/><text x="25" y="17" text-anchor="middle" font-size="10">In:{in_n}</text></g>
    
    <g transform="translate(345, 565)"><rect width="50" height="25" fill="white" stroke="black"/><text x="25" y="17" text-anchor="middle" font-size="10">In:{in_s}</text></g>
    <g transform="translate(405, 565)"><rect width="50" height="25" fill="white" stroke="black"/><text x="25" y="17" text-anchor="middle" font-size="10">Out:{out_s}</text></g>

    <g transform="translate(60, 260)"><rect width="55" height="25" fill="white" stroke="black"/><text x="27.5" y="17" text-anchor="middle" font-size="10">In:{in_w}</text></g>
    <g transform="translate(60, 365)"><rect width="55" height="25" fill="white" stroke="black"/><text x="27.5" y="17" text-anchor="middle" font-size="10">Out:{out_w}</text></g>

    <g transform="translate(685, 260)"><rect width="55" height="25" fill="white" stroke="black"/><text x="27.5" y="17" text-anchor="middle" font-size="10">In:{in_e}</text></g>
    <g transform="translate(685, 365)"><rect width="55" height="25" fill="white" stroke="black"/><text x="27.5" y="17" text-anchor="middle" font-size="10">Out:{out_e}</text></g>

    <rect x="405" y="215" width="20" height="18" fill="white" stroke="black"/><text x="415" y="228" text-anchor="middle" font-size="9">{n_l}</text><text x="410" y="245" font-size="18">↧</text>
    <rect x="428" y="215" width="25" height="18" fill="white" stroke="black"/><text x="440.5" y="228" text-anchor="middle" font-size="9">{n_t}</text><text x="435" y="245" font-size="18">↓</text>
    <rect x="456" y="215" width="20" height="18" fill="white" stroke="black"/><text x="466" y="228" text-anchor="middle" font-size="9">{n_r}</text><text x="461" y="245" font-size="18">↴</text>

    <rect x="325" y="415" width="20" height="18" fill="white" stroke="black"/><text x="335" y="428" text-anchor="middle" font-size="9">{s_r}</text><text x="330" y="415" font-size="18">↰</text>
    <rect x="348" y="415" width="25" height="18" fill="white" stroke="black"/><text x="360.5" y="428" text-anchor="middle" font-size="9">{s_t}</text><text x="355" y="415" font-size="18">↑</text>
    <rect x="376" y="415" width="20" height="18" fill="white" stroke="black"/><text x="386" y="428" text-anchor="middle" font-size="9">{s_l}</text><text x="381" y="415" font-size="18">⤴</text>

    <rect x="305" y="255" width="22" height="18" fill="white" stroke="black"/><text x="316" y="268" text-anchor="middle" font-size="9">{w_r}</text><text x="332" y="270" font-size="18">↱</text>
    <rect x="305" y="278" width="22" height="18" fill="white" stroke="black"/><text x="316" y="291" text-anchor="middle" font-size="9">{w_t}</text><text x="332" y="293" font-size="18">→</text>
    <rect x="305" y="301" width="22" height="18" fill="white" stroke="black"/><text x="316" y="314" text-anchor="middle" font-size="9">{w_l}</text><text x="332" y="316" font-size="18">↳</text>

    <rect x="473" y="332" width="22" height="18" fill="white" stroke="black"/><text x="484" y="345" text-anchor="middle" font-size="9">{e_l}</text><text x="455" y="347" font-size="18">↤</text>
    <rect x="473" y="355" width="22" height="18" fill="white" stroke="black"/><text x="484" y="368" text-anchor="middle" font-size="9">{e_t}</text><text x="455" y="370" font-size="18">←</text>
    <rect x="473" y="378" width="22" height="18" fill="white" stroke="black"/><text x="484" y="391" text-anchor="middle" font-size="9">{e_r}</text><text x="455" y="393" font-size="18">↲</text>

    <g transform="translate(720, 80)"><circle r="25" fill="none" stroke="black"/><path d="M 0 -20 L 5 0 L -5 0 Z" fill="red"/><text y="15" text-anchor="middle" font-weight="bold">N</text></g>
</svg>
</div>
"""

st.components.v1.html(svg, height=650)
