import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(page_title="Clear Traffic Movement Diagram", layout="wide")

# --- Traffic Logic: Fratar Method ---
def calc_matrix(inbound, outbound, labels, up, sp):
    n = len(inbound)
    seed = np.ones((n, n)) * ((100 - sp - up) / (n - 1))
    for i in range(n):
        for j in range(n):
            if i == j: seed[i,j] = up
            elif abs(i-j) == 2: seed[i,j] = sp
    in_v, out_v = np.array(inbound, dtype=float), np.array(outbound, dtype=float)
    if in_v.sum() > 0: out_v = out_v * (in_v.sum() / out_v.sum())
    m = seed.copy()
    for _ in range(50):
        m = m * (in_v / np.where(m.sum(axis=1)==0, 1, m.sum(axis=1)))[:, np.newaxis]
        m = m * (out_v / np.where(m.sum(axis=0)==0, 1, m.sum(axis=0)))
    return pd.DataFrame(m, index=labels, columns=labels)

# --- Sidebar Inputs ---
with st.sidebar:
    st.header("🚦 ข้อมูลปริมาณจราจร (PCU/Hr)")
    legs = ["North (N)", "South (S)", "East (E)", "West (W)"]
    in_v, out_v = [], []
    for leg in legs:
        st.subheader(f"ทิศ {leg}")
        c1, c2 = st.columns(2)
        in_v.append(c1.number_input(f"เข้า", min_value=0, value=1000, key=f"in_{leg}"))
        out_v.append(c2.number_input(f"ออก", min_value=0, value=1000, key=f"out_{leg}"))
    u_p = st.slider("U-Turn (%)", 0, 15, 2)
    s_p = st.slider("ตรงไป (%)", 40, 95, 70)

# --- Calculation ---
df = calc_matrix(in_v, out_v, legs, u_p, s_p)
d = {
    "N": {"T": df.iloc[0,1], "R": df.iloc[0,2], "L": df.iloc[0,3], "U": df.iloc[0,0], "In": in_v[0], "Out": out_v[0]},
    "S": {"T": df.iloc[1,0], "R": df.iloc[1,3], "L": df.iloc[1,2], "U": df.iloc[1,1], "In": in_v[1], "Out": out_v[1]},
    "E": {"T": df.iloc[2,3], "R": df.iloc[2,0], "L": df.iloc[2,1], "U": df.iloc[2,2], "In": in_v[2], "Out": out_v[2]},
    "W": {"T": df.iloc[3,2], "R": df.iloc[3,1], "L": df.iloc[3,0], "U": df.iloc[3,3], "In": in_v[3], "Out": out_v[3]},
}

st.title("🚦 Turning Movement Diagram (Readable Version)")

# --- SVG Drawing: เน้นความใหญ่และอ่านง่ายที่สุด ---
svg = f"""
<svg viewBox="0 0 1000 1000" xmlns="http://www.w3.org/2000/svg" style="background:#ffffff; border:1px solid #ccc; display:block; margin:auto;">
    <path d="M 400 0 v 400 h -400 M 0 600 h 400 v 400 M 600 1000 v -400 h 400 M 1000 400 h -400 v -400" 
          fill="none" stroke="#333" stroke-width="4"/>
    
    <text x="920" y="80" font-size="25" font-weight="bold">N ▲</text>

    <g transform="translate(410, 30)">
        <text x="90" y="20" text-anchor="middle" font-size="28" font-weight="bold" fill="darkblue">ติวานนท์</text>
        <rect x="0" y="40" width="85" height="45" fill="#E3F2FD" stroke="black" stroke-width="2"/> <text x="42" y="72" text-anchor="middle" font-size="22" font-weight="bold">{d['N']['In']}</text>
        <rect x="95" y="40" width="85" height="45" fill="white" stroke="black" stroke-width="2"/> <text x="137" y="72" text-anchor="middle" font-size="22">{d['N']['Out']}</text>
        <g transform="translate(0, 310)" font-size="18" font-weight="bold">
            <text x="5" y="0">↶ {d['N']['U']:.0f}</text>
            <text x="5" y="30">↓ {d['N']['T']:.0f}</text>
            <text x="65" y="30">→ {d['N']['R']:.0f}</text>
            <text x="125" y="30">← {d['N']['L']:.0f}</text>
        </g>
    </g>

    <g transform="translate(410, 620)">
        <text x="90" y="350" text-anchor="middle" font-size="28" font-weight="bold" fill="darkblue">แคราย</text>
        <rect x="0" y="280" width="85" height="45" fill="white" stroke="black" stroke-width="2"/> <text x="42" y="312" text-anchor="middle" font-size="22">{d['S']['Out']}</text>
        <rect x="95" y="280" width="85" height="45" fill="#E3F2FD" stroke="black" stroke-width="2"/> <text x="137" y="312" text-anchor="middle" font-size="22" font-weight="bold">{d['S']['In']}</text>
        <g transform="translate(0, -10)" font-size="18" font-weight="bold">
            <text x="130" y="0">↶ {d['S']['U']:.0f}</text>
            <text x="95" y="-30">↑ {d['S']['T']:.0f}</text>
            <text x="40" y="-30">→ {d['S']['R']:.0f}</text>
            <text x="5" y="-10">← {d['S']['L']:.0f}</text>
        </g>
    </g>

    <g transform="translate(30, 410)">
        <rect x="0" y="0" width="85" height="45" fill="#E3F2FD" stroke="black" stroke-width="2"/> <text x="42" y="32" text-anchor="middle" font-size="22" font-weight="bold">{d['W']['In']}</text>
        <rect x="0" y="135" width="85" height="45" fill="white" stroke="black" stroke-width="2"/> <text x="42" y="167" text-anchor="middle" font-size="22">{d['W']['Out']}</text>
        <g transform="translate(320, 0)" font-size="18" font-weight="bold">
            <text x="0" y="32">← {d['W']['L']:.0f}</text>
            <text x="0" y="92">→ {d['W']['T']:.0f}</text>
            <text x="0" y="152">↓ {d['W']['R']:.0f}</text>
        </g>
    </g>

    <g transform="translate(710, 410)">
        <text x="180" y="-20" text-anchor="middle" font-size="28" font-weight="bold" fill="darkblue">งามวงศ์วาน</text>
        <rect x="195" y="0" width="85" height="45" fill="white" stroke="black" stroke-width="2"/> <text x="237" y="32" text-anchor="middle" font-size="22">{d['E']['Out']}</text>
        <rect x="195" y="135" width="85" height="45" fill="#E3F2FD" stroke="black" stroke-width="2"/> <text x="237" y="167" text-anchor="middle" font-size="22" font-weight="bold">{d['E']['In']}</text>
        <g transform="translate(-100, 0)" font-size="18" font-weight="bold" text-anchor="end">
            <text x="90" y="32">→ {d['E']['R']:.0f}</text>
            <text x="90" y="92">← {d['E']['T']:.0f}</text>
            <text x="90" y="152">↓ {d['E']['L']:.0f}</text>
        </g>
    </g>
</svg>
"""

st.components.v1.html(svg, height=1020)
st.info("💡 ผังจราจรแบบขยายขนาด: สีฟ้า = ขาเข้า (Inbound), สีขาว = ขาออก (Outbound)")
