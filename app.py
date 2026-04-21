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
    <line x1="425" y1="470" x2="425" y2="700" stroke="#999" stroke-dasharray="8,5" stroke-width="1.
