import streamlit as st
import numpy as np

st.set_page_config(layout="wide", page_title="Traffic Turning Estimator")

# --- Sidebar: ตั้งค่าชื่อถนน ---
with st.sidebar:
    st.header("📍 ตั้งค่าชื่อถนน")
    title_text = st.text_input("หัวข้อแผนภูมิ", "Traffic Movement Estimation")
    rd_n = st.text_input("ถนนทิศเหนือ", "ติวานนท์")
    rd_s = st.text_input("ถนนทิศใต้", "ติวานนท์")
    rd_e = st.text_input("ถนนทิศตะวันออก", "งามวงศ์วาน")
    rd_w = st.text_input("ถนนทิศตะวันตก", "รัตนาธิเบศร์")

# --- ส่วนกรอกข้อมูลหลัก (Input Inbound & Outbound) ---
st.subheader("📊 ป้อนปริมาณรถ ขาเข้า และ ขาออก รวมของแต่ละทิศ")
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"**ทิศเหนือ ({rd_n})**")
    in_n = st.number_input("In (รวมเข้า)", value=3577, key="in_n")
    out_n = st.number_input("Out (รวมออก)", value=1632, key="out_n")
with c2:
    st.markdown(f"**ทิศใต้ ({rd_s})**")
    in_s = st.number_input("In (รวมเข้า)", value=2234, key="in_s")
    out_s = st.number_input("Out (รวมออก)", value=2458, key="out_s")
with c3:
    st.markdown(f"**ทิศตะวันออก ({rd_e})**")
    in_e = st.number_input("In (รวมเข้า)", value=3628, key="in_e")
    out_e = st.number_input("Out (รวมออก)", value=7989, key="out_e")
with c4:
    st.markdown(f"**ทิศตะวันตก ({rd_w})**")
    in_w = st.number_input("In (รวมเข้า)", value=4488, key="in_w")
    out_w = st.number_input("Out (รวมออก)", value=1847, key="out_w")

# --- Algorithm: Iterative Balancing (ประมาณค่าการเลี้ยว) ---
seed = np.array([
    [0.0, 0.7, 0.15, 0.15], # จาก N ไป N, S, E, W
    [0.7, 0.0, 0.15, 0.15], # จาก S ไป N, S, E, W
    [0.15, 0.15, 0.0, 0.7], # จาก E ไป N, S, E, W
    [0.15, 0.15, 0.7, 0.0]  # จาก W ไป N, S, E, W
])
targets_in = np.array([in_n, in_s, in_e, in_w])
targets_out = np.array([out_n, out_s, out_e, out_w])
matrix = seed.copy()
for _ in range(15):
    matrix = (matrix.T * (targets_in / np.maximum(matrix.sum(axis=1), 1))).T
    matrix = matrix * (targets_out / np.maximum(matrix.sum(axis=0), 1))

def gv(o, d): return int(round(matrix[o, d]))

# คำนวณการเลี้ยวรายทิศ
n_l, n_t, n_r = gv(0, 2), gv(0, 1), gv(0, 3)
s_l, s_t, s_r = gv(1, 3), gv(1, 0), gv(1, 2)
e_l, e_t, e_r = gv(2, 1), gv(2, 3), gv(2, 0)
w_l, w_t, w_r = gv(3, 0), gv(3, 2), gv(3, 1)

# --- SVG Drawing: แบ่งเส้นขาเข้า-ขาออกชัดเจน ---
svg_draw = f"""
<div style="display: flex; justify-content: center;">
<svg viewBox="0 0 700 600" xmlns="http://www.w3.org/2000/svg" style="width: 100%; max-width: 700px; background: white; border: 1px solid #ccc;">
    <rect width="100%" height="100%" fill="#ffffff" />
    <text x="350" y="30" text-anchor="middle" font-size="18" font-weight="bold">{title_text}</text>

    <path d="M 300 40 V 230 M 350 40 V 230 M 400 40 V 230" stroke="#999" fill="none" stroke-width="1" stroke-dasharray="4"/>
    <path d="M 300 40 V 230 M 400 40 V 230" stroke="black" fill="none" stroke-width="2"/>
    <path d="M 300 370 V 560 M 350 370 V 560 M 400 370 V 560" stroke="#999" fill="none" stroke-width="1" stroke-dasharray="4"/>
    <path d="M 300 370 V 560 M 400 370 V 560" stroke="black" fill="none" stroke-width="2"/>
    
    <path d="M 40 230 H 300 M 40 300 H 300 M 40 370 H 300" stroke="#999" fill="none" stroke-width="1" stroke-dasharray="4"/>
    <path d="M 40 230 H 300 M 40 370 H 300" stroke="black" fill="none" stroke-width="2"/>
    <path d="M 400 230 H 660 M 400 300 H 660 M 400 370 H 660" stroke="#999" fill="none" stroke-width="1" stroke-dasharray="4"/>
    <path d="M 400 230 H 660 M 400 370 H 660" stroke="black" fill="none" stroke-width="2"/>

    <rect x="305" y="50" width="40" height="20" fill="white" stroke="black"/><text x="325" y="64" text-anchor="middle" font-size="9">Out:{out_n}</text>
    <rect x="355" y="50" width="40" height="20" fill="white" stroke="black"/><text x="375" y="64" text-anchor="middle" font-size="9">In:{in_n}</text>
    
    <rect x="305" y="520" width="40" height="20" fill="white" stroke="black"/><text x="325" y="534" text-anchor="middle" font-size="9">In:{in_s}</text>
    <rect x="355" y="520" width="40" height="20" fill="white" stroke="black"/><text x="375" y="534" text-anchor="middle" font-size="9">Out:{out_s}</text>

    <rect x="50" y="240" width="45" height="20" fill="white" stroke="black"/><text x="72.5" y="254" text-anchor="middle" font-size="9">In:{in_w}</text>
    <rect x="50" y="340" width="45" height="20" fill="white" stroke="black"/><text x="72.5" y="354" text-anchor="middle" font-size="9">Out:{out_w}</text>

    <rect x="600" y="240" width="45" height="20" fill="white" stroke="black"/><text x="622.5" y="254" text-anchor="middle" font-size="9">In:{in_e}</text>
    <rect x="600" y="340" width="45" height="20" fill="white" stroke="black"/><text x="622.5" y="354" text-anchor="middle" font-size="9">Out:{out_e}</text>

    <rect x="345" y="200" width="18" height="15" fill="white" stroke="black"/><text x="354" y="211" text-anchor="middle" font-size="8">{n_l}</text>
    <rect x="365" y="200" width="22" height="15" fill="white" stroke="black"/><text x="376" y="211" text-anchor="middle" font-size="8">{n_t}</text>
    <rect x="388" y="200" width="18" height="15" fill="white" stroke="black"/><text x="397" y="211" text-anchor="middle" font-size="8">{n_r}</text>
    <text x="350" y="228" font-size="14">↧</text><text x="370" y="228" font-size="14">↓</text><text x="390" y="228" font-size="14">↴</text>

    <rect x="302" y="380" width="18" height="15" fill="white" stroke="black"/><text x="311" y="391" text-anchor="middle" font-size="8">{s_r}</text>
    <rect x="322" y="380" width="22" height="15" fill="white" stroke="black"/><text x="333" y="391" text-anchor="middle" font-size="8">{s_t}</text>
    <rect x="346" y="380" width="18" height="15" fill="white" stroke="black"/><text x="355" y="391" text-anchor="middle" font-size="8">{s_l}</text>
    <text x="305" y="380" font-size="14">↰</text><text x="325" y="380" font-size="14">↑</text><text x="348" y="380" font-size="14">⤴</text>

    <rect x="275" y="235" width="22" height="15" fill="white" stroke="black"/><text x="286" y="246" text-anchor="middle" font-size="8">{w_r}</text>
    <rect x="275" y="255" width="22" height="15" fill="white" stroke="black"/><text x="286" y="266" text-anchor="middle" font-size="8">{w_t}</text>
    <rect x="275" y="275" width="22" height="15" fill="white" stroke="black"/><text x="286" y="286" text-anchor="middle" font-size="8">{w_l}</text>
    <text x="302" y="248" font-size="14">↱</text><text x="302" y="268" font-size="14">→</text><text x="302" y="288" font-size="14">↳</text>

    <rect x="405" y="310" width="22" height="15" fill="white" stroke="black"/><text x="416" y="321" text-anchor="middle" font-size="8">{e_l}</text>
    <rect x="405" y="330" width="22" height="15" fill="white" stroke="black"/><text x="416" y="341" text-anchor="middle" font-size="8">{e_t}</text>
    <rect x="405" y="350" width="22" height="15" fill="white" stroke="black"/><text x="416" y="361" text-anchor="middle" font-size="8">{e_r}</text>
    <text x="385" y="323" font-size="14">↤</text><text x="385" y="343" font-size="14">←</text><text x="385" y="363" font-size="14">↲</text>

    <text x="350" y="140" transform="rotate(-90 350,140)" font-size="12" fill="blue" font-weight="bold">{rd_n}</text>
    <text x="520" y="335" font-size="12" fill="blue" font-weight="bold">{rd_e}</text>

    <text x="630" y="60" font-size="25">🧭</text><text x="635" y="85" font-size="12" font-weight="bold">N</text>
</svg>
</div>
"""

st.components.v1.html(svg_draw, height=620)
