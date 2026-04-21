import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(page_title="Turning Movement Diagram", layout="wide")

# --- Custom CSS เพื่อจัดหน้าตาให้เหมือนผังทางแยก ---
st.markdown("""
    <style>
    .approach-box {
        border: 2px solid #333;
        padding: 10px;
        text-align: center;
        background-color: #f9f9f9;
        border-radius: 5px;
    }
    .lane-value {
        font-size: 20px;
        font-weight: bold;
        color: #1E88E5;
    }
    .total-box {
        background-color: #eee;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🚗 Turning Movement Estimation (PCU/Hr)")

# --- 1. Sidebar: Input Data ---
with st.sidebar:
    st.header("📍 ตั้งค่าทางแยก")
    # กำหนดทิศทางมาตรฐาน 4 ทิศ (ติวานนท์ - งามวงศ์วาน)
    legs = ["North (N)", "South (S)", "East (E)", "West (W)"]
    
    inbound, outbound = [], []
    for leg in legs:
        st.subheader(f"ทิศ {leg}")
        c1, c2 = st.columns(2)
        v_in = c1.number_input(f"ขาเข้า (In)", min_value=0, value=1000, key=f"in_{leg}")
        v_out = c2.number_input(f"ขาออก (Out)", min_value=0, value=1000, key=f"out_{leg}")
        inbound.append(v_in)
        outbound.append(v_out)

    st.header("⚙️ สมมติฐานสัดส่วน")
    u_pct = st.slider("U-Turn (%)", 0, 20, 2)
    s_pct = st.slider("ตรงไป (%)", 40, 90, 70)

# --- 2. Calculation Logic ---
def calculate_matrix(in_f, out_f, labels, u_p, s_p):
    n = len(in_f)
    seed = np.ones((n, n)) * ((100 - s_p - u_p) / (n - 1 if n > 1 else 1))
    for i in range(n):
        for j in range(n):
            if i == j: seed[i,j] = u_p
            elif abs(i-j) == 2: seed[i,j] = s_p
    
    in_f, out_f = np.array(in_f, dtype=float), np.array(out_f, dtype=float)
    if in_f.sum() > 0:
        out_f = out_f * (in_f.sum() / out_f.sum())

    matrix = seed.copy()
    for _ in range(100):
        matrix = matrix * (in_f / np.where(matrix.sum(axis=1)==0, 1, matrix.sum(axis=1)))[:, np.newaxis]
        matrix = matrix * (out_f / np.where(matrix.sum(axis=0)==0, 1, matrix.sum(axis=0)))
    return pd.DataFrame(matrix, index=labels, columns=labels)

# --- 3. Main Display: ผังทางแยก (Visual Diagram) ---
if st.button("🚀 ประมวลผลและสร้างผังทางแยก"):
    df = calculate_matrix(inbound, outbound, legs, u_pct, s_pct)
    
    # ดึงค่ามาเตรียมแสดงผล
    N = df.loc["North (N)"]
    S = df.loc["South (S)"]
    E = df.loc["East (E)"]
    W = df.loc["West (W)"]

    st.divider()
    
    # การจัด Layout แบบ Grid 3x3 เพื่อจำลองทางแยก
    row1_left, row1_center, row1_right = st.columns([1, 1, 1])
    row2_left, row2_center, row2_right = st.columns([1, 1, 1])
    row3_left, row3_center, row3_right = st.columns([1, 1, 1])

    # --- แถวบน: ทิศ North ---
    with row1_center:
        st.markdown(f"""
            <div class='approach-box'>
                <b>North (ติวานนท์)</b><br>
                <small>เข้าแยก 👇</small><br>
                <span class='lane-value'>{N["South (S)"]:.0f} | {N["East (E)"]:.0f} | {N["West (W)"]:.0f}</span><br>
                <div class='total-box'>Total In: {inbound[0]:.0f}</div>
            </div>
        """, unsafe_allow_html=True)

    # --- แถวกลาง: West, ทางแยก, East ---
    with row2_left:
        st.markdown(f"""
            <div class='approach-box'>
                <b>West (ขาเข้า)</b><br>
                <small>👉 เข้าแยก</small><br>
                <span class='lane-value'>{W["East (E)"]:.0f}<br>{W["North (N)"]:.0f}<br>{W["South (S)"]:.0f}</span><br>
                <div class='total-box'>Total In: {inbound[3]:.0f}</div>
            </div>
        """, unsafe_allow_html=True)

    with row2_center:
        st.write("")
        st.image("https://cdn-icons-png.flaticon.com/512/484/484167.png", width=100) # รูปไอคอนสี่แยก
        st.markdown("<center><b>INTERSECTION</b></center>", unsafe_allow_html=True)

    with row2_right:
        st.markdown(f"""
            <div class='approach-box'>
                <b>East (งามวงศ์วาน)</b><br>
                <small>👈 เข้าแยก</small><br>
                <span class='lane-value'>{E["West (W)"]:.0f}<br>{E["North (N)"]:.0f}<br>{E["South (S)"]:.0f}</span><br>
                <div class='total-box'>Total In: {inbound[2]:.0f}</div>
            </div>
        """, unsafe_allow_html=True)

    # --- แถวล่าง: ทิศ South ---
    with row3_center:
        st.markdown(f"""
            <div class='approach-box'>
                <div class='total-box'>Total In: {inbound[1]:.0f}</div>
                <span class='lane-value'>{S["North (N)"]:.0f} | {S["East (E)"]:.0f} | {S["West (W)"]:.0f}</span><br>
                <small>👆 เข้าแยก</small><br>
                <b>South (ขาเข้า)</b>
            </div>
        """, unsafe_allow_html=True)

    st.divider()
    
    # แสดงตาราง Matrix สรุปด้านล่าง
    st.subheader("📝 Summary Matrix (PCU/Hr)")
    matrix_final = df.copy()
    matrix_final["Total Out"] = matrix_final.sum(axis=1)
    st.dataframe(matrix_final.style.format("{:.0f}"))

    csv = matrix_final.to_csv().encode('utf-8-sig')
    st.download_button("📥 Download Data", csv, "turning_movement.csv")

else:
    st.info("กรุณากรอกปริมาณจราจร In/Out ที่แถบด้านซ้าย แล้วกดปุ่มคำนวณ")
