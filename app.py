import streamlit as st

st.set_page_config(layout="wide", page_title="Traffic Calculator")

# --- Sidebar ---
with st.sidebar:
    st.header("⚙️ Settings")
    title_text = st.text_input("หัวข้อแผนภูมิ", "Year 2006 AM")
    rd_n = st.text_input("ถนนทิศเหนือ", "ติวานนท์")
    rd_s = st.text_input("ถนนทิศใต้", "ติวานนท์")
    rd_e = st.text_input("ถนนทิศตะวันออก", "งามวงศ์วาน")
    rd_w = st.text_input("ถนนทิศตะวันตก", "รัตนาธิเบศร์")

# --- Input Area (ย่อส่วนลง) ---
with st.expander("📝 ป้อนปริมาณจราจร", expanded=True):
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        n_l, n_t, n_r = st.number_input("N: L/T/R", 25, 1190, 2362, key="n")
    with c2:
        s_l, s_t, s_r = st.number_input("S: L/T/R", 1693, 481, 60, key="s")
    with c3:
        e_l, e_t, e_r = st.number_input("E: L/T/R", 752, 1762, 1114, key="e")
    with c4:
        w_l, w_t, w_r = st.number_input("W: L/T/R", 516, 3935, 37, key="w")

# --- คำนวณ ---
in_n, out_n = (n_l+n_t+n_r), (s_t+e_r+w_l)
in_s, out_s = (s_l+s_t+s_r), (n_t+w_r+e_l)
in_e, out_e = (e_l+e_t+e_r), (w_t+n_l+s_r)
in_w, out_w = (w_l+w_t+w_r), (e_t+s_l+n_r)

# --- SVG Code (ปรับขนาดให้กระชับ 600x500) ---
svg_draw = f"""
<div style="display: flex; justify-content: center;">
<svg viewBox="0 0 600 500" xmlns="http://www.w3.org/2000/svg" style="width: 100%; max-width: 600px; background: white; border: 1px solid #ccc;">
    <defs>
        <pattern id="smallGrid" width="15" height="15" patternUnits="userSpaceOnUse">
            <path d="M 15 0 L 0 0 0 15" fill="none" stroke="#f0f0f0" stroke-width="0.5"/>
        </pattern>
    </defs>
    <rect width="100%" height="100%" fill="url(#smallGrid)" />
    
    <text x="300" y="30" text-anchor="middle" font-size="16" font-weight="bold">{title_text}</text>

    <path d="M 250 40 V 210 M 350 40 V 210 M 250 290 V 460 M 350 290 V 460" stroke="black" fill="none" />
    <path d="M 40 210 H 250 M 40 290 H 250 M 350 210 H 560 M 350 290 H 560" stroke="black" fill="none" />

    <text x="300" y="140" transform="rotate(-90 300,140)" font-size="11" fill="blue">{rd_n}</text>
    <text x="300" y="360" transform="rotate(-90 300,360)" font-size="11" fill="blue">{rd_s}</text>
    <text x="450" y="255" font-size="11" fill="blue">{rd_e}</text>
    <text x="140" y="255" font-size="11" fill="blue">{rd_w}</text>

    <rect x="255" y="60" width="40" height="20" fill="white" stroke="black"/><text x="275" y="74" text-anchor="middle" font-size="10">{out_n:,}</text>
    <rect x="305" y="60" width="40" height="20" fill="white" stroke="black"/><text x="325" y="74" text-anchor="middle" font-size="10">{in_n:,}</text>
    
    <rect x="255" y="420" width="40" height="20" fill="white" stroke="black"/><text x="275" y="434" text-anchor="middle" font-size="10">{in_s:,}</text>
    <rect x="305" y="420" width="40" height="20" fill="white" stroke="black"/><text x="325" y="434" text-anchor="middle" font-size="10">{out_s:,}</text>

    <rect x="480" y="220" width="45" height="20" fill="white" stroke="black"/><text x="502.5" y="234" text-anchor="middle" font-size="10">{in_e:,}</text>
    <rect x="480" y="260" width="45" height="20" fill="white" stroke="black"/><text x="502.5" y="274" text-anchor="middle" font-size="10">{out_e:,}</text>

    <rect x="70" y="220" width="45" height="20" fill="white" stroke="black"/><text x="92.5" y="234" text-anchor="middle" font-size="10">{in_w:,}</text>
    <rect x="70" y="260" width="45" height="20" fill="white" stroke="black"/><text x="92.5" y="274" text-anchor="middle" font-size="10">{out_w:,}</text>

    <rect x="280" y="185" width="22" height="18" fill="white" stroke="black"/><text x="291" y="198" text-anchor="middle" font-size="9">{n_l}</text>
    <rect x="305" y="185" width="28" height="18" fill="white" stroke="black"/><text x="319" y="198" text-anchor="middle" font-size="9">{n_t}</text>
    <rect x="335" y="185" width="22" height="18" fill="white" stroke="black"/><text x="346" y="198" text-anchor="middle" font-size="9">{n_r}</text>
    <text x="288" y="210" font-size="15">↧</text><text x="315" y="210" font-size="15">↓</text><text x="340" y="210" font-size="15">↴</text>

    <rect x="242" y="295" width="22" height="18" fill="white" stroke="black"/><text x="253" y="308" text-anchor="middle" font-size="9">{s_r}</text>
    <rect x="267" y="295" width="28" height="18" fill="white" stroke="black"/><text x="281" y="308" text-anchor="middle" font-size="9">{s_t}</text>
    <rect x="298" y="295" width="22" height="18" fill="white" stroke="black"/><text x="309" y="308" text-anchor="middle" font-size="9">{s_l}</text>
    <text x="245" y="295" font-size="15">↰</text><text x="275" y="295" font-size="15">↑</text><text x="302" y="295" font-size="15">⤴</text>

    <rect x="355" y="215" width="30" height="18" fill="white" stroke="black"/><text x="370" y="228" text-anchor="middle" font-size="9">{e_l}</text>
    <rect x="355" y="235" width="30" height="18" fill="white" stroke="black"/><text x="370" y="248" text-anchor="middle" font-size="9">{e_t}</text>
    <rect x="355" y="255" width="30" height="18" fill="white" stroke="black"/><text x="370" y="268" text-anchor="middle" font-size="9">{e_r}</text>
    <text x="388" y="230" font-size="15">↤</text><text x="388" y="250" font-size="15">←</text><text x="388" y="270" font-size="15">↲</text>

    <rect x="215" y="215" width="30" height="18" fill="white" stroke="black"/><text x="230" y="228" text-anchor="middle" font-size="9">{w_r}</text>
    <rect x="215" y="235" width="30" height="18" fill="white" stroke="black"/><text x="230" y="248" text-anchor="middle" font-size="9">{w_t}</text>
    <rect x="215" y="255" width="30" height="18" fill="white" stroke="black"/><text x="230" y="268" text-anchor="middle" font-size="9">{w_l}</text>
    <text x="200" y="230" font-size="15">↱</text><text x="200" y="250" font-size="15">→</text><text x="200" y="270" font-size="15">↳</text>

    <text x="520" y="60" font-size="20">🧭</text><text x="525" y="80" font-size="10" font-weight="bold">N</text>
    <text x="50" y="480" font-size="9">หน่วย : PCU/Hr.</text>
</svg>
</div>
"""

# --- ส่วนสำคัญ: ต้องใช้ st.components.v1.html เพื่อแสดงภาพ ---
st.components.v1.html(svg_draw, height=520)
