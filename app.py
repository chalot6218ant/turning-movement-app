import streamlit as st
import numpy as np
import pandas as pd

# ตั้งค่าหน้าจอแบบกว้าง
st.set_page_config(page_title="Turning Movement Analysis", layout="wide")

st.title("📊 Turning Movement Analysis (Estimation)")
st.write("โปรแกรมคำนวณปริมาณจราจรเลี้ยวแยกตามทิศทางและรองรับ U-Turn")

# --- ส่วนรับข้อมูล (Sidebar) ---
with st.sidebar:
    st.header("📍 ตั้งค่าทางแยก")
    j_type = st.radio("ประเภททางแยก", ["4 แยก", "3 แยก"])
    
    # กำหนดทิศทาง
    if j_type == "4 แยก":
        legs = ["North (N)", "South (S)", "East (E)", "West (W)"]
    else:
        legs = ["North (N)", "South (S)", "East (E)"]
    
    st.header("🚗 ข้อมูล Midblock Volume")
    inbound = []
    outbound = []
    for leg in legs:
        st.subheader(f"ทิศ {leg}")
        c1, c2 = st.columns(2)
        with c1:
            v_in = st.number_input(f"ขาเข้า (In)", min_value=0, value=1000, key=f"i_{leg}")
        with c2:
            v_out = st.number_input(f"ขาออก (Out)", min_value=0, value=1000, key=f"o_{leg}")
        inbound.append(v_in)
        outbound.append(v_out)

    st.header("⚙️ สมมติฐานสัดส่วน")
    u_pct = st.slider("สัดส่วน U-Turn (%)", 0, 20, 2)
    s_pct = st.slider("สัดส่วน ตรงไป (%)", 40, 90, 70)

# --- ส่วนคำนวณ (Logic) ---
def calculate_tmc(in_f, out_f, labels, u_p, s_p):
    n = len(in_f)
    # สร้าง Seed Matrix
    seed = np.ones((n, n)) * ((100 - s_p - u_p) / (n - 1 if n > 1 else 1))
    for i in range(n):
        for j in range(n):
            if i == j: seed[i,j] = u_p
            elif abs(i-j) == 2 or (n==4 and abs(i-j)==2): seed[i,j] = s_p

    in_f, out_f = np.array(in_f, dtype=float), np.array(out_f, dtype=float)
    if in_f.sum() != out_f.sum():
        out_f = out_f * (in_f.sum() / out_f.sum())

    matrix = seed.copy()
    for _ in range(100):
        matrix = matrix * (in_f / np.where(matrix.sum(axis=1)==0, 1, matrix.sum(axis=1)))[:, np.newaxis]
        matrix = matrix * (out_f / np.where(matrix.sum(axis=0)==0, 1, matrix.sum(axis=0)))
    return pd.DataFrame(matrix, index=labels, columns=labels)

# --- ส่วนแสดงผลหน้าแรก (Main UI) ---
if st.button("เริ่มคำนวณและแสดงผล"):
    df = calculate_tmc(inbound, outbound, legs, u_pct, s_pct)
    
    st.divider()
    st.subheader("✅ ผลการคำนวณแยกตามรายขาเข้า (Inbound Approach)")

    # วนลูปแสดงผลทีละทิศทางให้เหมือนในรูปตัวอย่าง
    for i, origin in enumerate(legs):
        with st.container():
            st.markdown(f"#### 📍 จากทิศทาง: **{origin}**")
            
            # สร้างคอลัมน์ย่อยสำหรับแต่ละทิศทางการไป
            cols = st.columns(len(legs) + 1) # +1 สำหรับ Total
            
            total_in = 0
            for j, destination in enumerate(legs):
                val = df.iloc[i, j]
                total_in += val
                with cols[j]:
                    label = "U-Turn" if origin == destination else f"ไป {destination}"
                    st.metric(label, f"{val:.0f}")
            
            with cols[-1]:
                st.metric("รวมขาเข้า (Total)", f"{total_in:.0f}", delta_color="off")
            st.divider()

    # แสดงตาราง Matrix รวมด้านล่าง
    with st.expander("ดูตาราง Matrix ทั้งหมด (Summary Matrix)"):
        st.dataframe(df.style.format("{:.0f}").highlight_max(axis=1, color="#D4E6F1"))
        
    csv = df.to_csv().encode('utf-8-sig')
    st.download_button("📥 ดาวน์โหลดข้อมูล (CSV)", csv, "turning_data.csv", "text/csv")

else:
    st.info("กรุณากรอกข้อมูลที่แถบด้านซ้าย แล้วกดปุ่ม 'เริ่มคำนวณและแสดงผล'")
