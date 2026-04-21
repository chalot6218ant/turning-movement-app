import streamlit as st
import numpy as np

st.set_page_config(layout="wide", page_title="Traffic Turning Analysis")

# --- 1. ส่วนรับข้อมูล ---
with st.sidebar:
    st.header("📝 ข้อมูลจราจร")
    title_text = st.text_input("ชื่อกราฟ", "ปริมาณจราจรปี 2569 (3 แยก / 4 แยก)")
    n_road = st.text_input("ถนนทิศเหนือ (N)", "ถ.กาญจนาภิเษก (N)")
    s_road = st.text_input("ถนนทิศใต้ (S)", "ถ.กาญจนาภิเษก (S)")
    e_road = st.text_input("ถนนทิศตะวันออก (E)", "ถ.โครงการแนวตะวันออก-ตก")
    w_road = st.text_input("ถนนทิศตะวันตก (W)", "ถ.บางกรวย-ไทรน้อย")

st.subheader("🚗 วิเคราะห์ Turning Movement (รองรับ 3 แยก)")

col1, col2, col3, col4 = st.columns(4)
with col1:
    in_n = st.number_input("Inbound (N)", value=0) # ลองใส่เป็น 0 ได้เลย
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

# --- 2. การคำนวณวิเคราะห์ (ปรับปรุงให้รองรับ 3 แยก) ---
t_in = np.array([in_n, in_s, in_e, in_w], dtype=float)
t_out = np.array([out_n, out_s, out_e, out_w], dtype=float)

total_in = int(np.sum(t_in))
total_out = int(np.sum(t_out))
diff = int(abs(total_in - total_out))
p_diff = (diff / total_in * 100) if total_in > 0 else 0

# Seed Matrix: กำหนดความเป็นไปได้เบื้องต้น
# [N->N, N->S, N->E, N->W] ...
seed = np.array([
    [0.0, 0.7, 0.15, 0.15], 
    [0.7, 0.0, 0.15, 0.15], 
    [0.15, 0.15, 0.0, 0.7], 
    [0.15, 0.15, 0.7, 0.0]
])

# ปรับ Seed ให้เป็น 0 ในทิศที่ไม่มีรถเข้าหรือออกจริง
for i in range(4):
    if t_in[i] == 0: seed[i, :] = 0
    if t_out[i] == 0: seed[:, i] = 0

mat = seed.copy()

# วนลูปคำนวณ (Fratar/Furness Method)
if total_in > 0 and total_out > 0:
    for _ in range(50):
        # Row Scaling (Inbound)
        row_sums = mat.sum(axis=1)
        row_indices = row_sums > 0
        mat[row_indices] = (mat[row_indices].T * (t_in[row_indices] / row_sums[row_indices])).T
        
        # Column Scaling (Outbound)
        col_sums = mat.sum(axis=0)
        col_indices = col_sums > 0
        mat[:, col_indices] = mat[:, col_indices] * (t_out[col_indices] / col_sums[col_indices])

def gv(o, d): 
    val = mat[o, d]
    return int(round(val)) if not np.isnan(val) else 0

res = {
    'nl': gv(0, 2), 'nt': gv(0, 1), 'nr': gv(0, 3),
    'sl': gv(1, 3), 'st': gv(1, 0), 'sr': gv(1, 2),
    'el': gv(2, 1), 'et': gv(2, 3), 'er': gv(2, 0),
    'wl': gv(3, 0), 'wt': gv(3, 2), 'wr': gv(3, 1)
}

# --- 3. ส่วนการสร้าง Diagram (SVG เดิม แต่รองรับค่า 0) ---
# (SVG Code เดิมของคุณทำงานได้อยู่แล้ว เพราะ res จะคืนค่าเป็น 0 หากไม่มีข้อมูล)
# [ใช้ SVG Code เดิมจากใน Prompt ของคุณได้เลยครับ]
