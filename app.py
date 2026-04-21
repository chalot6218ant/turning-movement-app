import streamlit as st
import numpy as np

st.set_page_config(layout="wide", page_title="Traffic Turning Analysis")

# --- 1. ส่วนรับข้อมูล (Inbound/Outbound) ---
with st.sidebar:
    st.header("📝 ข้อมูลจราจร")
    title_text = st.text_input("ชื่อกราฟ", "ปริมาณจราจรปี 2569")
    n_road = st.text_input("ถนนทิศเหนือ (N)", "ถ.กาญจนาภิเษก (N)")
    s_road = st.text_input("ถนนทิศใต้ (S)", "ถ.กาญจนาภิเษก (S)")
    e_road = st.text_input("ถนนทิศตะวันออก (E)", "ถ.โครงการแนวตะวันออก-ตก")
    w_road = st.text_input("ถนนทิศตะวันตก (W)", "ถ.บางกรวย-ไทรน้อย")

st.subheader("🚗 วิเคราะห์ Turning Movement (สไตล์ตามรูปตัวอย่าง)")

col1, col2, col3, col4 = st.columns(4)
with col1:
    in_n = st.number_input("Inbound (N)", value=7037)
    out_n = st.number_input("Outbound (N)", value=6810)
with col2:
    in_s = st.number_input("Inbound (S)", value=8086)
    out_s = st.number_input("Outbound (S)", value=7659)
with col3:
    in_e = st.number_input("Inbound (E)", value=3334)
    out_e = st.number_input("Outbound (E)", value=2245)
with col4:
    in_w = st.number_input("Inbound (W)", value=2680)
    out_w = st.number_input("Outbound (W)", value=2245)

# --- 2. การคำนวณวิเคราะห์ (Fratar Method) ---
t_in = np.array([in_n, in_s, in_e, in_w])
t_out = np.array([out_n, out_s, out_e, out_w])
seed = np.array([[0.0, 0.7, 0.15, 0.15], [0.7, 0.0, 0.15, 0.15], [0.15, 0.15, 0.0, 0.7], [0.15, 0.15, 0.7, 0.0]])
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
    <rect width="850" height="50" fill="#f8f9fa" />
    <text x="425" y="32" text-anchor="middle" font-size="20" font-weight="bold" font-family="Arial">{title_text}</text>

    <path d="M 350 50 V 280 M 500 50 V 280 M 350 470 V 700 M 500 470 V 700" stroke="black" stroke-width="2" fill="none"/>
    <path d="M 50 280 H 350 M 50 470 H 350 M 500 280 H 800 M 500 470 H 800" stroke="black" stroke-width="2" fill="none"/>
    
    <line x1="425" y1="50" x2="425" y2="280" stroke="#999" stroke-dasharray="5,5" />
    <line x1="425" y1="470" x2="425" y2="700" stroke="#999" stroke-dasharray="5,5" />
    <line x1="50" y1="375" x2="350" y2="375" stroke="#999" stroke-dasharray="5,5" />
    <line x1="500" y1="375" x2="800" y2="375" stroke="#999" stroke-dasharray="5,5" />

    <defs>
        <marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">
            <path d="M0,0 L8,4 L0,8 Z" fill="black" />
        </marker>
    </defs>

    <g transform="translate(435, 230)">
        <path d="M 10 -40 Q 10 0 45 0" fill="none" stroke="black" stroke-width="2.5" marker-end="url(#arrow)"/>
        <path d="M 32 -40 V 15" fill="none" stroke="black" stroke-width="2.5" marker-end="url(#arrow)"/>
        <path d="M 55 -40 Q 55 0 20 0" fill="none" stroke="black" stroke-width="2.5" marker-end="url(#arrow)"/>
        <rect x="0" y="-85" width="22" height="45" fill="white" stroke="black"/><text x="11" y="-62" text-anchor="middle" font-size="9" transform="rotate(-90 11,-62)">{res['nl']:,}</text>
        <rect x="22" y="-85" width="22" height="45" fill="white" stroke="black"/><text x="33" y="-62" text-anchor="middle" font-size="9" transform="rotate(-90 33,-62)">{res['nt']:,}</text>
        <rect x="44" y="-85" width="22" height="45" fill="white" stroke="black"/><text x="55" y="-62" text-anchor="middle" font-size="9" transform="rotate(-90 55,-62)">{res['nr']:,}</text>
        <text x="33" y="-100" text-anchor="middle" font-size="12" font-weight="bold">{in_n:,}</text>
    </g>

    <g transform="translate(355, 410)">
        <path d="M 10 50 Q 10 10 45 10" fill="none" stroke="black" stroke-width="2.5" marker-end="url(#arrow)"/>
        <path d="M 32 50 V -5" fill="none" stroke="black" stroke-width="2.5" marker-end="url(#arrow)"/>
        <path d="M 55 50 Q 55 10 20 10" fill="none" stroke="black" stroke-width="2.5" marker-end="url(#arrow)"/>
        <rect x="0" y="50" width="22" height="45" fill="white" stroke="black"/><text x="11" y="73" text-anchor="middle" font-size="9" transform="rotate(-90 11,73)">{res['sr']:,}</text>
        <rect x="22" y="50" width="22" height="45" fill="white" stroke="black"/><text x="33" y="73" text-anchor="middle" font-size="9" transform="rotate(-90 33,73)">{res['st']:,}</text>
        <rect x="44" y="50" width="22" height="45" fill="white" stroke="black"/><text x="55" y="73" text-anchor="middle" font-size="9" transform="rotate(-90 55,73)">{res['sl']:,}</text>
        <text x="33" y="110" text-anchor="middle" font-size="12" font-weight="bold">{in_s:,}</text>
    </g>

    <g transform="translate(265, 300)">
        <path d="M -30 10 Q 10 10 10 45" fill="none" stroke="black" stroke-width="2.5" marker-end="url(#arrow)"/>
        <path d="M -30 32 H 15" fill="none" stroke="black" stroke-width="2.5" marker-end="url(#arrow)"/>
        <path d="M -30 55 Q 10 55 10 20" fill="none" stroke="black" stroke-width="2.5" marker-end="url(#arrow)"/>
        <rect x="-80" y="0" width="50" height="22" fill="white" stroke="black"/><text x="-55" y="15" text-anchor="middle" font-size="10">{res['wl']:,}</text>
        <rect x="-80" y="22" width="50" height="22" fill="white" stroke="black"/><text x="-55" y="37" text-anchor="middle" font-size="10">{res['wt']:,}</text>
        <rect x="-80" y="44" width="50" height="22" fill="white" stroke="black"/><text x="-55" y="59" text-anchor="middle" font-size="10">{res['wr']:,}</text>
        <text x="-100" y="37" text-anchor="middle" font-size="12" font-weight="bold">{in_w:,}</text>
    </g>

    <g transform="translate(525, 385)">
        <path d="M 60 10 Q 20 10 20 50" fill="none" stroke="black" stroke-width="2.5" marker-end="url(#arrow)"/>
        <path d="M 60 32 H 15" fill="none" stroke="black" stroke-width="2.5" marker-end="url(#arrow)"/>
        <path d="M 60 55 Q 20 55 20 20" fill="none" stroke="black" stroke-width="2.5" marker-end="url(#arrow)"/>
        <rect x="60" y="0" width="50" height="22" fill="white" stroke="black"/><text x="85" y="15" text-anchor="middle" font-size="10">{res['er']:,}</text>
        <rect x="60" y="22" width="50" height="22" fill="white" stroke="black"/><text x="85" y="37" text-anchor="middle" font-size="10">{res['et']:,}</text>
        <rect x="60" y="44" width="50" height="22" fill="white" stroke="black"/><text x="85" y="59" text-anchor="middle" font-size="10">{res['el']:,}</text>
        <text x="135" y="37" text-anchor="middle" font-size="12" font-weight="bold">{in_e:,}</text>
    </g>

    <text x="340" y="150" transform="rotate(-90 340,150)" font-size="12" fill="blue" font-weight="bold">{n_road}</text>
    <text x="515" y="580" transform="rotate(-90 515,580)" font-size="12" fill="blue" font-weight="bold">{s_road}</text>
    <text x="650" y="270" font-size="12" fill="blue" font-weight="bold">{e_road}</text>
    <text x="100" y="485" font-size="12" fill="blue" font-weight="bold">{w_road}</text>

</svg>
</div>
"""

st.components.v1.html(svg_code, height=750)
