import streamlit as st

st.set_page_config(layout="wide", page_title="Traffic Turning Movement")

# --- Sidebar Settings ---
st.sidebar.header("⚙️ Configuration")
title_text = st.sidebar.text_input("Header Title", "Year 2006 AM")
rd_n = st.sidebar.text_input("North Road", "ติวานนท์")
rd_s = st.sidebar.text_input("South Road", "ติวานนท์")
rd_e = st.sidebar.text_input("East Road", "งามวงศ์วาน")
rd_w = st.sidebar.text_input("West Road", "รัตนาธิเบศร์")

# --- Input Section ---
st.subheader("📝 Input Traffic Volume (PCU/Hr.)")
c1, c2, c3, c4 = st.columns(4)
with c1:
    n_l, n_t, n_r = st.number_input("N-Left", 25), st.number_input("N-Through", 1190), st.number_input("N-Right", 2362)
with c2:
    s_l, s_t, s_r = st.number_input("S-Left", 1693), st.number_input("S-Through", 481), st.number_input("S-Right", 60)
with c3:
    e_l, e_t, e_r = st.number_input("E-Left", 752), st.number_input("E-Through", 1762), st.number_input("E-Right", 1114)
with c4:
    w_l, w_t, w_r = st.number_input("W-Left", 516), st.number_input("W-Through", 3935), st.number_input("W-Right", 37)

# --- Calculation ---
in_n, out_n = (n_l+n_t+n_r), (s_t+e_r+w_l)
in_s, out_s = (s_l+s_t+s_r), (n_t+w_r+e_l)
in_e, out_e = (e_l+e_t+e_r), (w_t+n_l+s_r)
in_w, out_w = (w_l+w_t+w_r), (e_t+s_l+n_r)

# --- SVG Rendering (เหมือนต้นฉบับเป๊ะ) ---
svg_code = f"""
<svg viewBox="0 0 800 700" xmlns="http://www.w3.org/2000/svg" style="background: white; border: 1px solid #ccc;">
    <defs>
        <pattern id="grid" width="20" height="20" patternUnits="userSpaceOnUse">
            <path d="M 20 0 L 0 0 0 20" fill="none" stroke="#eee" stroke-width="1"/>
        </pattern>
    </defs>
    <rect width="100%" height="100%" fill="url(#grid)" />
    
    <text x="400" y="40" text-anchor="middle" font-size="20" font-weight="bold">{title_text}</text>

    <line x1="320" y1="50" x2="320" y2="280" stroke="black" stroke-width="2" />
    <line x1="480" y1="50" x2="480" y2="280" stroke="black" stroke-width="2" />
    <line x1="320" y1="420" x2="320" y2="650" stroke="black" stroke-width="2" />
    <line x1="480" y1="420" x2="480" y2="650" stroke="black" stroke-width="2" />
    
    <line x1="50" y1="280" x2="320" y2="280" stroke="black" stroke-width="2" />
    <line x1="50" y1="420" x2="320" y2="420" stroke="black" stroke-width="2" />
    <line x1="480" y1="280" x2="750" y2="280" stroke="black" stroke-width="2" />
    <line x1="480" y1="420" x2="750" y2="420" stroke="black" stroke-width="2" />

    <text x="395" y="200" transform="rotate(-90 395,200)" font-size="14" font-weight="bold">{rd_n}</text>
    <text x="600" y="340" font-size="14" font-weight="bold">{rd_e}</text>

    <rect x="340" y="100" width="60" height="30" fill="white" stroke="black" /> <text x="370" y="120" text-anchor="middle">{out_n}</text>
    <rect x="410" y="100" width="60" height="30" fill="white" stroke="black" /> <text x="440" y="120" text-anchor="middle">{in_n}</text>
    
    <rect x="340" y="570" width="60" height="30" fill="white" stroke="black" /> <text x="370" y="590" text-anchor="middle">{in_s}</text>
    <rect x="410" y="570" width="60" height="30" fill="white" stroke="black" /> <text x="440" y="590" text-anchor="middle">{out_s}</text>

    <rect x="650" y="290" width="60" height="30" fill="white" stroke="black" /> <text x="680" y="310" text-anchor="middle">{in_e}</text>
    <rect x="650" y="380" width="60" height="30" fill="white" stroke="black" /> <text x="680" y="400" text-anchor="middle">{out_e}</text>

    <rect x="100" y="290" width="60" height="30" fill="white" stroke="black" /> <text x="130" y="310" text-anchor="middle">{in_w}</text>
    <rect x="100" y="380" width="60" height="30" fill="white" stroke="black" /> <text x="130" y="400" text-anchor="middle">{out_w}</text>

    <rect x="370" y="240" width="30" height="25" fill="white" stroke="black" /> <text x="385" y="258" text-anchor="middle" font-size="12">{n_l}</text>
    <rect x="405" y="240" width="40" height="25" fill="white" stroke="black" /> <text x="425" y="258" text-anchor="middle" font-size="12">{n_t}</text>
    <rect x="450" y="240" width="30" height="25" fill="white" stroke="black" /> <text x="465" y="258" text-anchor="middle" font-size="12">{n_r}</text>
    <text x="380" y="275" font-size="20">↧</text> <text x="420" y="275" font-size="20">↓</text> <text x="455" y="275" font-size="20">↴</text>

    <rect x="320" y="430" width="30" height="25" fill="white" stroke="black" /> <text x="335" y="448" text-anchor="middle" font-size="12">{s_r}</text>
    <rect x="355" y="430" width="40" height="25" fill="white" stroke="black" /> <text x="375" y="448" text-anchor="middle" font-size="12">{s_t}</text>
    <rect x="400" y="430" width="30" height="25" fill="white" stroke="black" /> <text x="415" y="448" text-anchor="middle" font-size="12">{s_l}</text>
    <text x="325" y="425" font-size="20">↰</text> <text x="365" y="425" font-size="20">↑</text> <text x="405" y="425" font-size="20">⤴</text>

    <rect x="530" y="320" width="40" height="25" fill="white" stroke="black" /> <text x="550" y="338" text-anchor="middle" font-size="12">{e_l}</text>
    <rect x="530" y="347" width="40" height="25" fill="white" stroke="black" /> <text x="550" y="365" text-anchor="middle" font-size="12">{e_t}</text>
    <rect x="530" y="374" width="40" height="25" fill="white" stroke="black" /> <text x="550" y="392" text-anchor="middle" font-size="12">{e_r}</text>
    <text x="500" y="335" font-size="20">↤</text> <text x="500" y="365" font-size="20">←</text> <text x="500" y="395" font-size="20">↲</text>

    <rect x="230" y="285" width="40" height="25" fill="white" stroke="black" /> <text x="250" y="303" text-anchor="middle" font-size="12">{w_r}</text>
    <rect x="230" y="312" width="40" height="25" fill="white" stroke="black" /> <text x="250" y="330" text-anchor="middle" font-size="12">{w_t}</text>
    <rect x="230" y="339" width="40" height="25" fill="white" stroke="black" /> <text x="250" y="357" text-anchor="middle" font-size="12">{w_l}</text>
    <text x="285" y="300" font-size="20">↱</text> <text x="285" y="330" font-size="20">→</text> <text x="285" y="360" font-size="20">↳</text>

    <text x="730" y="80" font-size="30">🧭</text> <text x="735" y="105" font-weight="bold">N</text>
    <text x="60" y="620" font-size="12">หน่วย : PCU/Hr.</text>
</svg>
"""

st.divider()
st.components.v1.html(svg_code, height=720)
