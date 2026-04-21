import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(page_title="Traffic Movement Diagram", layout="wide")

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
        in_v.append(c1.number_input(f"เข้า (In)", min_value=0, value=1000, key=f"i_{leg}"))
        out_v.append(c2.number_input(f"ออก (Out)", min_value=0, value=1000, key=f"o_{leg}"))
    u_p = st.slider("สัดส่วน U-Turn (%)", 0, 15, 2)
    s_p = st.slider("สัดส่วน ตรงไป (%)", 40, 95, 70)

# --- Calculation ---
df = calc_matrix(in_v, out_v, legs, u_p, s_p)
d = {
    "N": {"T": df.iloc[0,1], "R": df.iloc[0,2], "L": df.iloc[0,3], "U": df.iloc[0,0], "In": in_v[0], "Out": out_v[0]},
    "S": {"T": df.iloc[1,0], "R": df.iloc[1,3], "L": df.iloc[1,2], "U": df.iloc[1,1], "In": in_v[1], "Out": out_v[1]},
    "E": {"T": df.iloc[2,3], "R": df.iloc[2,0], "L": df.iloc[2,1], "U": df.iloc[2,2], "In": in_v[2], "Out": out_v[2]},
    "W": {"T": df.iloc[3,2], "R": df.iloc[3,1], "L": df.iloc[3,0], "U": df.iloc[3,3], "In": in_v[3], "Out": out_v[3]},
}

st.title("📍 Turning Movement Diagram (Year 2026)")

# --- SVG Drawing: High Visibility Mode ---
svg = f"""
<svg viewBox="0 0 800 800" xmlns="http://www.w3.org/2000/svg" style="background:#fff; border:1px solid #eee; display:block; margin:auto;">
    <rect x="330" y="0" width="140" height="800" fill="#fcfcfc" />
    <rect x="0" y="330" width="800" height="140" fill="#fcfcfc" />
    <path d="M 330 0 v 330 h -330 M 0 470 h 330 v 330 M 470 800 v -330 h 330 M 800 330 h -330 v -330" fill="none" stroke="#444" stroke-width="3"/>
    
    <text x="740" y="50" font-size="20" font-weight="bold">N ▲</text>

    <g transform="translate(335, 20)">
        <text x="65" y="20" text-anchor="middle" font-size="24" font-weight="bold" fill="#1565C0">ติวานนท์</text>
        <rect x="0" y="40" width="60" height="35" fill="#E3F2FD" stroke="black"/> <text x="30" y="65" text-anchor="middle" font-size="18" font-weight="bold">{d['N']['In']}</text>
        <rect x="70" y="40" width="60" height="35" fill="white" stroke="black"/> <text x="100" y="65" text-anchor="middle" font-size="18">{d['N']['Out']}</text>
        <text x="5" y="280" font-size="16" font-weight="bold">↶ {d['N']['U']:.0f}</text>
        <text x="5" y="305" font-size="16" font-weight="bold">↓ {d['N']['T']:.0f}</text>
        <text x="50" y="305" font-size="16" font-weight="bold">→ {d['N']['R']:.0f}</text>
        <text x="95" y="305" font-size="16" font-weight="bold">← {d['N']['L']:.0f}</text>
    </g>

    <g transform="translate(335, 485)">
        <text x="65" y="290" text-anchor="middle" font-size="24" font-weight="bold" fill="#1565C0">แคราย</text>
        <rect x="0" y="235" width="60" height="35" fill="white" stroke="black"/> <text x="30" y="260" text-anchor="middle" font-size="18">{d['S']['Out']}</text>
        <rect x="70" y="235" width="60" height="35" fill="#E3F2FD" stroke="black"/> <text x="100" y="260" text-anchor="middle" font-size="18" font-weight="bold">{d['S']['In']}</text>
        <text x="75" y="45" font-size="16" font-weight="bold">← {d['S']['L']:.0f}</text>
        <text x="75" y="20" font-size="16" font-weight="bold">↑ {d['S']['T']:.0f}</text>
        <text x="120" y="20" font-size="16" font-weight="bold">↶ {d['S']['U']:.0f}</text>
        <text x="30" y="20" font-size="16" font-weight="bold">→ {d['S']['R']:.0f}</text>
    </g>

    <g transform="translate(20, 335)">
        <rect x="10" y="0" width="65" height="35" fill="#E3F2FD" stroke="black"/> <text x="42" y="25" text-anchor="middle" font-size="18" font-weight="bold">{d['W']['In']}</text>
        <rect x="10" y="95" width="65" height="35" fill="white" stroke="black"/> <text x="42" y="120" text-anchor="middle" font-size="18">{d['W']['Out']}</text>
        <text x="245" y="25" font-size="16" font-weight="bold">← {d['W']['L']:.0f}</text>
        <text x="245" y="70" font-size="16" font-weight="bold">→ {d['W']['T']:.0f}</text>
        <text x="245" y="115" font-size="16" font-weight="bold">↓ {d['W']['R']:.0f}</text>
    </g>

    <g transform="translate(530, 335)">
        <text x="135" y="-15" text-anchor="middle" font-size="24" font-weight="bold" fill="#1565C0">งามวงศ์วาน</text>
        <rect x="195" y="0" width="65" height="35" fill="white" stroke="black"/> <text x="227" y="25" text-anchor="middle" font-size="18">{d['E']['Out']}</text>
        <rect x="195" y="95" width="65" height="35" fill="#E3F2FD" stroke="black"/> <text x="227" y="120" text-anchor="middle" font-size="18" font-weight="bold">{d['E']['In']}</text>
        <text x="15" y="25" font-size="16" font-weight="bold">→ {d['E']['R']:.0f}</text>
        <text x="15" y="70" font-size="16" font-weight="bold">← {d['E']['T']:.0f}</text>
        <text x="15" y="115" font-size="16" font-weight="bold">↓ {d['E']['L']:.0f}</text>
    </g>
</svg>
"""

st.components.v1.html(svg, height=820)
st.info("💡 ข้อมูลในผังใช้หน่วย PCU/Hr | สีฟ้า = ขาเข้า (Inbound), สีขาว = ขาออก (Outbound)")
