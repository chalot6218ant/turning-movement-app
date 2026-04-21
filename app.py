import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(page_title="Turning Movement Diagram", layout="wide")

# --- Custom CSS เพื่อจัดวางตำแหน่งตัวเลขให้เหมือนผังทางแยก ---
st.markdown("""
    <style>
    .intersection-container {
        position: relative;
        width: 100%;
        max-width: 800px;
        margin: auto;
        background-color: white;
        padding: 20px;
    }
    .approach-box {
        border: 1px solid #000;
        padding: 5px;
        text-align: center;
        background-color: #fff;
        min-width: 120px;
        display: inline-block;
    }
    .lane-box {
        border: 1px solid #ccc;
        width: 40px;
        height: 50px;
        display: inline-block;
        vertical-align: top;
        font-size: 14px;
        font-weight: bold;
        line-height: 1.2;
        padding-top: 5px;
    }
    .total-in-out {
        font-size: 16px;
        font-weight: bold;
        margin-top: 5px;
    }
    .road-label {
        font-weight: bold;
        color: #333;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 Turning Movement Diagram (Year 2006 AM)")
st.write("หน่วย: PCU/Hr.")

# --- 1. Sidebar ---
with st.sidebar:
    st.header("📍 ตั้งค่าปริมาณจราจร")
    legs = ["North (N)", "South (S)", "East (E)", "West (W)"]
    inbound, outbound = [], []
    for leg in legs:
        st.subheader(f"ทิศ {leg}")
        c1, c2 = st.columns(2)
        v_in = c1.number_input(f"In", min_value=0, value=1000, key=f"in_{leg}")
        v_out = c2.number_input(f"Out", min_value=0, value=1000, key=f"out_{leg}")
        inbound.append(v_in)
        outbound.append(v_out)

    u_pct = st.slider("U-Turn (%)", 0, 20, 2)
    s_pct = st.slider("ตรงไป (%)", 40, 90, 70)

# --- 2. Logic ---
def calculate_matrix(in_f, out_f, labels, u_p, s_p):
    n = len(in_f)
    seed = np.ones((n, n)) * ((100 - s_p - u_p) / (n - 1 if n > 1 else 1))
    for i in range(n):
        for j in range(n):
            if i == j: seed[i,j] = u_p
            elif abs(i-j) == 2: seed[i,j] = s_p
    in_f, out_f = np.array(in_f, dtype=float), np.array(out_f, dtype=float)
    if in_f.sum() > 0: out_f = out_f * (in_f.sum() / out_f.sum())
    matrix = seed.copy()
    for _ in range(50):
        matrix = matrix * (in_f / np.where(matrix.sum(axis=1)==0, 1, matrix.sum(axis=1)))[:, np.newaxis]
        matrix = matrix * (out_f / np.where(matrix.sum(axis=0)==0, 1, matrix.sum(axis=0)))
    return pd.DataFrame(matrix, index=labels, columns=labels)

# --- 3. UI Helper Function ---
def lane_html(val, arrow_type):
    return f"<div class='lane-box'>{val:.0f}<br>{arrow_type}</div>"

# --- 4. Main Display ---
if st.button("🚀 สร้างผังทางแยก"):
    df = calculate_matrix(inbound, outbound, legs, u_pct, s_pct)
    
    # ดึงค่าตามรายขา
    N = df.loc["North (N)"]
    S = df.loc["South (S)"]
    E = df.loc["East (E)"]
    W = df.loc["West (W)"]

    st.markdown("<div class='intersection-container'>", unsafe_allow_html=True)
    
    # --- ทิศ North (ติวานนท์) ---
    c1, c2, c3 = st.columns([1, 1, 1])
    with c2:
        st.markdown(f"<div class='road-label'>ติวานนท์</div>", unsafe_allow_html=True)
        st.markdown(f"{lane_html(N.iloc[0], '↶')}{lane_html(N.iloc[1], '↓')}{lane_html(N.iloc[2], '↷')}", unsafe_allow_html=True)
        st.markdown(f"<div class='total-in-out'>{inbound[0]:.0f} | {outbound[0]:.0f}</div>", unsafe_allow_html=True)

    # --- ทิศ West และ East (งามวงศ์วาน) ---
    c1, c2, c3 = st.columns([1, 1, 1])
    with c1:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown(f"<div class='total-in-out'>{inbound[3]:.0f} | {outbound[3]:.0f}</div>", unsafe_allow_html=True)
        st.markdown(f"{lane_html(W.iloc[0], '↶')}{lane_html(W.iloc[1], '→')}{lane_html(W.iloc[2], '↷')}", unsafe_allow_html=True)
    
    with c2:
        st.markdown("<center><br><br><b>N</b><br>▲<br>|</center>", unsafe_allow_html=True)

    with c3:
        st.markdown("<br><br><b>งามวงศ์วาน</b>", unsafe_allow_html=True)
        st.markdown(f"{lane_html(E.iloc[0], '↶')}{lane_html(E.iloc[1], '←')}{lane_html(E.iloc[2], '↷')}", unsafe_allow_html=True)
        st.markdown(f"<div class='total-in-out'>{inbound[2]:.0f} | {outbound[2]:.0f}</div>", unsafe_allow_html=True)

    # --- ทิศ South ---
    c1, c2, c3 = st.columns([1, 1, 1])
    with c2:
        st.markdown(f"<div class='total-in-out'>{inbound[1]:.0f} | {outbound[1]:.0f}</div>", unsafe_allow_html=True)
        st.markdown(f"{lane_html(S.iloc[0], '↶')}{lane_html(S.iloc[1], '↑')}{lane_html(S.iloc[2], '↷')}", unsafe_allow_html=True)
        st.markdown("<b>แคราย</b>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
    
    with st.expander("📝 ดูตาราง Matrix สรุป"):
        st.dataframe(df.style.format("{:.0f}"))
else:
    st.info("กรุณากรอกข้อมูลที่แถบด้านซ้าย แล้วกดปุ่ม 'สร้างผังทางแยก'")
