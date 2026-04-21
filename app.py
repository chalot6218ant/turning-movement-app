import streamlit as st
import numpy as np

st.set_page_config(layout="wide", page_title="Traffic Turning Analysis")

# --- 1. ส่วนรับข้อมูล (Total In/Out) ---
with st.sidebar:
    st.header("📝 ตั้งค่าพื้นฐาน")
    title_text = st.text_input("ชื่อกราฟ", "ปริมาณจราจรปี 2569")
    n_road = st.text_input("ถนนทิศเหนือ", "ถ.กาญจนาภิเษก (N)")
    s_road = st.text_input("ถนนทิศใต้", "ถ.กาญจนาภิเษก (S)")
    e_road = st.text_input("ถนนทิศตะวันออก", "ถ.โครงการแนวตะวันออก-ตก")
    w_road = st.text_input("ถนนทิศตะวันตก", "ถ.บางกรวย-ไทรน้อย")

st.subheader("🚗 วิเคราะห์ Turning Movement จากยอด Inbound/Outbound")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.info(f"📍 {n_road}")
    in_n = st.number_input("Inbound (N)", value=7037)
    out_n = st.number_input("Outbound (N)", value=6810)
with col2:
    st.info(f"📍 {s_road}")
    in_s = st.number_input("Inbound (S)", value=8086)
    out_s = st.number_input("Outbound (S)", value=7659)
with col3:
    st.info(f"📍 {e_road}")
    in_e = st.number_input("Inbound (E)", value=3334)
    out_e = st.number_input("Outbound (E)", value=2245)
with col4:
    st.info(f"📍 {w_road}")
    in_w = st.number_input("Inbound (W)", value=2680)
    out_w = st.number_input("Outbound (W)", value=2245)

# --- 2. การคำนวณวิเคราะห์ Turning (Fratar Balancing) ---
# สร้าง Matrix เริ่มต้น (Seed) ตามพฤติกรรมการเลี้ยวมาตรฐาน
# 0:North, 1:South, 2:East, 3:West
t_in = np.array([in_n, in_s, in_e, in_w])
t_out = np.array([out_n, out_s, out_e, out_w])

# Seed (สัดส่วนโดยประมาณ: ตรง 70%, เลี้ยวอย่างละ 15%)
seed = np.array([
    [0.0, 0.7, 0.15, 0.15], # จาก N
    [0.7, 0.0, 0.15, 0.15], # จาก S
    [0.15, 0.15, 0.0, 0.7], # จาก E
    [0.15, 0.15, 0.7, 0.0]  # จาก W
])

mat = seed.copy()
# วนลูปคำนวณเพื่อปรับสมดุล (Balancing) ให้ผลรวมตรงกับ In/Out ที่กรอก
for _ in range(30):
    # ปรับตามแถว (Inbound)
    row_sums = mat.sum(axis=1)
    mat = (mat.T * (t_in / np.maximum(row_sums, 1))).T
    # ปรับตามคอลัมน์ (Outbound)
    col_sums = mat.sum(axis=0)
    mat = mat * (t_out / np.maximum(col_sums, 1))

# ฟังก์ชันดึงค่าที่วิเคราะห์ได้
def get_v(o, d):
    return int(round(mat[o, d]))

# เก็บค่าเข้า Dictionary เพื่อนำไปวาด (ตามทิศทางเลี้ยวจริง)
res = {
    'nl': get_v(0, 2), 'nt': get_v(0, 1), 'nr': get_v(0, 3),
    'sl': get_v(1, 3), 'st': get_v(1, 0), 'sr': get_v(1, 2),
    'el': get_v(2, 1), 'et': get_v(2, 3), 'er': get_v(2, 0),
    'wl': get_v(3, 0), 'wt': get_v(3, 2), 'wr': get_v(3, 1)
}

# --- 3. ส่วนการสร้าง Diagram (SVG) ---
svg_code = f"""
<div style="display: flex; justify-content: center;">
<svg viewBox="0 0 850 750" xmlns="http://www.w3.org/2000/svg" style="background:white; border:1px solid #ccc; width:100%; max-width:850px;">
    <rect width="850" height="60" fill="#f8f9fa" />
    <text x="425" y="38" text-anchor="middle" font-size="22" font-weight="bold">{title_text}</text>

    <path d="M 350 60 V 280 M 500 60 V 280 M 350 470 V 700 M 500 470 V 700" stroke="black" stroke-width="2" fill="none"/>
    <path d="M 50 280 H 350 M 50 470 H 350 M 500 280 H 800 M 500 470 H 800" stroke="black" stroke-width="2" fill="none"/>
    <line x1="425" y1="60" x2="425" y2="280" stroke="#aaa" stroke-dasharray="5,5" />
    <line x1="425" y1="470" x2="425" y2="700" stroke="#aaa" stroke-dasharray="5,5" />
    <line x1="50" y1="375" x2="350" y2="375" stroke="#aaa" stroke-dasharray="5,5" />
    <line x1="500" y1="375" x2="800" y2="375" stroke="#aaa" stroke-dasharray="5,5" />

    <text x="445" y="140" transform="rotate(-90 445,140)" font-size="14" font-weight="bold" fill="blue">{n_road}</text>
    <text x="445" y="580" transform="rotate(-90 445,580)" font-size="14" font-weight="bold" fill="blue">{s_road}</text>
    <text x="620" y="365" font-size="14" font-weight="bold" fill="blue">{e_road}</text>
    <text x="120" y="365" font-size="14" font-weight="bold" fill="blue">{w_road}</text>

    <g font-size="12" font-weight="bold">
        <rect x="430" y="80" width="60" height="25" fill="white" stroke="black"/><text x="460" y="97" text-anchor="middle">{in_n:,}</text>
        <rect x="360" y="80" width="60" height="25" fill="white" stroke="black"/><text x="390" y="97" text-anchor="middle">{out_n:,}</text>
        <rect x="360" y="650" width="60" height="25" fill="white" stroke="black"/><text x="390" y="667" text-anchor="middle">{in_s:,}</text>
        <rect x="430" y="650" width="60" height="25" fill="white" stroke="black"/><text x="460" y="667" text-anchor="middle">{out_s:,}</text>
        <rect x="80" y="310" width="60" height="25" fill="white" stroke="black"/><text x="110" y="327" text-anchor="middle">{in_w:,}</text>
        <rect x="80" y="420" width="60" height="25" fill="white" stroke="black"/><text x="110" y="437" text-anchor="middle">{out_w:,}</text>
        <rect x="710" y="310" width="60" height="25" fill="white" stroke="black"/><text x="740" y="327" text-anchor="middle">{in_e:,}</text>
        <rect x="710" y="420" width="60" height="25" fill="white" stroke="black"/><text x="740" y="437" text-anchor="middle">{out_e:,}</text>
    </g>

    <g transform="translate(430, 205)">
        <text x="12" y="-10" text-anchor="middle" font-size="20">↰</text><rect x="0" y="0" width="24" height="45" fill="white" stroke="black"/><text x="12" y="28" text-anchor="middle" font-size="10" transform="rotate(-90 12,28)">{res['nl']:,}</text>
        <text x="36" y="-10" text-anchor="middle" font-size="20">↓</text><rect x="24" y="0" width="24" height="45" fill="white" stroke="black"/><text x="36" y="28" text-anchor="middle" font-size="10" transform="rotate(-90 36,28)">{res['nt']:,}</text>
        <text x="60" y="-10" text-anchor="middle" font-size="20">↱</text><rect x="48" y="0" width="24" height="45" fill="white" stroke="black"/><text x="60" y="28" text-anchor="middle" font-size="10" transform="rotate(-90 60,28)">{res['nr']:,}</text>
    </g>

    <g transform="translate(352, 410)">
        <rect x="0" y="0" width="24" height="45" fill="white" stroke="black"/><text x="12" y="28" text-anchor="middle" font-size="10" transform="rotate(-90 12,28)">{res['sr']:,}</text><text x="12" y="65" text-anchor="middle" font-size="20">↰</text>
        <rect x="24" y="0" width="24" height="45" fill="white" stroke="black"/><text x="36" y="28" text-anchor="middle" font-size="10" transform="rotate(-90 36,28)">{res['st']:,}</text><text x="36" y="65" text-anchor="middle" font-size="20">↑</text>
        <rect x="48" y="0" width="24" height="45" fill="white" stroke="black"/><text x="60" y="28" text-anchor="middle" font-size="10" transform="rotate(-90 60,28)">{res['sl']:,}</text><text x="60" y="65" text-anchor="middle" font-size="20">↱</text>
    </g>

    <g transform="translate(260, 290)">
        <text x="-15" y="18" text-anchor="middle" font-size="20">↱</text><rect x="0" y="0" width="50" height="23" fill="white" stroke="black"/><text x="25" y="16" text-anchor="middle" font-size="11">{res['wl']:,}</text>
        <text x="-15" y="41" text-anchor="middle" font-size="20">→</text><rect x="0" y="23" width="50" height="23" fill="white" stroke="black"/><text x="25" y="39" text-anchor="middle" font-size="11">{res['wt']:,}</text>
        <text x="-15" y="64" text-anchor="middle" font-size="20">↳</text><rect x="0" y="46" width="50" height="23" fill="white" stroke="black"/><text x="25" y="62" text-anchor="middle" font-size="11">{res['wr']:,}</text>
    </g>

    <g transform="translate(520, 385)">
        <rect x="0" y="0" width="50" height="23" fill="white" stroke="black"/><text x="25" y="16" text-anchor="middle" font-size="11">{res['er']:,}</text><text x="65" y="18" text-anchor="middle" font-size="20">↰</text>
        <rect x="0" y="23" width="50" height="23" fill="white" stroke="black"/><text x="25" y="39" text-anchor="middle" font-size="11">{res['et']:,}</text><text x="65" y="41" text-anchor="middle" font-size="20">←</text>
        <rect x="0" y="46" width="50" height="23" fill="white" stroke="black"/><text x="25" y="62" text-anchor="middle" font-size="11">{res['el']:,}</text><text x="65" y="64" text-anchor="middle" font-size="20">↲</text>
    </g>

    <g transform="translate(780, 100)"><circle r="20" fill="none" stroke="#666"/><path d="M 0 -15 L 5 0 L -5 0 Z" fill="red"/><text y="20" text-anchor="middle" font-size="12" font-weight="bold">N</text></g>
</svg>
</div>
"""

st.components.v1.html(svg_code, height=750)
