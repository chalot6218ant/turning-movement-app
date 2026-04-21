import streamlit as st

st.set_page_config(layout="wide", page_title="Manual Traffic Movement Analysis")

# --- Sidebar: ชื่อถนน ---
with st.sidebar:
    st.header("📝 ตั้งค่าชื่อถนน")
    title_text = st.text_input("ชื่อกราฟ", "ปริมาณจราจรปี 2569")
    n_road = st.text_input("ถนนทิศเหนือ (North)", "ถ.กาญจนาภิเษก (N)")
    s_road = st.text_input("ถนนทิศใต้ (South)", "ถ.กาญจนาภิเษก (S)")
    e_road = st.text_input("ถนนทิศตะวันออก (East)", "ถ.โครงการแนวตะวันออก-ตก")
    w_road = st.text_input("ถนนทิศตะวันตก (West)", "ถ.บางกรวย-ไทรน้อย")

st.subheader("🚗 ป้อนปริมาณจราจรรายเลน (Turning Movement Volume)")

# --- ส่วนรับข้อมูล 4 ทิศทาง (แก้ไขชื่อตัวแปรไม่ให้ซ้ำกับ st) ---
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.info(f"📍 {n_road}")
    n_l = st.number_input(f"North: เลี้ยวซ้าย (L)", value=816)
    n_t = st.number_input(f"North: ตรงไป (T)", value=5025)
    n_r = st.number_input(f"North: เลี้ยวขวา (R)", value=1196)
    inbound_n = n_l + n_t + n_r
    st.caption(f"รวม Inbound: {inbound_n:,}")

with col2:
    st.info(f"📍 {s_road}")
    s_l = st.number_input(f"South: เลี้ยวซ้าย (L)", value=1803)
    s_t = st.number_input(f"South: ตรงไป (T)", value=5053)
    s_r = st.number_input(f"South: เลี้ยวขวา (R)", value=1230)
    inbound_s = s_l + s_t + s_r
    st.caption(f"รวม Inbound: {inbound_s:,}")

with col3:
    st.info(f"📍 {e_road}")
    e_l = st.number_input(f"East: เลี้ยวซ้าย (L)", value=1227)
    e_t = st.number_input(f"East: ตรงไป (T)", value=199)
    e_r = st.number_input(f"East: เลี้ยวขวา (R)", value=819)
    inbound_e = e_l + e_t + e_r
    st.caption(f"รวม Inbound: {inbound_e:,}")

with col4:
    st.info(f"📍 {w_road}")
    w_l = st.number_input(f"West: เลี้ยวซ้าย (L)", value=938)
    w_t = st.number_input(f"West: ตรงไป (T)", value=335)
    w_r = st.number_input(f"West: เลี้ยวขวา (R)", value=1407)
    inbound_w = w_l + w_t + w_r
    st.caption(f"รวม Inbound: {inbound_w:,}")

# --- คำนวณ Outbound ตามหลักการเลี้ยวจริง ---
# รถที่ออกไปทิศ North = มาจาก South(ตรง) + East(ขวา) + West(ซ้าย)
outbound_n = s_t + e_r + w_l
# รถที่ออกไปทิศ South = มาจาก North(ตรง) + West(ขวา) + East(ซ้าย)
outbound_s = n_t + w_r + e_l
# รถที่ออกไปทิศ East = มาจาก West(ตรง) + North(ซ้าย) + South(ขวา)
outbound_e = w_t + n_l + s_r
# รถที่ออกไปทิศ West = มาจาก East(ตรง) + South(ซ้าย) + North(ขวา)
outbound_w = e_t + s_l + n_r

# --- ส่วนการสร้าง Diagram (SVG) ---
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
        <rect x="430" y="75" width="60" height="25" fill="white" stroke="black"/><text x="460" y="92" text-anchor="middle">{inbound_n:,}</text>
        <rect x="360" y="75" width="60" height="25" fill="white" stroke="black"/><text x="390" y="92" text-anchor="middle">{outbound_n:,}</text>
        
        <rect x="360" y="650" width="60" height="25" fill="white" stroke
