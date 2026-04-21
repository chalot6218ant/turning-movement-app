import streamlit as st
import numpy as np

st.set_page_config(layout="wide", page_title="3-Way Traffic Analysis")

# --- 1. ส่วนรับข้อมูล (3 ทิศ: South, East, West) ---
with st.sidebar:
    st.header("📝 ตั้งค่าพื้นฐาน (3 แยก)")
    title_text = st.text_input("ชื่อกราฟ", "Traffic Analysis - 3 แยก")
    s_road = st.text_input("ถนนทิศใต้", "ถ.กาญจนาภิเษก (S)")
    e_road = st.text_input("ถนนทิศตะวันออก", "ถ.โครงการแนวตะวันออก-ตก")
    w_road = st.text_input("ถนนทิศตะวันตก", "ถ.บางกรวย-ไทรน้อย")

st.subheader("🚗 วิเคราะห์ Turning Movement (เฉพาะ 3 แยก: South, East, West)")

col1, col2, col3 = st.columns(3)
with col1:
    st.info(f"📍 {s_road}")
    in_s = st.number_input("Inbound (S)", value=8086)
    out_s = st.number_input("Outbound (S)", value=7659)
with col2:
    st.info(f"📍 {e_road}")
    in_e = st.number_input("Inbound (E)", value=3334)
    out_e = st.number_input("Outbound (E)", value=2245)
with col3:
    st.info(f"📍 {w_road}")
    in_w = st.number_input("Inbound (W)", value=2680)
    out_w = st.number_input("Outbound (W)", value=2245)

# --- 2. การคำนวณวิเคราะห์ (Fratar Method สำหรับ 3 แยก) ---
# Index: 0=South, 1=East, 2=West
t_in = np.array([in_s, in_e, in_w])
t_out = np.array([out_s, out_e, out_w])

# Seed สำหรับ 3 แยก (รถจากใต้ไปออกตะวันออก/ตก, รถจากตะวันออกไปใต้/ตก เป็นต้น)
seed = np.array([
    [0.0, 0.5, 0.5], # จาก S ไป E, W
    [0.5, 0.0, 0.5], # จาก E ไป S, W
    [0.5, 0.5, 0.0]  # จาก W ไป S, E
])

mat = seed.copy()
for _ in range(30):
    mat = (mat.T * (t_in / np.maximum(mat.sum(axis=1), 1))).T
    mat = mat * (t_out / np.maximum(mat.sum(axis=0), 1))

def get_v(o, d): return int(round(mat[o, d]))

# ผลการวิเคราะห์ (3 แยกจะไม่มีการ "ตรงไป" ในบางทิศทาง)
res = {
    'sl': get_v(0, 2), 'sr': get_v(0, 1), # South เลี้ยวซ้ายไป West, ขวาไป East
    'el': get_v(1, 0), 'et': get_v(1, 2), # East เลี้ยวซ้ายไป South, ตรงไป West
    'wr': get_v(2, 0), 'wt': get_v(2, 1)  # West เลี้ยวขวาไป South, ตรงไป East
}

# --- 3. ส่วนการสร้าง Diagram (SVG) ---
svg_code = f"""
<div style="display: flex; justify-content: center;">
<svg viewBox="0 0 850 600" xmlns="http://www.w3.org/2000/svg" style="background:white; border:1px solid #ccc; width:100%; max-width:850px;">
    <rect width="850" height="60" fill="#f8f9fa" />
    <text x="425" y="38" text-anchor="middle" font-size="22" font-weight="bold">{title_text}</text>

    <path d="M 50 280 H 800 M 50 470 H 350 M 500 470 H 800 M 350 470 V 700 M 500 470 V 700" stroke="black" stroke-width="2" fill="none"/>
    <line x1="50" y1="375" x2="800" y2="375" stroke="#aaa" stroke-dasharray="5,5" />
    <line x1="425" y1="470" x2="425" y2="700" stroke="#aaa" stroke-dasharray="5,5" />

    <text x="445" y="580" transform="rotate(-90 445,580)" font-size="14" font-weight="bold" fill="blue">{s_road}</text>
    <text x="650" y="365" font-size="14" font-weight="bold" fill="blue">{e_road}</text>
    <text x="100" y="365" font-size="14" font-weight="bold" fill="blue">{w_road}</text>

    <g font-size="12" font-weight="bold">
        <rect x="360" y="600" width="60" height="25" fill="white" stroke="black"/><text x="390" y="617" text-anchor="middle">{in_s:,}</text>
        <rect x="430" y="600" width="60" height="25" fill="white" stroke="black"/><text x="460" y="617" text-anchor="middle">{out_s:,}</text>
        <rect x="720" y="310" width="60" height="25" fill="white" stroke="black"/><text x="750" y="327" text-anchor="middle">{in_e:,}</text>
        <rect x="720" y="420" width="60" height="25" fill="white" stroke="black"/><text x="750" y="437" text-anchor="middle">{out_e:,}</text>
        <rect x="70" y="310" width="60" height="25" fill="white" stroke="black"/><text x="100" y="327" text-anchor="middle">{in_w:,}</text>
        <rect x="70" y="420" width="60" height="25" fill="white" stroke="black"/><text x="100" y="437" text-anchor="middle">{out_w:,}</text>
    </g>

    <g transform="translate(352, 410)">
        <path d="M 12 55 Q 12 25 40 25" fill="none" stroke="black" stroke-width="1.5" marker-end="url(#arrowhead)"/>
        <rect x="0" y="0" width="24" height="40" fill="white" stroke="black"/><text x="12" y="22" text-anchor="middle" font-size="9" transform="rotate(-90 12,22)">{res['sr']:,}</text>
        
        <path d="M 60 55 Q 60 25 32 25" fill="none" stroke="black" stroke-width="1.5" marker-end="url(#arrowhead)"/>
        <rect x="48" y="0" width="24" height="40" fill="white" stroke="black"/><text x="60" y="22" text-anchor="middle" font-size="9" transform="rotate(-90 60,22)">{res['sl']:,}</text>
    </g>

    <g transform="translate(260, 295)">
        <path d="M -15 15 Q 15 15 15 45" fill="none" stroke="black" stroke-width="1.5" marker-end="url(#arrowhead)"/>
        <rect x="0" y="0" width="45" height="22" fill="white" stroke="black"/><text x="22" y="15" text-anchor="middle" font-size="10">{res['wr']:,}</text>
        
        <path d="M -15 37 H 15" fill="none" stroke="black" stroke-width="1.5" marker-end="url(#arrowhead)"/>
        <rect x="0" y="22" width="45" height="22" fill="white" stroke="black"/><text x="22" y="37" text-anchor="middle" font-size="10">{res['wt']:,}</text>
    </g>

    <g transform="translate(540, 385)">
        <path d="M 65 15 Q 35 15 35 45" fill="none" stroke="black" stroke-width="1.5" marker-end="url(#arrowhead)"/>
        <rect x="0" y="0" width="45" height="22" fill="white" stroke="black"/><text x="22" y="15" text-anchor="middle" font-size="10">{res['el']:,}</text>
        
        <path d="M 65 37 H 35" fill="none" stroke="black" stroke-width="1.5" marker-end="url(#arrowhead)"/>
        <rect x="0" y="22" width="45" height="22" fill="white" stroke="black"/><text x="22" y="37" text-anchor="middle" font-size="10">{res['et']:,}</text>
    </g>

    <defs>
        <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
            <polygon points="0 0, 10 3.5, 0 7" fill="black" />
        </marker>
    </defs>
</svg>
</div>
"""

st.components.v1.html(svg_code, height=700)
