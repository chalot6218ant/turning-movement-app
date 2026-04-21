import streamlit as st
import numpy as np

st.set_page_config(layout="wide", page_title="Traffic Turning Estimator")

# --- Sidebar: ตั้งค่าชื่อถนน ---
with st.sidebar:
    st.header("📍 ตั้งค่าชื่อถนน")
    title_text = st.text_input("หัวข้อแผนภูมิ", "Traffic Estimation (Fratar Method)")
    rd_names = {
        "N": st.text_input("ถนนทิศเหนือ", "ติวานนท์"),
        "S": st.text_input("ถนนทิศใต้", "ติวานนท์"),
        "E": st.text_input("ถนนทิศตะวันออก", "งามวงศ์วาน"),
        "W": st.text_input("ถนนทิศตะวันตก", "รัตนาธิเบศร์")
    }

# --- ส่วนกรอกข้อมูลหลัก (Input Inbound & Outbound) ---
st.subheader("📊 ป้อนปริมาณรถ ขาเข้า และ ขาออก (PCU/Hr.)")
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.info(f"ทิศเหนือ ({rd_names['N']})")
    in_n = st.number_input("Inbound (เข้าแยก)", value=3577, key="in_n")
    out_n = st.number_input("Outbound (ออกจากแยก)", value=1632, key="out_n")
with c2:
    st.info(f"ทิศใต้ ({rd_names['S']})")
    in_s = st.number_input("Inbound (เข้าแยก)", value=2234, key="in_s")
    out_s = st.number_input("Outbound (ออกจากแยก)", value=2458, key="out_s")
with c3:
    st.info(f"ทิศตะวันออก ({rd_names['E']})")
    in_e = st.number_input("Inbound (เข้าแยก)", value=3628, key="in_e")
    out_e = st.number_input("Outbound (ออกจากแยก)", value=7989, key="out_e")
with c4:
    st.info(f"ทิศตะวันตก ({rd_names['W']})")
    in_w = st.number_input("Inbound (เข้าแยก)", value=4488, key="in_w")
    out_w = st.number_input("Outbound (ออกจากแยก)", value=1847, key="out_w")

# --- Algorithm: Iterative Balancing (Fratar/Furness Method) ---
# สร้างเมทริกซ์สัดส่วนเริ่มต้น (Seed Matrix) - กำหนดให้ตรงไป 70% เลี้ยว 15% (ปรับเปลี่ยนได้)
# แถว: N, S, E, W (Origin) | คอลัมน์: N, S, E, W (Destination)
seed = np.array([
    [0.0, 0.7, 0.15, 0.15], # จาก N ไป N=0, S=ตรง, E=ซ้าย, W=ขวา
    [0.7, 0.0, 0.15, 0.15], # จาก S
    [0.15, 0.15, 0.0, 0.7], # จาก E
    [0.15, 0.15, 0.7, 0.0]  # จาก W
])

targets_in = np.array([in_n, in_s, in_e, in_w])
targets_out = np.array([out_n, out_s, out_e, out_w])

# วนลูปปรับสมดุล (Balancing) 10 รอบ
matrix = seed.copy()
for _ in range(10):
    # ปรับตามแถว (Inbound)
    row_sums = matrix.sum(axis=1)
    row_sums[row_sums == 0] = 1
    matrix = (matrix.T * (targets_in / row_sums)).T
    # ปรับตามคอลัมน์ (Outbound)
    col_sums = matrix.sum(axis=0)
    col_sums[col_sums == 0] = 1
    matrix = matrix * (targets_out / col_sums)

# ดึงค่าที่ประมาณได้ออกมา
def get_val(o, d): return int(round(matrix[o, d]))

# Mapping การเลี้ยว (ตัวอย่างจากทิศเหนือ)
# N_L (ไป E), N_T (ไป S), N_R (ไป W)
n_l, n_t, n_r = get_val(0, 2), get_val(0, 1), get_val(0, 3)
s_l, s_t, s_r = get_val(1, 3), get_val(1, 0), get_val(1, 2)
e_l, e_t, e_r = get_val(2, 1), get_val(2, 3), get_val(2, 0)
w_l, w_t, w_r = get_val(3, 0), get_val(3, 2), get_val(3, 1)

# --- ส่วนแสดงผล SVG Diagram ---
svg_draw = f"""
<div style="display: flex; justify-content: center;">
<svg viewBox="0 0 600 500" xmlns="http://www.w3.org/2000/svg" style="width: 100%; max-width: 600px; background: white; border: 1px solid #ccc;">
    <rect width="100%" height="100%" fill="#fafafa" />
    <text x="300" y="30" text-anchor="middle" font-size="16" font-weight="bold">{title_text}</text>

    <path d="M 250 40 V 210 M 350 40 V 210 M 250 290 V 460 M 350 290 V 460" stroke="black" fill="none" stroke-width="2"/>
    <path d="M 40 210 H 250 M 40 290 H 250 M 350 210 H 560 M 350 290 H 560" stroke="black" fill="none" stroke-width="2"/>

    <rect x="255" y="50" width="45" height="25" fill="#f8d7da" stroke="black"/><text x="277" y="67" text-anchor="middle" font-size="10" font-weight="bold">Out:{out_n}</text>
    <rect x="305" y="50" width="45" height="25" fill="#d4edda" stroke="black"/><text x="327" y="67" text-anchor="middle" font-size="10" font-weight="bold">In:{in_n}</text>

    <rect x="275" y="185" width="25" height="18" fill="white" stroke="black"/><text x="287" y="198" text-anchor="middle" font-size="9">{n_l}</text>
    <rect x="305" y="185" width="30" height="18" fill="white" stroke="black"/><text x="320" y="198" text-anchor="middle" font-size="9">{n_t}</text>
    <rect x="340" y="185" width="25" height="18" fill="white" stroke="black"/><text x="352" y="198" text-anchor="middle" font-size="9">{n_r}</text>
    <text x="280" y="208" font-size="14">↧</text><text x="315" y="208" font-size="14">↓</text><text x="345" y="208" font-size="14">↴</text>

    <rect x="235" y="295" width="25" height="18" fill="white" stroke="black"/><text x="247" y="308" text-anchor="middle" font-size="9">{s_r}</text>
    <rect x="265" y="295" width="30" height="18" fill="white" stroke="black"/><text x="280" y="308" text-anchor="middle" font-size="9">{s_t}</text>
    <rect x="300" y="295" width="25" height="18" fill="white" stroke="black"/><text x="312" y="308" text-anchor="middle" font-size="9">{s_l}</text>
    <text x="240" y="295" font-size="14">↰</text><text x="275" y="295" font-size="14">↑</text><text x="305" y="295" font-size="14">⤴</text>

    <text x="520" y="60" font-size="20">🧭</text><text x="525" y="80" font-size="10" font-weight="bold">N</text>
    <text x="300" y="480" text-anchor="middle" font-size="11" fill="gray">*ประมาณการด้วย Fratar Method (Iterative Balancing)</text>
</svg>
</div>
"""

st.components.v1.html(svg_draw, height=520)

st.success("✅ ระบบได้ทำการประมาณค่า Turning Movements ให้สอดคล้องกับปริมาณรถเข้า-ออกแล้ว")
