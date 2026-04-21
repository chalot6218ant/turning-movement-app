import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(page_title="Turning Movement Estimator", layout="wide")

st.title("🚗 Turning Movement Estimation (Include U-Turn)")
st.write("โปรแกรมประมาณค่าปริมาณจราจรเลี้ยวจากข้อมูล Midblock พร้อมรองรับ U-Turn")

# --- Sidebar: Input Data ---
with st.sidebar:
    st.header("1. ตั้งค่าทางแยก")
    junction_type = st.radio("ประเภททางแยก", ["4 แยก (Cross)", "3 แยก (T-Junction)"])
    
    legs = ["North", "South", "East", "West"] if junction_type == "4 แยก (Cross)" else ["North", "South", "East"]
    
    inbound = []
    outbound = []
    
    st.header("2. ข้อมูล Midblock (In/Out)")
    for leg in legs:
        st.subheader(f"ทิศ {leg}")
        col1, col2 = st.columns(2)
        with col1:
            val_in = st.number_input(f"เข้า (In) - {leg}", min_value=0, value=1000, key=f"in_{leg}")
        with col2:
            val_out = st.number_input(f"ออก (Out) - {leg}", min_value=0, value=1000, key=f"out_{leg}")
        inbound.append(val_in)
        outbound.append(val_out)

    st.header("3. สมมติฐานสัดส่วน (%)")
    u_turn_pct = st.slider("U-Turn โดยประมาณ (%)", 0, 20, 2)
    straight_pct = st.slider("ตรงไป โดยประมาณ (%)", 50, 90, 70)

# --- Logic ---
def estimate_tmc(in_f, out_f, labels, u_p, s_p):
    n = len(in_f)
    # สร้าง Seed Matrix
    seed = np.ones((n, n)) * ((100 - s_p - u_p) / (n - 1 if n > 1 else 1))
    for i in range(n):
        for j in range(n):
            if i == j: 
                seed[i,j] = u_p
            elif abs(i-j) == 2 or (n==4 and abs(i-j)==2): 
                seed[i,j] = s_p

    in_f = np.array(in_f, dtype=float)
    out_f = np.array(out_f, dtype=float)
    
    if in_f.sum() != out_f.sum():
        out_f = out_f * (in_f.sum() / out_f.sum())

    matrix = seed.copy()
    for _ in range(100):
        # Row Scaling
        r_sum = matrix.sum(axis=1)
        matrix = matrix * (in_f / np.where(r_sum==0, 1, r_sum))[:, np.newaxis]
        # Column Scaling
        c_sum = matrix.sum(axis=0)
        matrix = matrix * (out_f / np.where(c_sum==0, 1, c_sum))
        
    return pd.DataFrame(matrix, index=labels, columns=labels)

# --- Display ---
if st.button("คำนวณ Turning Movement"):
    df_result = estimate_tmc(inbound, outbound, legs, u_turn_pct, straight_pct)
    st.subheader("📊 ตารางปริมาณจราจรเลี้ยว (คัน/ชม.)")
    st.table(df_result.style.format("{:.0f}").highlight_max(axis=0))
    
    csv = df_result.to_csv().encode('utf-8-sig')
    st.download_button("📥 ดาวน์โหลดไฟล์ Excel (CSV)", csv, "Turning_Movement.csv", "text/csv")
else:
    st.info("กรอกข้อมูลในแถบด้านซ้ายแล้วกดคำนวณ")
