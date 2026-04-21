import streamlit as st

# ตั้งค่าหน้ากระดาษ
st.set_page_config(layout="wide", page_title="Traffic Movement Analysis")

# --- 1. ส่วนรับข้อมูล (Inputs) ---
with st.sidebar:
    st.header("📝 ตั้งค่าพื้นฐาน")
    title_text = st.text_input("ชื่อกราฟ", "ปริมาณจราจรปี 2569")
    n_road = st.text_input("ถนนทิศเหนือ (North)", "ถ.กาญจนาภิเษก (N)")
    s_road = st.text_input("ถนนทิศใต้ (South)", "ถ.กาญจนาภิเษก (S)")
    e_road = st.text_input("ถนนทิศตะวันออก (East)", "ถ.โครงการแนวตะวันออก-ตก")
    w_road = st.text_input("ถนนทิศตะวันตก (West)", "ถ.บางกรวย-ไทรน้อย")

st.subheader("🚗 ป้อนปริมาณจราจรรายเลน (Manual Input from Excel)")

# สร้าง 4 คอลัมน์สำหรับกรอกข้อมูลรายทิศ
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"**📍 {n_road}**")
    v_nl = st.number_input("North: ซ้าย (L)", value=816)
    v_nt = st.number_input("North: ตรง (T)", value=5025)
    v_nr = st.number_input("North: ขวา (R)", value=1196)
    total_in_n = v_nl + v_nt + v_nr

with c2:
    st.markdown(f"**📍 {s_road}**")
    v_sl = st.number_input("South: ซ้าย (L)", value=1230)
    v_st = st.number_input("South: ตรง (T)", value=5053)
    v_sr = st.number_input("South: ขวา (R)", value=1803)
    total_in_s = v_sl + v_st + v_sr

with c3:
    st.markdown(f"**📍 {e_road}**")
    v_el = st.number_input("East: ซ้าย (L)", value=1227)
    v_et = st.number_input("East: ตรง (T)", value=199)
    v_er = st.number_input("East: ขวา (R)", value=819)
    total_in_e = v_el + v_et + v_er

with c4:
    st.markdown(f"**📍 {w_road}**")
    v_wl = st.number_input("West: ซ้าย (L)", value=938)
    v_wt = st.number_input("West: ตรง (T)", value=335)
    v_wr = st.number_input("West: ขวา (R)", value=1407)
    total_in_w = v_wl + v_wt + v_wr

# --- 2. คำนวณ Outbound (รถที่มุ่งหน้าออกจากแยกไปยังทิศนั้นๆ) ---
# Logic: รถไป N = (S ตรง) + (E ขวา) + (W ซ้าย)
out_n = v_st + v_er + v_wl
out_s = v_nt + v_wr + v_el
out_e = v_wt + v_nl + v_sr
out_w = v_et + v_sl + v_nr

# --- 3. ส่วนการสร้าง Diagram (SVG) ---
# ใช้ f-string และระวังการปิดปีกกา
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
        <rect x="430" y="80" width="60" height="25" fill="white" stroke="black"/><text x="460" y="97" text-anchor="middle">{total_in_n:,}</text>
        <rect x="360" y="80" width="60" height="25" fill="white" stroke="black"/><text x="390" y="97" text-anchor="middle">{out_n:,}</text>
        <rect x="360" y="650" width="60" height="25" fill="white" stroke="black"/><text x="390" y="667" text-anchor="middle">{total_in_s:,}</text>
        <rect x="430" y="650" width="60" height="25" fill="white" stroke="black"/><text x="460" y="667" text-anchor="middle">{out_s:,}</text>
        <rect x="80" y="310" width="60" height="25" fill="white" stroke="black"/><text x="110" y="327" text-anchor="middle">{total_in_w:,}</text>
        <rect x="80" y="420" width="60" height="25" fill="white" stroke="black"/><text x="110" y="437" text-anchor="middle">{out_w:,}</text>
        <rect x="710" y="310" width="60" height="25" fill="white" stroke="black"/><text x="740" y="327" text-anchor="middle">{total_in_e:,}</text>
        <rect x="710" y="420" width="60" height="25" fill="white" stroke="black"/><text x="740" y="437" text-anchor="middle">{out_e:,}</text>
    </g>

    <g transform="translate(430, 205)">
        <text x="12" y="-10" text-anchor="middle" font-size="20">↰</text><rect x="0" y="0" width="24" height="45" fill="white" stroke="black"/><text x="12" y="28" text-anchor="middle" font-size="10" transform="rotate(-90 12,28)">{v_nl:,}</text>
        <text x="36" y="-10" text-anchor="middle" font-size="20">↓</text><rect x="24" y="0" width="24" height="45" fill="white" stroke="black"/><text x="36" y="28" text-anchor="middle" font-size="10" transform="rotate(-90 36,28)">{v_nt:,}</text>
        <text x="60" y="-10" text-anchor="middle" font-size="20">↱</text><rect x="48" y="0" width="24" height="45" fill="white" stroke="black"/><text x="60" y="28" text-anchor="middle" font-size="10" transform="rotate(-90 60,28)">{v_nr:,}</text>
    </g>

    <g transform="translate(352, 410)">
        <rect x="0" y="0" width="24" height="45" fill="white" stroke="black"/><text x="12" y="28" text-anchor="middle" font-size="10" transform="rotate(-90 12,28)">{v_sr:,}</text><text x="12" y="65" text-anchor="middle" font-size="20">↰</text>
        <rect x="24" y="0" width="24" height="45" fill="white" stroke="black"/><text x="36" y="28" text-anchor="middle" font-size="10" transform="rotate(-90 36,28)">{v_st:,}</text><text x="36" y="65" text-anchor="middle" font-size="20">↑</text>
        <rect x="48" y="0" width="24" height="45" fill="white" stroke="black"/><text x="60" y="28" text-anchor="middle" font-size="10" transform="rotate(-90 60,28)">{v_sl:,}</text><text x="60" y="65" text-anchor="middle" font-size="20">↱</text>
    </g>

    <g transform="translate(260, 290)">
        <text x="-15" y="18" text-anchor="middle" font-size="20">↰</text><rect x="0" y="0" width="50" height="23" fill="white" stroke="black"/><text x="25" y="16" text-anchor="middle" font-size="11">{v_wl:,}</text>
        <text x="-15" y="41" text-anchor="middle" font-size="20">→</text><rect x="0" y="23" width="50" height="23" fill="white" stroke="black"/><text x="25" y="39" text-anchor="middle" font-size="11">{v_wt:,}</text>
        <text x="-15" y="64" text-anchor="middle" font-size="20">↳</text><rect x="0" y="46" width="50" height="23" fill="white" stroke="black"/><text x="25" y="62" text-anchor="middle" font-size="11">{v_wr:,}</text>
    </g>

    <g transform="translate(520, 385)">
        <rect x="0" y="0" width="50" height="23" fill="white" stroke="black"/><text x="25" y="16" text-anchor="middle" font-size="11">{v_er:,}</text><text x="65" y="18" text-anchor="middle" font-size="20">↱</text>
        <rect x="0" y="23" width="50" height="23" fill="white" stroke="black"/><text x="25" y="39" text-anchor="middle" font-size="11">{v_et:,}</text><text x="65" y="41" text-anchor="middle" font-size="20">←</text>
        <rect x="0" y="46" width="50" height="23" fill="white" stroke="black"/><text x="25" y="62" text-anchor="middle" font-size="11">{v_el:,}</text><text x="65" y="64" text-anchor="middle" font-size="20">↲</text>
    </g>

    <g transform="translate(780, 100)"><circle r="20" fill="none" stroke="#666"/><path d="M 0 -15 L 5 0 L -5 0 Z" fill="red"/><text y="20" text-anchor="middle" font-size="12" font-weight="bold">N</text></g>
</svg>
</div>
"""

# แสดงผล Diagram
st.components.v1.html(svg_code, height=750)
