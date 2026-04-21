import streamlit as st

st.set_page_config(layout="wide", page_title="Traffic Turning Movement")

# --- Sidebar: สำหรับแก้ไขชื่อถนนและหัวข้อ ---
with st.sidebar:
    st.header("📍 Settings")
    title_text = st.text_input("หัวข้อแผนภูมิ", "Year 2006 AM")
    rd_n = st.text_input("ถนนทิศเหนือ", "ติวานนท์")
    rd_s = st.text_input("ถนนทิศใต้", "ติวานนท์")
    rd_e = st.text_input("ถนนทิศตะวันออก", "งามวงศ์วาน")
    rd_w = st.text_input("ถนนทิศตะวันตก", "รัตนาธิเบศร์")

# --- ส่วนกรอกข้อมูล: ใช้ Expander เพื่อประหยัดพื้นที่ ---
with st.expander("📝 คลิกเพื่อกรอกปริมาณจราจร (PCU/Hr.)", expanded=True):
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.caption(f"ทิศเหนือ ({rd_n})")
        n_l, n_t, n_r = st.number_input("N-Left", 25), st.number_input("N-Through", 1190), st.number_input("N-Right", 2362)
    with c2:
        st.caption(f"ทิศใต้ ({rd_s})")
        s_l, s_t, s_r = st.number_input("S-Left", 1693), st.number_input("S-Through", 481), st.number_input("S-Right", 60)
    with c3:
        st.caption(f"ทิศตะวันออก ({rd_e})")
        e_l, e_t, e_r = st.number_input("E-Left", 752), st.number_input("E-Through", 1762), st.number_input("E-Right", 1114)
    with c4:
        st.caption(f"ทิศตะวันตก ({rd_w})")
        w_l, w_t, w_r = st.number_input("W-Left", 516), st.number_input("W-Through", 3935), st.number_input("W-Right", 37)

# --- คำนวณผลรวม ---
in_n, out_n = (n_l+n_t+n_r), (s_t+e_r+w_l)
in_s, out_s = (s_l+s_t+s_r), (n_t+w_r+e_l)
in_e, out_e = (e_l+e_t+e_r), (w_t+n_l+s_r)
in_w, out_w = (w_l+w_t+w_r), (e_t+s_l+n_r)

# --- SVG Rendering: ปรับให้ Responsive และขนาดพอดีจอ ---
svg_code = f"""
<div style="display: flex; justify-content: center; background-color: #f0f2f6; padding: 10px; border-radius: 10px;">
<svg viewBox="0 0 800 600" preserveAspectRatio="xMidYMid meet" xmlns="http://www.w3.org/2000/svg" style="width: 100%; max-width: 800px; height: auto; background: white; border: 1px solid #ccc; box-shadow: 2px 2px 10px rgba(0,0,0,0.1);">
    <defs>
        <pattern id="grid" width="20" height="20" patternUnits="userSpaceOnUse">
            <path d="M 20 0 L 0 0 0 20" fill="none" stroke="#f0f0f0" stroke-width="1"/>
        </pattern>
    </defs>
    <rect width="100%" height="100%" fill="url(#grid)" />
    
    <text x="400" y="35" text-anchor="middle" font-size="18" font-weight="bold" fill="#333">{title_text}</text>

    <line x1="330" y1="50" x2="330" y2="250" stroke="black" stroke-width="2" />
    <line x1="470" y1="50" x2="470" y2="250" stroke="black" stroke-width="2" />
    <line x1="330" y1="350" x2="330" y2="550" stroke="black" stroke-width="2" />
    <line x1="470" y1="350" x2="470" y2="550" stroke="black" stroke-width="2" />
    <line x1="50" y1="250" x2="330" y2="250" stroke="black" stroke-width="2" />
    <line x1="50" y1="350" x2="330" y2="350" stroke="black" stroke-width="2" />
    <line x1="470" y1="250" x2="750" y2="250" stroke="black" stroke-width="2" />
    <line x1="470" y1="350" x2="750" y2="350" stroke="black" stroke-width="2" />

    <text x="405" y="160" transform="rotate(-90 405,160)" font-size="13" font-weight="bold" fill="blue">{rd_n}</text>
    <text x="405" y="440" transform="rotate(-90 405,440)" font-size="13" font-weight="bold" fill="blue">{rd_s}</text>
    <text x="610" y="305" font-size="13" font-weight="bold" fill="blue">{rd_e}</text>
    <text x="180" y="305" font-size="13" font-weight="bold" fill="blue">{rd_w}</text>

    <rect x="345" y="80" width="55" height="25" fill="white" stroke="black" /> <text x="372.5" y="97" text-anchor="middle" font-size="12">{out_n:,}</text>
    <rect x="405" y="80" width="55" height="25" fill="white" stroke="black" /> <text x="432.5" y="97" text-anchor="middle" font-size="12">{in_n:,}</text>
    
    <rect x="345" y="495" width="55" height="25" fill="white" stroke="black" /> <text x="372.5" y="512" text-anchor="middle" font-size="12">{in_s:,}</text>
    <rect x="405" y="495" width="55" height="25" fill="white" stroke="black" /> <text x="432.5" y="512" text-anchor="middle" font-size="12">{out_s:,}</text>

    <rect x="650" y="265" width="55" height="25" fill="white" stroke="black" /> <text x="677.5" y="282" text-anchor="middle" font-size="12">{in_e:,}</text>
    <rect x="650" y="310" width="55" height="25" fill="white" stroke="black" /> <text x="677.5" y="327" text-anchor="middle" font-size="12">{out_e:,}</text>

    <rect x="95" y="265" width="55" height="25" fill="white" stroke="black" /> <text x="122.5" y="282" text-anchor="middle" font-size="12">{in_w:,}</text>
    <rect x="95" y="310" width="55" height="25" fill="white" stroke="black" /> <text x="122.5" y="327" text-anchor="middle" font-size="12">{out_w:,}</text>

    <rect x="375" y="220" width="28" height="22" fill="white" stroke="black" /> <text x="389" y="236" text-anchor="middle" font-size="11">{n_l}</text>
    <rect x="405" y="220" width="35" height="22" fill="white" stroke="black" /> <text x="422.5" y="236" text-anchor="middle" font-size="11">{n_t}</text>
    <rect x="442" y="220" width="28" height="22" fill="white" stroke="black" /> <text x="456" y="236" text-anchor="middle" font-size="11">{n_r}</text>
    <text x="382" y="248" font-size="18">↧</text> <text x="415" y="248" font-size="18">↓</text> <text x="448" y="248" font-size="18">↴</text>

    <rect x="332" y="358" width="28" height="22" fill="white" stroke="black" /> <text x="346" y="374" text-anchor="middle" font-size="11">{s_r}</text>
    <rect x="362" y="358" width="35" height="22" fill="white" stroke="black" /> <text x="379.5" y="374" text-anchor="middle" font-size="11">{s_t}</text>
    <rect x="399" y="358" width="28" height="22" fill="white" stroke="black" /> <text x="413" y="374" text-anchor="middle" font-size="11">{s_l}</text>
    <text x="336" y="355" font-size="18">↰</text> <text x="372" y="355" font-size="18">↑</text> <text x="406" y="355" font-size="18">⤴</text>

    <rect x="475" y="260" width="35" height="22" fill="white" stroke="black" /> <text x="492.5" y="276" text-anchor="middle" font-size="11">{e_l}</text>
    <rect x="475" y="285" width="35" height="22" fill="white" stroke="black" /> <text x="492.5" y="301" text-anchor="middle" font-size="11">{e_t}</text>
    <rect x="475" y="310" width="35" height="22" fill="white" stroke="black" /> <text x="492.5" y="326" text-anchor="middle" font-size="11">{e_r}</text>
    <text x="515" y="278" font-size="18" text-anchor="start">↤</text> <text x="515" y="303" font-size="18" text-anchor="start">←</text> <text x="515" y="328" font-size="18" text-anchor="start">↲</text>

    <rect x="290" y="260" width="35" height="22" fill="white" stroke="black" /> <text x="307.5" y="276" text-anchor="middle" font-size="11">{w_r}</text>
    <rect x="290" y="285" width="35" height="22" fill="white" stroke="black" /> <text x="307.5" y="301" text-anchor="middle" font-size="11">{w_t}</text>
    <rect x="290" y="310" width="35" height="22" fill="white" stroke="black" /> <text x="307.5" y="326" text-anchor="middle" font-size="11">{w_l}</text>
    <text x="268" y="278" font-size="18" text-anchor="end">↱</text> <text x="268" y="303" font-size="18" text-anchor="end">→</text> <text x="268" y="328" font-size="18" text-anchor="end">↳</text>

    <g transform="translate(730, 60)">
        <circle cx="0" cy="0" r="20" fill="none" stroke="#666" stroke-width="1" />
        <path d="M 0 -15 L 5 0 L -5 0 Z" fill="red" />
        <text x="0" y="25" text-anchor="middle" font-size="12" font-weight="bold">N</text>
    </g>
    
    <text x="50" y="580" font-size="11" fill="#666">หน่วย : PCU/Hr.</text>
</svg>
</div>
"""

st.markdown(svg_code, unsafe_allow_html=True)
