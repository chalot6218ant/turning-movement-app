import streamlit as st
import numpy as np

st.set_page_config(layout="wide", page_title="Traffic Turning Analysis")

# --- 1. ส่วนรับข้อมูล ---
with st.sidebar:
    st.header("📝 ข้อมูลจราจร")
    title_text = st.text_input("ชื่อกราฟ", "ปริมาณจราจรปี 2569")
    n_road = st.text_input("ถนนทิศเหนือ (N)", "ถ.กาญจนาภิเษก (N)")
    s_road = st.text_input("ถนนทิศใต้ (S)", "ถ.กาญจนาภิเษก (S)")
    e_road = st.text_input("ถนนทิศตะวันออก (E)", "ถ.โครงการแนวตะวันออก-ตก")
    w_road = st.text_input("ถนนทิศตะวันตก (W)", "ถ.บางกรวย-ไทรน้อย")

st.subheader("🚗 วิเคราะห์ Turning Movement (ปรับขนาดลูกศรและตัวเลข)")

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

# --- 2. การคำนวณวิเคราะห์ ---
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

# --- 3. ส่วนการสร้าง Diagram ---
svg_code = f"""
<div style="display: flex; justify-content: center;">
<svg viewBox="0 0 850 750" xmlns="http://www.w3.org/2000/svg" style="background:white; border:1px solid #ccc; width:100%; max-width:850px;">
    <rect width="850" height="50" fill="#f8f9fa" />
    <text x="425" y="32" text-anchor="middle" font-size="22" font-weight="bold" font-family="Arial">{title_text}</text>

    <path d="M 350 50 V 280 M 500 50 V 280 M 350 470 V 700 M 500 470 V 700" stroke="black" stroke-width="2" fill="none"/>
    <path d="M 50 280 H 350 M 50 470 H 350 M 500 280 H 800 M 500 470 H 800" stroke="black" stroke-width="2" fill="none"/>
    
    <line x1="425" y1="50" x2="425" y2="280" stroke="#999" stroke-dasharray="5,5" />
    <line x1="425" y1="470" x2="425" y2="700" stroke="#999" stroke-dasharray="5,5" />
    <line x1="50" y1="375" x2="350" y2="375" stroke="#999" stroke-dasharray="5,5" />
    <line x1="500" y1="375" x2="800" y2="375" stroke="#999" stroke-dasharray="5,5" />

    <defs>
        <marker id="arrow" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto">
            <path d="M0,0 L6,3 L0,6 Z" fill="black" />
        </marker>
    </defs>

    <g font-size="14" font-weight="bold" font-family="Arial" fill="#d35400">
        <text x="465" y="75" text-anchor="middle">IN: {in_n:,}</text> <text x="385" y="75" text-anchor="middle">OUT: {out_n:,}</text>
        <text x="385" y="685" text-anchor="middle">IN: {in_s:,}</text> <text x="465" y="685" text-anchor="middle">OUT: {out_s:,}</text>
        <text x="100" y="330" text-anchor="middle">IN: {in_w:,}</text> <text x="100" y="440" text-anchor="middle">OUT: {out_w:,}</text>
        <text x="750" y="330" text-anchor="middle">IN: {in_e:,}</text> <text x="750" y="440" text-anchor="middle">OUT: {out_e:,}</text>
    </g>

    <g transform="translate(435, 230)">
        <path d="M 50 -30 Q 50 0 75 0" fill="none" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
        <path d="M 32 -30 V 10" fill="none" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
        <path d="M 14 -30 Q 14 0 -15 0" fill="none" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
        
        <rect x="42" y="-75" width="18" height="45" fill="white" stroke="black"/><text x="51" y="-52" text-anchor="middle" font-size="11" font-weight="bold" transform="rotate(-90 51,-52)">{res['nl']:,}</text>
        <rect x="23" y="-75" width="18" height="45" fill="white" stroke="black"/><text x="32" y="-52" text-anchor="middle" font-size="11" font-weight="bold" transform="rotate(-90 32,-52)">{res['nt']:,}</text>
        <rect x="4" y="-75" width="18" height="45" fill="white" stroke="black"/><text x="13" y="-52" text-anchor="middle" font-size="11" font-weight="bold" transform="rotate(-90 13,-52)">{res['nr']:,}</text>
    </g>

    <g transform="translate(355, 410)">
        <path d="M 14 45 Q 14 15 -10 15" fill="none" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
        <path d="M 32 45 V 5" fill="none" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
        <path d="M 50 45 Q 50 15 75 15" fill="none" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
        
        <rect x="5" y="45" width="18" height="45" fill="white" stroke="black"/><text x="14" y="68" text-anchor="middle" font-size="11" font-weight="bold" transform="rotate(-90 14,68)">{res['sl']:,}</text>
        <rect x="23" y="45" width="18" height="45" fill="white" stroke="black"/><text x="32" y="68" text-anchor="middle" font-size="11" font-weight="bold" transform="rotate(-90 32,68)">{res['st']:,}</text>
        <rect x="42" y="45" width="18" height="45" fill="white" stroke="black"/><text x="51" y="68" text-anchor="middle" font-size="11" font-weight="bold" transform="rotate(-90 51,68)">{res['sr']:,}</text>
    </g>

    <g transform="translate(265, 300)">
        <path d="M -30 14 Q 5 14 5 -10" fill="none" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
        <path d="M -30 32 H 10" fill="none" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
        <path d="M -30 50 Q 5 50 5 75" fill="none" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
        
        <rect x="-75" y="4" width="45" height="18" fill="white" stroke="black"/><text x="-52" y="18" text-anchor="middle" font-size="11" font-weight="bold">{res['wl']:,}</text>
        <rect x="-75" y="23" width="45" height="18" fill="white" stroke="black"/><text x="-52" y="37" text-anchor="middle" font-size="11" font-weight="bold">{res['wt']:,}</text>
        <rect x="-75" y="42" width="45" height="18" fill="white" stroke="black"/><text x="-52" y="56" text-anchor="middle" font-size="11" font-weight="bold">{res['wr']:,}</text>
    </g>

    <g transform="translate(525, 385)">
        <path d="M 60 50 Q 25 50 25 75" fill="none" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
        <path d="M 60 32 H 20" fill="none" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
        <path d="M 60 14 Q 25 14 25 -10" fill="none" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
        
        <rect x="60" y="42" width="45" height="18" fill="white" stroke="black"/><text x="82" y="56" text-anchor="middle" font-size="11" font-weight="bold">{res['el']:,}</text>
        <rect x="60" y="23" width="45" height="18" fill="white" stroke="black"/><text x="82" y="37" text-anchor="middle" font-size="11" font-weight="bold">{res['et']:,}</text>
        <rect x="60" y="4" width="45" height="18" fill="white" stroke="black"/><text x="82" y="18" text-anchor="middle" font-size="11" font-weight="bold">{res['er']:,}</text>
    </g>

    <text x="340" y="180" transform="rotate(-90 340,180)" font-size="12" fill="blue" font-weight="bold">{n_road}</text>
    <text x="515" y="550" transform="rotate(-90 515,550)" font-size="12" fill="blue" font-weight="bold">{s_road}</text>
    <text x="650" y="270" font-size="12" fill="blue" font-weight="bold">{e_road}</text>
    <text x="100" y="485" font-size="12" fill="blue" font-weight="bold">{w_road}</text>
</svg>
</div>
"""

st.components.v1.html(svg_code, height=750)
