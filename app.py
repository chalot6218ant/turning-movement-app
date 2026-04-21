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

# --- ส่วนรับข้อมูล 4 ทิศทาง ---
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.info(f"📍 {n_road}")
    nl = st.number_input(f"North: เลี้ยวซ้าย (L)", value=816)
    nt = st.number_input(f"North: ตรงไป (T)", value=5025)
    nr = st.number_input(f"North: เลี้ยวขวา (R)", value=1196)
    in_n = nl + nt + nr
    st.caption(f"รวม Inbound: {in_n:,}")

with col2:
    st.info(f"📍 {s_road}")
    sl = st.number_input(f"South: เลี้ยวซ้าย (L)", value=1803) # อิงตามเข็มนาฬิกา
    st = st.number_input(f"South: ตรงไป (T)", value=5053)
    sr = st.number_input(f"South: เลี้ยวขวา (R)", value=1230)
    in_s = sl + st + sr
    st.caption(f"รวม Inbound: {in_s:,}")

with col3:
    st.info(f"📍 {e_road}")
    el = st.number_input(f"East: เลี้ยวซ้าย (L)", value=1227)
    et = st.number_input(f"East: ตรงไป (T)", value=199)
    er = st.number_input(f"East: เลี้ยวขวา (R)", value=819)
    in_e = el + et + er
    st.caption(f"รวม Inbound: {in_e:,}")

with col4:
    st.info(f"📍 {w_road}")
    wl = st.number_input(f"West: เลี้ยวซ้าย (L)", value=938)
    wt = st.number_input(f"West: ตรงไป (T)", value=335)
    wr = st.number_input(f"West: เลี้ยวขวา (R)", value=1407)
    in_w = wl + wt + wr
    st.caption(f"รวม Inbound: {in_w:,}")

# --- คำนวณ Outbound (ผลรวมรถที่มุ่งหน้าไปทิศนั้นๆ) ---
out_n = st + el + wr
out_s = nt + er + wl
out_e = nl + st + wr # ปรับตาม logic การเลี้ยวของสี่แยก
out_w = nr + sl + et

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
        <rect x="430" y="75" width="60" height="25" fill="white" stroke="black"/><text x="460" y="92" text-anchor="middle">{in_n:,}</text>
        <rect x="360" y="75" width="60" height="25" fill="white" stroke="black"/><text x="390" y="92" text-anchor="middle">{out_n:,}</text>
        <rect x="360" y="650" width="60" height="25" fill="white" stroke="black"/><text x="390" y="667" text-anchor="middle">{in_s:,}</text>
        <rect x="430" y="650" width="60" height="25" fill="white" stroke="black"/><text x="460" y="667" text-anchor="middle">{out_s:,}</text>
        <rect x="80" y="300" width="65" height="25" fill="white" stroke="black"/><text x="112.5" y="317" text-anchor="middle">{in_w:,}</text>
        <rect x="80" y="425" width="65" height="25" fill="white" stroke="black"/><text x="112.5" y="442" text-anchor="middle">{out_w:,}</text>
        <rect x="705" y="300" width="65" height="25" fill="white" stroke="black"/><text x="737.5" y="317" text-anchor="middle">{in_e:,}</text>
        <rect x="705" y="425" width="65" height="25" fill="white" stroke="black"/><text x="737.5" y="442" text-anchor="middle">{out_e:,}</text>
    </g>

    <g transform="translate(430, 215)">
        <text x="12" y="-10" text-anchor="middle" font-size="20">↰</text><rect x="0" y="0" width="24" height="40" fill="white" stroke="black"/><text x="12" y="25" text-anchor="middle" font-size="9" transform="rotate(-90 12,25)">{nl:,}</text>
        <text x="36" y="-10" text-anchor="middle" font-size="20">↓</text><rect x="24" y="0" width="24" height="40" fill="white" stroke="black"/><text x="36" y="25" text-anchor="middle" font-size="9" transform="rotate(-90 36,25)">{nt:,}</text>
        <text x="60" y="-10" text-anchor="middle" font-size="20">↱</text><rect x="48" y="0" width="24" height="40" fill="white" stroke="black"/><text x="60" y="25" text-anchor="middle" font-size="9" transform="rotate(-90 60,25)">{nr:,}</text>
    </g>

    <g transform="translate(352, 415)">
        <rect x="0" y="0" width="24" height="40" fill="white" stroke="black"/><text x="12" y="25" text-anchor="middle" font-size="9" transform="rotate(-90 12,25)">{sr:,}</text><text x="12" y="60" text-anchor="middle" font-size="20">↰</text>
        <rect x="24" y="0" width="24" height="40" fill="white" stroke="black"/><text x="36" y="25" text-anchor="middle" font-size="9" transform="rotate(-90 36,25)">{st:,}</text><text x="36" y="60" text-anchor="middle" font-size="20">↑</text>
        <rect x="48" y="0" width="24" height="40" fill="white" stroke="black"/><text x="60" y="25" text-anchor="middle" font-size="9" transform="rotate(-90 60,25)">{sl:,}</text><text x="60" y="60" text-anchor="middle" font-size="20">↱</text>
    </g>

    <g transform="translate(265, 295)">
        <text x="-15" y="18" text-anchor="middle" font-size="20">↱</text><rect x="0" y="0" width="48" height="22" fill="white" stroke="black"/><text x="24" y="15" text-anchor="middle" font-size="11">{wl:,}</text>
        <text x="-15" y="40" text-anchor="middle" font-size="20">→</text><rect x="0" y="22" width="48" height="22" fill="white" stroke="black"/><text x="24" y="37" text-anchor="middle" font-size="11">{wt:,}</text>
        <text x="-15" y="62" text-anchor="middle" font-size="20">↳</text><rect x="0" y="44" width="48" height="22" fill="white" stroke="black"/><text x="24" y="59" text-anchor="middle" font-size="11">{wr:,}</text>
    </g>

    <g transform="translate(515, 385)">
        <rect x="0" y="0" width="48" height="22" fill="white" stroke="black"/><text x="24" y="15" text-anchor="middle" font-size="11">{el:,}</text><text x="65" y="18" text-anchor="middle" font-size="20">↰</text>
        <rect x="0" y="22" width="48" height="22" fill="white" stroke="black"/><text x="24" y="37" text-anchor="middle" font-size="11">{et:,}</text><text x="65" y="40" text-anchor="middle" font-size="20">←</text>
        <rect x="0" y="44" width="48" height="22" fill="white" stroke="black"/><text x="24" y="59" text-anchor="middle" font-size="11">{er:,}</text><text x="65" y="62" text-anchor="middle" font-size="20">↲</text>
    </g>

    <g transform="translate(780, 100)"><circle r="20" fill="none" stroke="#666"/><path d="M 0 -15 L 5 0 L -5 0 Z" fill="red"/><text y="20" text-anchor="middle" font-size="12" font-weight="bold">N</text></g>
</svg>
</div>
"""

st.components.v1.html(svg_code, height=750)
