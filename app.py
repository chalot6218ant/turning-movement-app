import streamlit as st
import numpy as np
import pandas as pd

# ตั้งค่าหน้าจอแบบกว้าง
st.set_page_config(page_title="Traffic Turning Movement", layout="wide")

# --- CSS สำหรับตกแต่ง Card และลูกศรให้ดูเป็นมืออาชีพ ---
st.markdown("""
    <style>
    .approach-card {
        border: 2px solid #e0e0e0;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 25px;
        background-color: #ffffff;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
    }
    .approach-header {
        background-color: #2e7d32; /* สีเขียวเข้ม */
        color: white;
        padding: 8px 18px;
        border-radius: 8px;
        font-weight: bold;
        font-size: 1.1rem;
        margin-bottom: 15px;
        display: inline-block;
    }
    .movement-item {
        text-align: center;
        padding: 10px;
        border: 1px solid #f0f0f0;
        border-radius: 8px;
        background-color: #fafafa;
    }
    .arrow-label {
        font-size: 14px;
        color: #616161;
        margin-bottom: 5px;
    }
    .pcu-value {
        font-size: 26px;
        font-weight: bold;
        color: #1565c0;
    }
    .pcu-unit {
        font-size: 12px;
        color: #9e9e9e;
        font-weight: normal;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🚦 Turning Movement Estimation (PCU/Hr)")

# --- 1. Sidebar สำหรับกรอกข้อมูล ---
with st.sidebar:
    st.header("📍 ข้อมูลทางแยก (Midblock)")
    legs = ["North (N)", "South (S)", "East (E)", "West (W)"]
    inbound, outbound = [], []
    for leg in legs:
        st.subheader(f"ทิศ {leg}")
        c1, c2 = st.columns(2)
        v_in = c1.number_input(f"เข้า", min_value=0, value=1000, key=f"in_{leg}")
        v_out = c2.number_input(f"ออก", min_value=0, value=1000, key=f"out_{leg}")
        inbound.append(v_in)
        outbound.append(v_out)

    st.header("⚙️ สมมติฐานสัดส่วน")
    u_pct = st.slider("สัดส่วน U-Turn (%)", 0, 20, 2)
    s_pct = st.slider("สัดส่วน ตรงไป (%)", 40, 90, 70)

# --- 2. การคำนวณ (Logic) ---
def calculate_traffic(in_v, out_v, labels, u_p, s_p):
    n = len(in_v)
    seed = np.ones((n, n)) * ((100 - s_p - u_p) / (n - 1 if n > 1 else 1))
    for i in range(n):
        for j in range(n):
            if i == j: seed[i,j] = u_p
            elif abs(i-j) == 2: seed[i,j] = s_p
    
    in_v, out_v = np.array(in_v, dtype=float), np.array(out_v, dtype=float)
    if in_v.sum() > 0:
        out_v = out_v * (in_v.sum() / out_v.sum())

    matrix = seed.copy()
    for _ in range(50):
        matrix = matrix * (in_v / np.where(matrix.sum(axis=1)==0, 1, matrix.sum(axis=1)))[:, np.newaxis]
        matrix = matrix * (out_v / np.where(matrix.sum(axis=0)==0, 1, matrix.sum(axis=0)))
    return pd.DataFrame(matrix, index=labels, columns=labels)

# --- 3. การแสดงผล (Main UI) ---
if st.button("🚀 ประมวลผลและสร้างผังลูกศร"):
    df = calculate_traffic(inbound, outbound, legs, u_pct, s_pct)
    
    st.subheader("✅ ผลการประมาณค่าปริมาณจราจรเลี้ยว (แยกตามรายขาเข้า)")

    for i, origin in enumerate(legs):
        # สร้าง Card สำหรับแต่ละ Approach
        st.markdown(f"""
            <div class='approach-card'>
                <div class='approach-header'>📍 ขาเข้าจากทิศ: {origin}</div>
        """, unsafe_allow_html=True)
        
        # เตรียมทิศทางลูกศร
        cols = st.columns(len(legs) + 1)
        
        total_in_check = 0
        for j, dest in enumerate(legs):
            val = df.iloc[i, j]
            total_in_check += val
            
            # กำหนดสัญลักษณ์ลูกศร
            if i == j: 
                label = "↪️ U-Turn"
            elif abs(i-j) == 2: 
                label = "⬆️ ตรงไป"
            elif (i==0 and j==3) or (i==1 and j==2) or (i==2 and j==0) or (i==3 and j==1):
                label = "⬅️ เลี้ยวซ้าย"
            else:
                label = "➡️ เลี้ยวขวา"

            with cols[j]:
                st.markdown(f"""
                    <div class='movement-item'>
                        <div class='arrow-label'>{label}</div>
                        <div class='pcu-value'>{val:.0f}</div>
                        <div class='pcu-unit'>PCU/Hr</div>
                    </div>
                """, unsafe_allow_html=True)
        
        # ช่องรวมท้าย Card
        with cols[-1]:
            st.markdown(f"""
                <div class='movement-item' style='background-color: #eeeeee;'>
                    <div class='arrow-label'>📊 รวมขาเข้า</div>
                    <div class='pcu-value' style='color: #333;'>{total_in_check:.0f}</div>
                    <div class='pcu-unit'>PCU/Hr</div>
                </div>
            """, unsafe_allow_html=True)
            
        st.markdown("</div>", unsafe_allow_html=True) # ปิด div approach-card

    # สรุปตาราง Matrix ไว้ใน Expander
    with st.expander("📝 ดูตาราง Matrix สรุปผล"):
        st.dataframe(df.style.format("{:.0f}"))

else:
    st.info("กรุณากรอกข้อมูลปริมาณจราจรที่แถบด้านซ้าย แล้วกดปุ่มคำนวณด้านบน")
