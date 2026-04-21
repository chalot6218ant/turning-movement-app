import streamlit as st
import numpy as np

st.set_page_config(layout="wide", page_title="Intersection Analysis")

# --- 1. ส่วนรับข้อมูล ---
with st.sidebar:
    st.header("📝 ข้อมูลจราจร")
    title_text = st.text_input("ชื่อกราฟ", "วิเคราะห์ปริมาณจราจรทางแยก")
    n_road = st.text_input("ถนนทิศเหนือ (N)", "ถ.กาญจนาภิเษก (N)")
    s_road = st.text_input("ถนนทิศใต้ (S)", "ถ.กาญจนาภิเษก (S)")
    e_road = st.text_input("ถนนทิศตะวันออก (E)", "ถ.โครงการแนวตะวันออก-ตก")
    w_road = st.text_input("ถนนทิศตะวันตก (W)", "ถ.บางกรวย-ไทรน้อย")

st.subheader("🚗 วิเคราะห์ Turning Movement (รองรับ 3 แยก และ 4 แยก)")

col1, col2, col3, col4 = st.columns(4)
with col1:
    in_n = st.number_input("Inbound (N)", value=0) # ลองใส่เป็น 0 สำหรับ 3 แยก
    out_n = st.number_input("Outbound (N)", value=0)
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

total_in = int(np.sum(t_in))
total_out = int(np.sum(t_out))
diff = int(abs(total_in - total_out))
p_diff = (diff / total_in * 100) if total_in > 0 else 0

# ปรับ Seed Matrix: ถ้าขาไหนเป็น 0 ให้ความน่าจะเป็นในการไปทิศนั้นเป็น 0
seed = np.array([
    [0.0, 0.7, 0.15, 0.15], # จาก N ไป S, E, W
    [0.7, 0.0, 0.15, 0.15], # จาก S ไป N, E, W
    [0.15, 0.15, 0.0, 0.7], # จาก E ไป N, S, W
    [0.15, 0.15, 0.7, 0.0]  # จาก W ไป N, S, E
])

# Block ทิศที่ไม่มีรถเข้าหรือออก (บังคับให้เป็น 0 ใน Matrix)
for i in range(4):
    if t_in[i] == 0: seed[i, :] = 0
    if t_out[i] == 0: seed[:, i] = 0

mat = seed.copy()
if total_in > 0: # ป้องกัน Error กรณี 0 ทั้งหมด
    for _ in range(50): # เพิ่มรอบเพื่อให้แม่นยำขึ้น
        # ปรับแถว (Inbound)
        row_sums = mat.sum(axis=1)
        row_factor = np.divide(t_in, row_sums, out=np.zeros_like(t_in, dtype=float), where=row_sums!=0)
        mat = (mat.T * row_factor).T
        
        # ปรับคอลัมน์ (Outbound)
        col_sums = mat.sum(axis=0)
        col_factor = np.divide(t_out, col_sums, out=np.zeros_like(t_out, dtype=float), where=col_sums!=0)
        mat = mat * col_factor

def gv(o, d): return int(round(mat[o, d]))
res = {
    'nl': gv(0, 2), 'nt': gv(0, 1), 'nr': gv(0, 3),
    'sl': gv(1, 3), 'st': gv(1, 0), 'sr': gv(1, 2),
    'el': gv(2, 1), 'et': gv(2, 3), 'er': gv(2, 0),
    'wl': gv(3, 0), 'wt': gv(3, 2), 'wr': gv(3, 1)
}

# --- 3. ส่วนการสร้าง Diagram (ปรับเงื่อนไขการวาด) ---
# ฟังก์ชันช่วยเช็คว่าควรแสดงทิศนั้นไหม
def show_leg(in_v, out_v): return "inline" if (in_v > 0 or out_v > 0) else "none"

svg_code = f"""
<div style="display: flex; justify-content: center;">
<svg viewBox="0 0 850 750" xmlns="http://www.w3.org/2000/svg" style="background:white; border:1px solid #ccc; width:100%; max-width:850px;">
    <rect width="850" height="50" fill="#f8f9fa" />
    <text x="425" y="32" text-anchor="middle" font-size="22" font-weight="bold" font-family="Arial">{title_text}</text>

    <g stroke="black" stroke-width="2" fill="none">
        <path d="M 350 50 V 280 M 500 50 V 280" style="display: {show_leg(in_n, out_n)};" />
        <path d="M 350 470 V 700 M 500 470 V 700" style="display: {show_leg(in_s, out_s)};" />
        <path d="M 50 280 H 350 M 50 470 H 350" style="display: {show_leg(in_w, out_w)};" />
        <path d="M 500 280 H 800 M 500 470 H 800" style="display: {show_leg(in_e, out_e)};" />
    </g>
    
    <g stroke="#999" stroke-dasharray="5,5">
        <line x1="425" y1="50" x2="425" y2="280" style="display: {show_leg(in_n, out_n)};" />
        <line x1="425" y1="470" x2="425" y2="700" style="display: {show_leg(in_s, out_s)};" />
        <line x1="50" y1="375" x2="350" y2="375" style="display: {show_leg(in_w, out_w)};" />
        <line x1="500" y1="375" x2="800" y2="375" style="display: {show_leg(in_e, out_e)};" />
    </g>

    <defs>
        <marker id="arrow" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto">
            <path d="M0,0 L6,3 L0,6 Z" fill="black" />
        </marker>
    </defs>

    <g font-size="16" font-weight="bold" font-family="Arial">
        <g style="display: {show_leg(in_n, out_n)};">
            <text x="465" y="80" text-anchor="middle" fill="#2E7D32">IN: {in_n:,}</text> <text x="385" y="80" text-anchor="middle" fill="#C62828">OUT: {out_n:,}</text>
        </g>
        <g style="display: {show_leg(in_s, out_s)};">
            <text x="385" y="680" text-anchor="middle" fill="#2E7D32">IN: {in_s:,}</text> <text x="465" y="680" text-anchor="middle" fill="#C62828">OUT: {out_s:,}</text>
        </g>
        <g style="display: {show_leg(in_w, out_w)};">
            <text x="120" y="320" text-anchor="middle" fill="#2E7D32">IN: {in_w:,}</text> <text x="120" y="440" text-anchor="middle" fill="#C62828">OUT: {out_w:,}</text>
        </g>
        <g style="display: {show_leg(in_e, out_e)};">
            <text x="730" y="320" text-anchor="middle" fill="#2E7D32">IN: {in_e:,}</text> <text x="730" y="440" text-anchor="middle" fill="#C62828">OUT: {out_e:,}</text>
        </g>
    </g>

    <g transform="translate(630, 600)">
        <rect x="0" y="0" width="200" height="120" fill="#f0f4f7" stroke="#2c3e50" stroke-width="2" rx="10"/>
        <text x="100" y="25" text-anchor="middle" font-size="16" font-weight="bold" fill="#2c3e50">สรุปผลรวม (Total)</text>
        <line x1="10" y1="35" x2="190" y2="35" stroke="#2c3e50" stroke-width="1"/>
        <text x="20" y="60" font-size="14" font-weight="bold" fill="#2E7D32">Total IN:</text> <text x="180" y="60" text-anchor="end" font-size="14" font-weight="bold">{total_in:,}</text>
        <text x="20" y="85" font-size="14" font-weight="bold" fill="#C62828">Total OUT:</text> <text x="180" y="85" text-anchor="end" font-size="14" font-weight="bold">{total_out:,}</text>
        <text x="20" y="108" font-size="14" font-weight="bold" fill="#1976D2">Diff (%):</text> <text x="180" y="108" text-anchor="end" font-size="14" font-weight="bold">{diff:,} ({p_diff:.2f}%)</text>
    </g>

    <g transform="translate(435, 230)" style="display: { "inline" if in_n > 0 else "none" };">
        <path d="M 50 -30 Q 50 0 75 0" fill="none" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
        <path d="M 32 -30 V 10" fill="none" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
        <path d="M 14 -30 Q 14 0 -15 0" fill="none" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
        <rect x="41" y="-85" width="22" height="55" fill="white" stroke="black"/>
        <text x="52" y="-57.5" text-anchor="middle" dominant-baseline="central" font-size="14" font-weight="bold" transform="rotate(-90 52,-57.5)">{res['nl']:,}</text>
        <rect x="21" y="-85" width="22" height="55" fill="white" stroke="black"/>
        <text x="32" y="-57.5" text-anchor="middle" dominant-baseline="central" font-size="14" font-weight="bold" transform="rotate(-90 32,-57.5)">{res['nt']:,}</text>
        <rect x="1" y="-85" width="22" height="55" fill="white" stroke="black"/>
        <text x="12" y="-57.5" text-anchor="middle" dominant-baseline="central" font-size="14" font-weight="bold" transform="rotate(-90 12,-57.5)">{res['nr']:,}</text>
    </g>

    <g transform="translate(355, 410)" style="display: { "inline" if in_s > 0 else "none" };">
        <path d="M 14 45 Q 14 15 -10 15" fill="none" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
        <path d="M 32 45 V 5" fill="none" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
        <path d="M 50 45 Q 50 15 75 15" fill="none" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
        <rect x="3" y="45" width="22" height="55" fill="white" stroke="black"/>
        <text x="14" y="72.5" text-anchor="middle" dominant-baseline="central" font-size="14" font-weight="bold" transform="rotate(-90 14,72.5)">{res['sl']:,}</text>
        <rect x="21" y="45" width="22" height="55" fill="white" stroke="black"/>
        <text x="32" y="72.5" text-anchor="middle" dominant-baseline="central" font-size="14" font-weight="bold" transform="rotate(-90 32,72.5)">{res['st']:,}</text>
        <rect x="39" y="45" width="22" height="55" fill="white" stroke="black"/>
        <text x="50" y="72.5" text-anchor="middle" dominant-baseline="central" font-size="14" font-weight="bold" transform="rotate(-90 50,72.5)">{res['sr']:,}</text>
    </g>

    <g transform="translate(265, 300)" style="display: { "inline" if in_w > 0 else "none" };">
        <path d="M -30 14 Q 5 14 5 -10" fill="none" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
        <path d="M -30 32 H 10" fill="none" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
        <path d="M -30 50 Q 5 50 5 75" fill="none" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
        <rect x="-85" y="1" width="55" height="22" fill="white" stroke="black"/>
        <text x="-57.5" y="12" text-anchor="middle" dominant-baseline="central" font-size="14" font-weight="bold">{res['wl']:,}</text>
        <rect x="-85" y="21" width="55" height="22" fill="white" stroke="black"/>
        <text x="-57.5" y="32" text-anchor="middle" dominant-baseline="central" font-size="14" font-weight="bold">{res['wt']:,}</text>
        <rect x="-85" y="41" width="55" height="22" fill="white" stroke="black"/>
        <text x="-57.5" y="52" text-anchor="middle" dominant-baseline="central" font-size="14" font-weight="bold">{res['wr']:,}</text>
    </g>

    <g transform="translate(525, 385)" style="display: { "inline" if in_e > 0 else "none" };">
        <path d="M 60 50 Q 25 50 25 75" fill="none" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
        <path d="M 60 32 H 20" fill="none" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
        <path d="M 60 14 Q 25 14 25 -10" fill="none" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
        <rect x="60" y="41" width="55" height="22" fill="white" stroke="black"/>
        <text x="87.5" y="52" text-anchor="middle" dominant-baseline="central" font-size="14" font-weight="bold">{res['el']:,}</text>
        <rect x="60" y="21" width="55" height="22" fill="white" stroke="black"/>
        <text x="87.5" y="32" text-anchor="middle" dominant-baseline="central" font-size="14" font-weight="bold">{res['et']:,}</text>
        <rect x="60" y="1" width="55" height="22" fill="white" stroke="black"/>
        <text x="87.5" y="12" text-anchor="middle" dominant-baseline="central" font-size="14" font-weight="bold">{res['er']:,}</text>
    </g>

    <text x="340" y="180" transform="rotate(-90 340,180)" font-size="13" fill="blue" font-weight="bold" style="display: {show_leg(in_n, out_n)};">{n_road}</text>
    <text x="515" y="550" transform="rotate(-90 515,550)" font-size="13" fill="blue" font-weight="bold" style="display: {show_leg(in_s, out_s)};">{s_road}</text>
    <text x="650" y="270" font-size="13" fill="blue" font-weight="bold" style="display: {show_leg(in_e, out_e)};">{e_road}</text>
    <text x="100" y="485" font-size="13" fill="blue" font-weight="bold" style="display: {show_leg(in_w, out_w)};">{w_road}</text>
</svg>
</div>
"""

st.components.v1.html(svg_code, height=750)
