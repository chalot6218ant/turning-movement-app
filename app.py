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

st.subheader("🚗 วิเคราะห์ Turning Movement สไตล์ลูกศรหนา")

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
    <rect width="850" height="60" fill="#f8f9fa" />
    <text x="425" y="38" text-anchor="middle" font-size="22" font-weight="bold" font-family="Arial">{title_text}</text>

    <path d="M 350 60 V 280 M 500 60 V 280 M 350 470 V 700 M 500 470 V 700" stroke="black" stroke-width="2.5" fill="none"/>
    <path d="M 50 280 H 350 M 50 470 H 350 M 500 280 H 800 M 500 470 H 800" stroke="black" stroke-width="2.5" fill="none"/>
    
    <line x1="425" y1="60" x2="425" y2="280" stroke="#999" stroke-dasharray="8,5" stroke-width="1.5"/>
    <line x1="425" y1="470" x2="425" y2="700" stroke="#999" stroke-dasharray="8,5" stroke-width="1.5"/>
    <line x1="50" y1="375" x2="350" y2="375" stroke="#999" stroke-dasharray="8,5" stroke-width="1.5"/>
    <line x1="500" y1="375" x2="800" y2="375" stroke="#999" stroke-dasharray="8,5" stroke-width="1.5"/>

    <text x="445" y="140" transform="rotate(-90 445,140)" font-size="14" font-weight="bold" fill="#2c3e50" font-family="Arial">{n_road}</text>
    <text x="445" y="580" transform="rotate(-90 445,580)" font-size="14" font-weight="bold" fill="#2c3e50" font-family="Arial">{s_road}</text>
    <text x="620" y="365" font-size="14" font-weight="bold" fill="#2c3e50" font-family="Arial">{e_road}</text>
    <text x="120" y="365" font-size="14" font-weight="bold" fill="#2c3e50" font-family="Arial">{w_road}</text>

    <defs>
        <marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto">
            <path d="M0,0 L10,5 L0,10 Z" fill="black" />
        </marker>
    </defs>

    <g font-size="13" font-weight="bold" font-family="Arial">
        <rect x="430" y="80" width="65" height="28" fill="white" stroke="black" stroke-width="1.5"/><text x="462" y="99" text-anchor="middle">{in_n:,}</text>
        <rect x="355" y="80" width="65" height="28" fill="white" stroke="black" stroke-width="1.5"/><text x="387" y="99" text-anchor="middle">{out_n:,}</text>
        <rect x="355" y="640" width="65" height="28" fill="white" stroke="black" stroke-width="1.5"/><text x="387" y="659" text-anchor="middle">{in_s:,}</text>
        <rect x="430" y="640" width="65" height="28" fill="white" stroke="black" stroke-width="1.5"/><text x="462" y="659" text-anchor="middle">{out_s:,}</text>
    </g>

    <g transform="translate(430, 190)">
        <path d="M 12 0 Q 12 40 50 40" fill="none" stroke="black" stroke-width="3" marker-end="url(#arrow)"/>
        <rect x="0" y="0" width="24" height="45" fill="white" stroke="black"/><text x="12" y="28" text-anchor="middle" font-size="10" font-weight="bold" transform="rotate(-90 12,28)">{res['nl']:,}</text>
        
        <path d="M 36 0 V 45" fill="none" stroke="black" stroke-width="3" marker-end="url(#arrow)"/>
        <rect x="24" y="0" width="24" height="45" fill="white" stroke="black"/><text x="36" y="28" text-anchor="middle" font-size="10" font-weight="bold" transform="rotate(-90 36,28)">{res['nt']:,}</text>
        
        <path d="M 60 0 Q 60 40 20 40" fill="none" stroke="black" stroke-width="3" marker-end="url(#arrow)"/>
        <rect x="48" y="0" width="24" height="45" fill="white" stroke="black"/><text x="60" y="28" text-anchor="middle" font-size="10" font-weight="bold" transform="rotate(-90 60,28)">{res['nr']:,}</text>
    </g>

    <g transform="translate(352, 430)">
        <path d="M 12 45 Q 12 5 50 5" fill="none" stroke="black" stroke-width="3" marker-end="url(#arrow)"/>
        <rect x="0" y="0" width="24" height="45" fill="white" stroke="black"/><text x="12" y="28" text-anchor="middle" font-size="10" font-weight="bold" transform="rotate(-90 12,28)">{res['sr']:,}</text>
        
        <path d="M 36 45 V 0" fill="none" stroke="black" stroke-width="3" marker-end="url(#arrow)"/>
        <rect x="24" y="0" width="24" height="45" fill="white" stroke="black"/><text x="36" y="28" text-anchor="middle" font-size="10" font-weight="bold" transform="rotate(-90 36,28)">{res['st']:,}</text>
        
        <path d="M 60 45 Q 60 5 20 5" fill="none" stroke="black" stroke-width="3" marker-end="url(#arrow)"/>
        <rect x="48" y="0" width="24" height="45" fill="white" stroke="black"/><text x="60" y="28" text-anchor="middle" font-size="10" font-weight="bold" transform="rotate(-90 60,28)">{res['sl']:,}</text>
    </g>

    <g transform="translate(255, 290)">
        <path d="M 0 11 Q 45 11 45 50" fill="none" stroke="black" stroke-width="3" marker-end="url(#arrow)"/>
        <rect x="0" y="0" width="52" height="23" fill="white" stroke="black"/><text x="26" y="16" text-anchor="middle" font-size="11" font-weight="bold">{res['wl']:,}</text>
        
        <path d="M 0 34 H 55" fill="none" stroke="black" stroke-width="3" marker-end="url(#arrow)"/>
        <rect x="0" y="23" width="52" height="23" fill="white" stroke="black"/><text x="26" y="39" text-anchor="middle" font-size="11" font-weight="bold">{res['wt']:,}</text>
        
        <path d="M 0 57 Q 45 57 45 20" fill="none" stroke="black" stroke-width="3" marker-end="url(#arrow)"/>
        <rect x="0" y="46" width="52" height="23" fill="white" stroke="black"/><text x="26" y="62" text-anchor="middle" font-size="11" font-weight="bold">{res['wr']:,}</text>
    </g>

    <g transform="translate(545, 385)">
        <path d="M 52 11 Q 7 11 7 50" fill="none" stroke="black" stroke-width="3" marker-end="url(#arrow)"/>
        <rect x="0" y="0" width="52" height="23" fill="white" stroke="black"/><text x="26" y="16" text-anchor="middle" font-size="11" font-weight="bold">{res['er']:,}</text>
        
        <path d="M 52 34 H -3" fill="none" stroke="black" stroke-width="3" marker-end="url(#arrow)"/>
        <rect x="0" y="23" width="52" height="23" fill="white" stroke="black"/><text x="26" y="39" text-anchor="middle" font-size="11" font-weight="bold">{res['et']:,}</text>
        
        <path d="M 52 57 Q 7 57 7 20" fill="none" stroke="black" stroke-width="3" marker-end="url(#arrow)"/>
        <rect x="0" y="46" width="52" height="23" fill="white" stroke="black"/><text x="26" y="62" text-anchor="middle" font-size="11" font-weight="bold">{res['el']:,}</text>
    </g>
</svg>
</div>
"""

st.components.v1.html(svg_code, height=750)
