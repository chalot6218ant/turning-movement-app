import streamlit as st
import numpy as np

st.set_page_config(layout="wide", page_title="Traffic Turning Analysis")

# --- 1. ส่วนรับข้อมูล (Inputs) ---
with st.sidebar:
    st.header("📝 ตั้งค่าพื้นฐาน")
    title_text = st.text_input("ชื่อกราฟ", "ปริมาณจราจรปี 2569")
    n_road = st.text_input("ถนนทิศเหนือ (N)", "ถ.กาญจนาภิเษก (N)")
    s_road = st.text_input("ถนนทิศใต้ (S)", "ถ.กาญจนาภิเษก (S)")
    e_road = st.text_input("ถนนทิศตะวันออก (E)", "ถ.โครงการแนวตะวันออก-ตก")
    w_road = st.text_input("ถนนทิศตะวันตก (W)", "ถ.บางกรวย-ไทรน้อย")

st.subheader("🚗 วิเคราะห์ Turning Movement (4 แยกพร้อมลูกศรโค้งสมจริง)")

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

# --- 2. การคำนวณวิเคราะห์ (Fratar Method) ---
t_in = np.array([in_n, in_s, in_e, in_w])
t_out = np.array([out_n, out_s, out_e, out_w])

seed = np.array([
    [0.0, 0.7, 0.15, 0.15],
    [0.7, 0.0, 0.15, 0.15],
    [0.15, 0.15, 0.0, 0.7],
    [0.15, 0.15, 0.7, 0.0]
])

mat = seed.copy()
for _ in range(30):
    mat = (mat.T * (t_in / np.maximum(mat.sum(axis=1), 1))).T
    mat = mat * (t_out / np.maximum(mat.sum(axis=0), 1))

def gv(o, d): return int(round(mat[o, d]))

res = {
    'nl': gv(0, 2), 'nt': gv(0, 1), 'nr': gv(0, 3),
    'sl': gv(1, 3), 'st': gv(1, 0), 'sr': gv(1, 2),
    'el': gv(2, 1), 'et': gv(2, 3), 'er': gv(2, 0),
    'wl': gv(3, 0), 'wt': gv(3, 2), 'wr': gv(3, 1)
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

    <defs>
        <marker id="arr" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
            <polygon points="0 0, 10 3.5, 0 7" fill="black" />
        </marker>
    </defs>

    <g transform="translate(430, 205)">
        <path d="M 12 -15 Q 12 15 40 15" fill="none" stroke="black" stroke-width="1.2" marker-end="url(#arr)"/>
        <rect x="0" y="0" width="24" height="40" fill="white" stroke="black"/><text x="12" y="25" text-anchor="middle" font-size="9" transform="rotate(-90 12,25)">{res['nl']:,}</text>
        <path d="M 36 -15 V 10" fill="none" stroke="black" stroke-width="1.2" marker-end="url(#arr)"/>
        <rect x="24" y="0" width="24" height="40" fill="white" stroke="black"/><text x="36" y="25" text-anchor="middle" font-size="9" transform="rotate(-90 36,25)">{res['nt']:,}</text>
        <path d="M 60 -15 Q 60 15 32 15" fill="none" stroke="black" stroke-width="1.2" marker-end="url(#arr)"/>
        <rect x="48" y="0" width="24" height="40" fill="white" stroke="black"/><text x="60" y="25" text-anchor="middle" font-size="9" transform="rotate(-90 60,25)">{res['nr']:,}</text>
    </g>

    <g transform="translate(352, 415)">
        <path d="M 12 55 Q 12 25 40 25" fill="none" stroke="black" stroke-width="1.2" marker-end="url(#arr)"/>
        <rect x="0" y="0" width="24" height="40" fill="white" stroke="black"/><text x="12" y="25" text-anchor="middle" font-size="9" transform="rotate(-90 12,25)">{res['sr']:,}</text>
        <path d="M 36 55 V 30" fill="none" stroke="black" stroke-width="1.2" marker-end="url(#arr)"/>
        <rect x="24" y="0" width="24" height="40" fill="white" stroke="black"/><text x="36" y="25" text-anchor="middle" font-size="9" transform="rotate(-90 36,25)">{res['st']:,}</text>
        <path d="M 60 55 Q 60 25 32 25" fill="none" stroke="black" stroke-width="1.2" marker-end="url(#arr)"/>
        <rect x="48" y="0" width="24" height="40" fill="white" stroke="black"/><text x="60" y="25" text-anchor="middle" font-size="9" transform="rotate(-90 60,25)">{res['sl']:,}</text>
    </g>

    <g transform="translate(265, 295)">
        <path d="M -15 11 Q 15 11 15 40" fill="none" stroke="black" stroke-width="1.2" marker-end="url(#arr)"/>
        <rect x="0" y="0" width="45" height="22" fill="white" stroke="black"/><text x="22" y="15" text-anchor="middle" font-size="10">{res['wl']:,}</text>
        <path d="M -15 33 H 10" fill="none" stroke="black" stroke-width="1.2" marker-end="url(#arr)"/>
        <rect x="0" y="22" width="45" height="22" fill="white" stroke="black"/><text x="22" y="37" text-anchor="middle" font-size="10">{res['wt']:,}</text>
        <path d="M -15 55 Q 15 55 15 25" fill="none" stroke="black" stroke-width="1.2" marker-end="url(#arr)"/>
        <rect x="0" y="44" width="45" height="22" fill="white" stroke="black"/><text x="22" y="59" text-anchor="middle" font-size="10">{res['wr']:,}</text>
    </g>

    <g transform="translate(540, 385)">
        <path d="M 60 11 Q 30 11 30 40" fill="none" stroke="black" stroke-width="1.2" marker-end="url(#arr)"/>
        <rect x="0" y="0" width="45" height="22" fill="white" stroke="black"/><text x="22" y="15" text-anchor="middle" font-size="10">{res['er']:,}</text>
        <path d="M 60 33 H 35" fill="none" stroke="black" stroke-width="1.2" marker-end="url(#arr)"/>
        <rect x="0" y="22" width="45" height="22" fill="white" stroke="black"/><text x="22" y="37" text-anchor="middle" font-size="10">{res['et']:,}</text>
        <path d="M 60 55 Q 30 55 30 25" fill="none" stroke="black" stroke-width="1.2" marker-end="url(#arr)"/>
        <rect x="0" y="44" width="45" height="22" fill="white" stroke="black"/><text x="22" y="59" text-anchor="middle" font-size="10">{res['el']:,}</text>
    </g>

</svg>
</div>
"""

st.components.v1.html(svg_code, height=750)
