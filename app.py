import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(page_title="Intersection Diagram 100%", layout="wide")

# --- ส่วนของการคำนวณปริมาณจราจร ---
def calculate_matrix(inbound, outbound, labels, u_p, s_p):
    n = len(inbound)
    # ประมาณค่าสัดส่วน (Seed Matrix)
    seed = np.ones((n, n)) * ((100 - s_p - u_p) / (n - 1))
    for i in range(n):
        for j in range(n):
            if i == j: seed[i,j] = u_p  # U-Turn
            elif abs(i-j) == 2: seed[i,j] = s_p # ตรงไป
    
    in_v = np.array(inbound, dtype=float)
    out_v = np.array(outbound, dtype=float)
    
    # ปรับสมดุลเบื้องต้น
    if in_v.sum() > 0:
        out_v = out_v * (in_v.sum() / out_v.sum())
    
    # Fratar Method (Iteration)
    matrix = seed.copy()
    for _ in range(50):
        matrix = matrix * (in_v / np.where(matrix.sum(axis=1)==0, 1, matrix.sum(axis=1)))[:, np.newaxis]
        matrix = matrix * (out_v / np.where(matrix.sum(axis=0)==0, 1, matrix.sum(axis=0)))
    return pd.DataFrame(matrix, index=labels, columns=labels)

# --- Sidebar Inputs ---
with st.sidebar:
    st.header("📍 ข้อมูลทางแยก (PCU/Hr)")
    legs = ["North (N)", "South (S)", "East (E)", "West (W)"]
    in_v, out_v = [], []
    for leg in legs:
        st.subheader(f"ทิศ {leg}")
        c1, c2 = st.columns(2)
        v_in = c1.number_input(f"In", min_value=0, value=1000, key=f"in_{leg}")
        v_out = c2.number_input(f"Out", min_value=0, value=1000, key=f"out_{leg}")
        in_v.append(v_in)
        out_v.append(v_out)
    st.divider()
    u_p = st.slider("U-Turn (%)", 0, 15, 2)
    s_p = st.slider("ตรงไป (%)", 40, 95, 70)

# --- ประมวลผลข้อมูล ---
df = calculate_matrix(in_v, out_v, legs, u_p, s_p)
# สรุปค่ารายทิศ (L=Left, T=Through, R=Right, U=UTurn)
# อ้างอิง index: 0:N, 1:S, 2:E, 3:W
data = {
    "N": {"U": df.iloc[0,0], "T": df.iloc[0,1], "R": df.iloc[0,2], "L": df.iloc[0,3], "In": in_v[0], "Out": out_v[0]},
    "S": {"U": df.iloc[1,1], "T": df.iloc[1,0], "R": df.iloc[1,3], "L": df.iloc[1,2], "In": in_v[1], "Out": out_v[1]},
    "E": {"U": df.iloc[2,2], "T": df.iloc[2,3], "R": df.iloc[2,0], "L": df.iloc[2,1], "In": in_v[2], "Out": out_v[2]},
    "W": {"U": df.iloc[3,3], "T": df.iloc[3,2], "R": df.iloc[3,1], "L": df.iloc[3,0], "In": in_v[3], "Out": out_v[3]},
}

st.title("🏗️ Engineering Intersection Diagram")
st.write(f"**Year 2006 AM** | หน่วย: PCU/Hr.")

# --- ส่วนการวาดผังด้วย SVG ---
svg_code = f"""
<svg viewBox="0 0 800 800" xmlns="http://www.w3.org/2000/svg" style="background:#fff; border:1px solid #ddd;">
    <path d="M 300 0 L 300 300 L 0 300 M 0 500 L 300 500 L 300 800 M 500 800 L 500 500 L 800 500 M 800 300 L 500 300 L 500 0" 
          fill="none" stroke="black" stroke-width="3"/>
    
    <g transform="translate(650, 100)">
        <path d="M 0 -40 L 15 0 L 0 -10 L -15 0 Z" fill="none" stroke="black"/>
        <text x="0" y="-50" text-anchor="middle" font-weight="bold" font-size="20">N</text>
    </g>

    <text x="320" y="250" font-weight="bold" transform="rotate(-90, 320, 250)">ติวานนท์</text>
    <text x="550" y="285" font-weight="bold">งามวงศ์วาน</text>
    <text x="420" y="550" font-weight="bold" transform="rotate(90, 420, 550)">แคราย</text>

    <g transform="translate(300, 50)">
        <rect x="10" y="100" width="45" height="30" fill="white" stroke="black"/> <text x="32" y="120" text-anchor="middle" font-size="12">{data['N']['U']:.0f}</text>
        <rect x="55" y="100" width="45" height="30" fill="white" stroke="black"/> <text x="77" y="120" text-anchor="middle" font-size="12">{data['N']['T']:.0f}</text>
        <rect x="100" y="100" width="45" height="30" fill="white" stroke="black"/> <text x="122" y="120" text-anchor="middle" font-size="12">{data['N']['R']:.0f}</text>
        <path d="M 32 140 q 0 15 15 15" fill="none" stroke="black" stroke-width="2" marker-end="url(#arrow)"/> <path d="M 77 140 L 77 165" fill="none" stroke="black" stroke-width="2" marker-end="url(#arrow)"/> <path d="M 122 140 q 0 15 -15 15" fill="none" stroke="black" stroke-width="2" marker-end="url(#arrow)"/> <rect x="10" y="0" width="60" height="30" fill="none" stroke="black"/> <text x="40" y="20" text-anchor="middle" font-weight="bold">{data['N']['In']}</text>
        <rect x="100" y="0" width="60" height="30" fill="none" stroke="black"/> <text x="130" y="20" text-anchor="middle" font-weight="bold">{data['N']['Out']}</text>
    </g>

    <g transform="translate(300, 620)">
        <rect x="10" y="0" width="45" height="30" fill="white" stroke="black"/> <text x="32" y="20" text-anchor="middle" font-size="12">{data['S']['L']:.0f}</text>
        <rect x="55" y="0" width="45" height="30" fill="white" stroke="black"/> <text x="77" y="20" text-anchor="middle" font-size="12">{data['S']['T']:.0f}</text>
        <rect x="100" y="0" width="45" height="30" fill="white" stroke="black"/> <text x="122" y="20" text-anchor="middle" font-size="12">{data['S']['R']:.0f}</text>
        <path d="M 32 -10 q 0 -15 -15 -15" fill="none" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
        <path d="M 77 -10 L 77 -35" fill="none" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
        <path d="M 122 -10 q 0 -15 15 -15" fill="none" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
        <rect x="10" y="100" width="60" height="30" fill="none" stroke="black"/> <text x="40" y="120" text-anchor="middle" font-weight="bold">{data['S']['In']}</text>
        <rect x="100" y="100" width="60" height="30" fill="none" stroke="black"/> <text x="130" y="120" text-anchor="middle" font-weight="bold">{data['S']['Out']}</text>
    </g>

    <g transform="translate(50, 300)">
        <rect x="100" y="10" width="45" height="30" fill="white" stroke="black"/> <text x="122" y="30" text-anchor="middle" font-size="12">{data['W']['L']:.0f}</text>
        <rect x="100" y="55" width="45" height="30" fill="white" stroke="black"/> <text x="122" y="75" text-anchor="middle" font-size="12">{data['W']['T']:.0f}</text>
        <rect x="100" y="100" width="45" height="30" fill="white" stroke="black"/> <text x="122" y="120" text-anchor="middle" font-size="12">{data['W']['R']:.0f}</text>
        <path d="M 150 25 q 15 0 15 -15" fill="none" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
        <path d="M 150 70 L 175 70" fill="none" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
        <path d="M 150 115 q 15 0 15 15" fill="none" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
        <rect x="0" y="10" width="60" height="30" fill="none" stroke="black"/> <text x="30" y="30" text-anchor="middle" font-weight="bold">{data['W']['In']}</text>
        <rect x="0" y="100" width="60" height="30" fill="none" stroke="black"/> <text x="30" y="120" text-anchor="middle" font-weight="bold">{data['W']['Out']}</text>
    </g>

    <g transform="translate(620, 300)">
        <rect x="0" y="10" width="45" height="30" fill="white" stroke="black"/> <text x="22" y="30" text-anchor="middle" font-size="12">{data['E']['R']:.0f}</text>
        <rect x="0" y="55" width="45" height="30" fill="white" stroke="black"/> <text x="22" y="75" text-anchor="middle" font-size="12">{data['E']['T']:.0f}</text>
        <rect x="0" y="100" width="45" height="30" fill="white" stroke="black"/> <text x="22" y="120" text-anchor="middle" font-size="12">{data['E']['L']:.0f}</text>
        <path d="M -10 25 q -15 0 -15 15" fill="none" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
        <path d="M -10 70 L -35 70" fill="none" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
        <path d="M -10 115 q -15 0 -15 -15" fill="none" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
        <rect x="100" y="10" width="60" height="30" fill="none" stroke="black"/> <text x="130" y="30" text-anchor="middle" font-weight="bold">{data['E']['Out']}</text>
        <rect x="100" y="100" width="60" height="30" fill="none" stroke="black"/> <text x="130" y="120" text-anchor="middle" font-weight="bold">{data['E']['In']}</text>
    </g>

    <defs>
        <marker id="arrow" markerWidth="10" markerHeight="10" refX="5" refY="5" orient="auto">
            <path d="M 0 0 L 10 5 L 0 10 z" fill="black" />
        </marker>
    </defs>
</svg>
"""

# แสดงผลผังทางแยก
st.components.v1.html(svg_code, height=820)

# แสดงตารางข้อมูล Matrix เพื่อการตรวจสอบ
with st.expander("📊 ตาราง Matrix สรุปผล (Origin-Destination)"):
    st.dataframe(df.style.format("{:.0f}"))
