import streamlit as st
import numpy as np

st.set_page_config(layout="wide", page_title="Traffic Movement Analysis")

# --- Sidebar ---
with st.sidebar:
    st.header("📝 Edit Road Names")
    title_text = st.text_input("Chart Title", "Year 2006 AM")
    n_road = st.text_input("North Road", "ถ.กาญจนาภิเษก (N)")
    s_road = st.text_input("South Road", "ถ.กาญจนาภิเษก (S)")
    e_road = st.text_input("East Road", "ถ.โครงการแนวตะวันออก-ตก")
    w_road = st.text_input("West Road", "ถ.บางกรวย-ไทรน้อย")

# --- Input Traffic Volume ---
st.subheader("🚗 ป้อนปริมาณจราจร (PCU/Hr)")
col1, col2, col3, col4 = st.columns(4)
with col1:
    in_n, out_n = st.number_input(f"In {n_road}", value=7037), st.number_input(f"Out {n_road}", value=6810)
with col2:
    in_s, out_s = st.number_input(f"In {s_road}", value=8086), st.number_input(f"Out {s_road}", value=7659)
with col3:
    in_e, out_e = st.number_input(f"In {e_road}", value=3334), st.number_input(f"Out {e_road}", value=2245)
with col4:
    in_w, out_w = st.number_input(f"In {w_road}", value=2680), st.number_input(f"Out {w_road}", value=2245)

# --- Calculation (Fratar Method) ---
t_in = np.array([in_n, in_s, in_e, in_w])
t_out = np.array([out_n, out_s, out_e, out_w])
seed = np.array([[0, 0.7, 0.15, 0.15], [0.7, 0, 0.15, 0.15], [0.15, 0.15, 0, 0.7], [0.15, 0.15, 0.7, 0]])
mat = seed.copy()
for _ in range(20):
    mat = (mat.T * (t_in / np.maximum(mat.sum(axis=1), 1))).T
    mat = mat * (t_out / np.maximum(mat.sum(axis=0), 1))

def gv(o, d): return int(round(mat[o, d]))
v = {
    'nl': gv(0, 2), 'nt': gv(0, 1), 'nr': gv(0, 3),
    'sl': gv(1, 3), 'st': gv(1, 0), 'sr': gv(1, 2),
    'el': gv(2, 1), 'et': gv(2, 3), 'er': gv(2, 0),
    'wl': gv(3, 0), 'wt': gv(3, 2), 'wr': gv(3, 1)
}

# --- SVG Drawing ---
final_svg = f"""
<div style="display: flex; justify-content: center;">
<svg viewBox="0 0 850 750" xmlns="http://www.w3.org/2000/svg" style="background:white; border:1px solid #333; width:100%; max-width:850px;">
    <rect width="850" height="60" fill="#f8f9fa" />
    <text x="425" y="38" text-anchor="middle" font-size="22" font-weight="bold" fill="#333">{title_text}</text>

    <path d="M 350 60 V 280 M 500 60 V 280 M 350 470 V 700 M 500 470 V 700" stroke="black" stroke-width="2" fill="none"/>
    <path d="M 50 280 H 350 M 50 470 H 350 M 500 280 H 800 M 500 470 H 800" stroke="black" stroke-width="2" fill="none"/>
    
    <line x1="425" y1="60" x2="425" y2="280" stroke="#ccc" stroke-dasharray="5,5" />
    <line x1="425" y1="470" x2="425" y2="700" stroke="#ccc" stroke-dasharray="5,5" />
    <line x1="50" y1="375" x2="350" y2="375" stroke="#ccc" stroke-dasharray="5,5" />
    <line x1="500" y1="375" x2="800" y2="375" stroke="#ccc" stroke-dasharray="5,5" />

    <text x="445" y="140" transform="rotate(-90 445,140)" font-size="14" font-weight="bold" fill="blue">{n_road}</text>
    <text x="445" y="580" transform="rotate(-90 445,580)" font-size="14" font-weight="bold" fill="blue">{s_road}</text>
    <text x="620" y="360" font-size="14" font-weight="bold" fill="blue">{e_road}</text>
    <text x="120" y="360" font-size="14" font-weight="bold" fill="blue">{w_road}</text>

    <g font-size="11" font-weight="bold">
        <rect x="360" y="70" width="60" height="25" fill="#fff" stroke="#000"/><text x="390" y="87" text-anchor="middle">Out:{out_n}</text>
        <rect x="430" y="70" width="60" height="25" fill="#fff" stroke="#000"/><text x="460" y="87" text-anchor="middle">In:{in_n}</text>
        <rect x="360" y="660" width="60" height="25" fill="#fff" stroke="#000"/><text x="390" y="677" text-anchor="middle">In:{in_s}</text>
        <rect x="430" y="660" width="60" height="25" fill="#fff" stroke="#000"/><text x="460" y="677" text-anchor="middle">Out:{out_s}</text>
        <rect x="60" y="290" width="65" height="25" fill="#fff" stroke="#000"/><text x="92.5" y="307" text-anchor="middle">In:{in_w}</text>
        <rect x="60" y="435" width="65" height="25" fill="#fff" stroke="#000"/><text x="92.5" y="452" text-anchor="middle">Out:{out_w}</text>
        <rect x="725" y="290" width="65" height="25" fill="#fff" stroke="#000"/><text x="757.5" y="307" text-anchor="middle">In:{in_e}</text>
        <rect x="725" y="435" width="65" height="25" fill="#fff" stroke="#000"/><text x="757.5" y="452" text-anchor="middle">Out:{out_e}</text>
    </g>

    <g transform="translate(430, 210)">
        <rect x="0" y="0" width="22" height="22" fill="white" stroke="black"/><text x="11" y="16" text-anchor="middle" font-size="14">↰</text>
        <rect x="0" y="22" width="22" height="22" fill="white" stroke="black"/><text x="11" y="37" text-anchor="middle" font-size="9" transform="rotate(-90 11,37)">{v['nl']}</text>
        <rect x="22" y="0" width="22" height="22" fill="white" stroke="black"/><text x="33" y="16" text-anchor="middle" font-size="14">↓</text>
        <rect x="22" y="22" width="22" height="22" fill="white" stroke="black"/><text x="33" y="37" text-anchor="middle" font-size="9" transform="rotate(-90 33,37)">{v['nt']}</text>
        <rect x="44" y="0" width="22" height="22" fill="white" stroke="black"/><text x="55" y="16" text-anchor="middle" font-size="14">↱</text>
        <rect x="44" y="22" width="22" height="22" fill="white" stroke="black"/><text x="55" y="37" text-anchor="middle" font-size="9" transform="rotate(-90 55,37)">{v['nr']}</text>
    </g>

    <g transform="translate(358, 425)">
        <rect x="0" y="0" width="22" height="22" fill="white" stroke="black"/><text x="11" y="16" text-anchor="middle" font-size="14">↰</text>
        <rect x="0" y="22" width="22" height="22" fill="white" stroke="black"/><text x="11" y="37" text-anchor="middle" font-size="9" transform="rotate(-90 11,37)">{v['sr']}</text>
        <rect x="22" y="0" width="22" height="22" fill="white" stroke="black"/><text x="33" y="16" text-anchor="middle" font-size="14">↑</text>
        <rect x="22" y="22" width="22" height="22" fill="white" stroke="black"/><text x="33" y="37" text-anchor="middle" font-size="9" transform="rotate(-90 33,37)">{v['st']}</text>
        <rect x="44" y="0" width="22" height="22" fill="white" stroke="black"/><text x="55" y="16" text-anchor="middle" font-size="14">↱</text>
        <rect x="44" y="22" width="22" height="22" fill="white" stroke="black"/><text x="55" y="37" text-anchor="middle" font-size="9" transform="rotate(-90 55,37)">{v['sl']}</text>
    </g>

    <g transform="translate(285, 290)">
        <rect x="0" y="0" width="30" height="22" fill="white" stroke="black"/><text x="15" y="16" text-anchor="middle" font-size="14">↱</text>
        <rect x="30" y="0" width="35" height="22" fill="white" stroke="black"/><text x="47.5" y="15" text-anchor="middle" font-size="10">{v['wr']}</text>
        
        <rect x="0" y="22" width="30" height="22" fill="white" stroke="black"/><text x="15" y="38" text-anchor="middle" font-size="14">→</text>
        <rect x="30" y="22" width="35" height="22" fill="white" stroke="black"/><text x="47.5" y="37" text-anchor="middle" font-size="10">{v['wt']}</text>
        
        <rect x="0" y="44" width="30" height="22" fill="white" stroke="black"/><text x="15" y="60" text-anchor="middle" font-size="14">↳</text>
        <rect x="30" y="44" width="35" height="22" fill="white" stroke="black"/><text x="47.5" y="59" text-anchor="middle" font-size="10">{v['wl']}</text>
    </g>

    <g transform="translate(500, 380)">
        <rect x="0" y="0" width="30" height="22" fill="white" stroke="black"/><text x="15" y="16" text-anchor="middle" font-size="14">↰</text>
        <rect x="30" y="0" width="35" height="22" fill="white" stroke="black"/><text x="47.5" y="15" text-anchor="middle" font-size="10">{v['er']}</text>
        
        <rect x="0" y="22" width="30" height="22" fill="white" stroke="black"/><text x="15" y="38" text-anchor="middle" font-size="14">←</text>
        <rect x="30" y="22" width="35" height="22" fill="white" stroke="black"/><text x="47.5" y="37" text-anchor="middle" font-size="10">{v['et']}</text>
        
        <rect x="0" y="44" width="30" height="22" fill="white" stroke="black"/><text x="15" y="60" text-anchor="middle" font-size="14">↲</text>
        <rect x="30" y="44" width="35" height="22" fill="white" stroke="black"/><text x="47.5" y="59" text-anchor="middle" font-size="10">{v['el']}</text>
    </g>

    <rect x="580" y="580" width="200" height="85" fill="#fcfcfc" stroke="#333" rx="5"/>
    <text x="680" y="605" text-anchor="middle" font-size="14" font-weight="bold">Summary Total</text>
    <text x="595" y="630" font-size="12">In: {int(t_in.sum()):,}</text>
    <text x="595" y="650" font-size="12">Out: {int(t_out.sum()):,}</text>

    <g transform="translate(750, 110)"><circle r="18" fill="none" stroke="#666"/><path d="M 0 -14 L 3 0 L -3 0 Z" fill="red"/><text y="15" text-anchor="middle" font-size="9" font-weight="bold">N</text></g>
</svg>
</div>
"""

st.components.v1.html(final_svg, height=750)
