import streamlit as st
import numpy as np

st.set_page_config(layout="wide", page_title="Traffic Movement Analysis")

# --- 1. ส่วนรับข้อมูล (Inputs) ---
with st.sidebar:
    st.header("📝 ตั้งค่าพื้นฐาน")
    title_text = st.text_input("ชื่อกราฟ (Title)", "Year 2006 AM")
    n_road = st.text_input("ถนนทิศเหนือ (North)", "ถ.กาญจนาภิเษก (N)")
    s_road = st.text_input("ถนนทิศใต้ (South)", "ถ.กาญจนาภิเษก (S)")
    e_road = st.text_input("ถนนทิศตะวันออก (East)", "ถ.โครงการแนวตะวันออก-ตก")
    w_road = st.text_input("ถนนทิศตะวันตก (West)", "ถ.บางกรวย-ไทรน้อย")

st.subheader("🚗 ป้อนปริมาณจราจร (PCU/Hr)")
c1, c2, c3, c4 = st.columns(4)
with c1:
    in_n = st.number_input(f"ขาเข้า (In) {n_road}", value=7037)
    out_n = st.number_input(f"ขาออก (Out) {n_road}", value=6810)
with c2:
    in_s = st.number_input(f"ขาเข้า (In) {s_road}", value=8086)
    out_s = st.number_input(f"ขาออก (Out) {s_road}", value=7659)
with c3:
    in_e = st.number_input(f"ขาเข้า (In) {e_road}", value=3334)
    out_e = st.number_input(f"ขาออก (Out) {e_road}", value=2245)
with c4:
    in_w = st.number_input(f"ขาเข้า (In) {w_road}", value=2680)
    out_w = st.number_input(f"ขาออก (Out) {w_road}", value=2245)

# --- 2. ส่วนการคำนวณ (Fratar Balancing) ---
# ระบบจะรันส่วนนี้ใหม่ทุกครั้งที่ค่า Input ด้านบนเปลี่ยน
t_in = np.array([in_n, in_s, in_e, in_w])
t_out = np.array([out_n, out_s, out_e, out_w])

# Seed สำหรับกระจายรถ (เลี้ยวซ้าย/ตรง/เลี้ยวขวา)
seed = np.array([
    [0, 0.7, 0.15, 0.15], # จาก N ไป S, E, W
    [0.7, 0, 0.15, 0.15], # จาก S ไป N, E, W
    [0.15, 0.15, 0, 0.7], # จาก E ไป W, N, S
    [0.15, 0.15, 0.7, 0]  # จาก W ไป E, N, S
])

mat = seed.copy()
for _ in range(25): # Balancing 25 รอบ
    mat = (mat.T * (t_in / np.maximum(mat.sum(axis=1), 1))).T
    mat = mat * (t_out / np.maximum(mat.sum(axis=0), 1))

def gv(o, d): return f"{int(round(mat[o, d])):,}"

# ดึงค่าที่คำนวณได้มาเก็บในตัวแปรสำหรับ SVG
# n=0, s=1, e=2, w=3
val = {
    'nl': gv(0, 2), 'nt': gv(0, 1), 'nr': gv(0, 3), # North Inbound
    'sl': gv(1, 3), 'st': gv(1, 0), 'sr': gv(1, 2), # South Inbound
    'el': gv(2, 1), 'et': gv(2, 3), 'er': gv(2, 0), # East Inbound
    'wl': gv(3, 0), 'wt': gv(3, 2), 'wr': gv(3, 1)  # West Inbound
}

# --- 3. ส่วนการสร้าง Diagram (SVG) ---
svg_code = f"""
<div style="display: flex; justify-content: center;">
<svg viewBox="0 0 850 750" xmlns="http://www.w3.org/2000/svg" style="background:white; border:1px solid #ddd; width:100%; max-width:850px;">
    <rect width="850" height="60" fill="#f0f2f6" />
    <text x="425" y="38" text-anchor="middle" font-size="24" font-weight="bold">{title_text}</text>

    <path d="M 350 60 V 280 M 500 60 V 280 M 350 470 V 700 M 500 470 V 700" stroke="black" stroke-width="2" fill="none"/>
    <path d="M 50 280 H 350 M 50 470 H 350 M 500 280 H 800 M 500 470 H 800" stroke="black" stroke-width="2" fill="none"/>
    <line x1="425" y1="60" x2="425" y2="280" stroke="#aaa" stroke-dasharray="5,5" />
    <line x1="425" y1="470" x2="425" y2="700" stroke="#aaa" stroke-dasharray="5,5" />
    <line x1="50" y1="375" x2="350" y2="375" stroke="#aaa" stroke-dasharray="5,5" />
    <line x1="500" y1="375" x2="800" y2="375" stroke="#aaa" stroke-dasharray="5,5" />

    <text x="440" y="150" transform="rotate(-90 440,150)" font-size="14" font-weight="bold" fill="blue">{n_road}</text>
    <text x="440" y="600" transform="rotate(-90 440,600)" font-size="14" font-weight="bold" fill="blue">{s_road}</text>
    <text x="610" y="360" font-size="14" font-weight="bold" fill="blue">{e_road}</text>
    <text x="130" y="360" font-size="14" font-weight="bold" fill="blue">{w_road}</text>

    <g font-size="12" font-weight="bold">
        <rect x="430" y="75" width="60" height="25" fill="white" stroke="black"/><text x="460" y="92" text-anchor="middle">{in_n:,}</text>
        <rect x="360" y="75" width="60" height="25" fill="white" stroke="black"/><text x="390" y="92" text-anchor="middle">{out_n:,}</text>
        <rect x="360" y="650" width="60" height="25" fill="white" stroke="black"/><text x="390" y="667" text-anchor="middle">{in_s:,}</text>
        <rect x="430" y="650" width="60" height="25" fill="white" stroke="black"/><text x="460" y="667" text-anchor="middle">{out_s:,}</text>
        <rect x="80" y="300" width="65" height="25" fill="white" stroke="black"/><text x="112.5" y="317" text-anchor="middle">{in_w:,}</text>
        <rect x="80" y="425" width="65" height="25" fill="white" stroke="black"/><text x="112.5" y="442" text-anchor="middle">{out_w:,}</text>
        <rect x="705" y="300" width="65" height="25" fill="white" stroke="black"/><text x="737.5" y="317" text-anchor="middle">{in_e:,}</text>
        <rect x="705" y="425" width="65" height="25" fill="white" stroke="black"/><text x="737.5" y="442" text-anchor="middle">{out_e:,}</text>
    </g>

    <g transform="translate(430, 215)">
        <text x="12" y="-10" text-anchor="middle" font-size="20">↰</text><rect x="0" y="0" width="24" height="35" fill="white" stroke="black"/><text x="12" y="22" text-anchor="middle" font-size="10" transform="rotate(-90 12,22)">{val['nl']}</text>
        <text x="36" y="-10" text-anchor="middle" font-size="20">↓</text><rect x="24" y="0" width="24" height="35" fill="white" stroke="black"/><text x="36" y="22" text-anchor="middle" font-size="10" transform="rotate(-90 36,22)">{val['nt']}</text>
        <text x="60" y="-10" text-anchor="middle" font-size="20">↱</text><rect x="48" y="0" width="24" height="35" fill="white" stroke="black"/><text x="60" y="22" text-anchor="middle" font-size="10" transform="rotate(-90 60,22)">{val['nr']}</text>
    </g>

    <g transform="translate(352, 420)">
        <rect x="0" y="0" width="24" height="35" fill="white" stroke="black"/><text x="12" y="22" text-anchor="middle" font-size="10" transform="rotate(-90 12,22)">{val['sr']}</text><text x="12" y="55" text-anchor="middle" font-size="20">↰</text>
        <rect x="24" y="0" width="24" height="35" fill="white" stroke="black"/><text x="36" y="22" text-anchor="middle" font-size="10" transform="rotate(-90 36,22)">{val['st']}</text><text x="36" y="55" text-anchor="middle" font-size="20">↑</text>
        <rect x="48" y="0" width="24" height="35" fill="white" stroke="black"/><text x="60" y="22" text-anchor="middle" font-size="10" transform="rotate(-90 60,22)">{val['sl']}</text><text x="60" y="55" text-anchor="middle" font-size="20">↱</text>
    </g>

    <g transform="translate(275, 295)">
        <text x="-15" y="18" text-anchor="middle" font-size="20">↱</text><rect x="0" y="0" width="45" height="22" fill="white" stroke="black"/><text x="22" y="15" text-anchor="middle" font-size="11">{val['wr']}</text>
        <text x="-15" y="40" text-anchor="middle" font-size="20">→</text><rect x="0" y="22" width="45" height="22" fill="white" stroke="black"/><text x="22" y="37" text-anchor="middle" font-size="11">{val['wt']}</text>
        <text x="-15" y="62" text-anchor="middle" font-size="20">↳</text><rect x="0" y="44" width="45" height="22" fill="white" stroke="black"/><text x="22" y="59" text-anchor="middle" font-size="11">{val['wl']}</text>
    </g>

    <g transform="translate(510, 385)">
        <rect x="0" y="0" width="45" height="22" fill="white" stroke="black"/><text x="22" y="15" text-anchor="middle" font-size="11">{val['er']}</text><text x="60" y="18" text-anchor="middle" font-size="20">↰</text>
        <rect x="0" y="22" width="45" height="22" fill="white" stroke="black"/><text x="22" y="37" text-anchor="middle" font-size="11">{val['et']}</text><text x="60" y="40" text-anchor="middle" font-size="20">←</text>
        <rect x="0" y="44" width="45" height="22" fill="white" stroke="black"/><text x="22" y="59" text-anchor="middle" font-size="11">{val['el']}</text><text x="60" y="62" text-anchor="middle" font-size="20">↲</text>
    </g>

    <g transform="translate(780, 100)"><circle r="20" fill="none" stroke="#666"/><path d="M 0 -15 L 5 0 L -5 0 Z" fill="red"/><text y="20" text-anchor="middle" font-size="12" font-weight="bold">N</text></g>
</svg>
</div>
"""

st.components.v1.html(svg_code, height=750)
