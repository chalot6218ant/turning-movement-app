import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(page_title="Compact Traffic Diagram", layout="wide")

# --- Traffic Logic ---
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

# --- Sidebar ---
with st.sidebar:
    st.header("🚦 ข้อมูลจราจร (PCU/Hr)")
    legs = ["North (N)", "South (S)", "East (E)", "West (W)"]
    in_v, out_v = [], []
    for leg in legs:
        st.subheader(f"ทิศ {leg}")
        c1, c2 = st.columns(2)
        in_v.append(c1.number_input(f"In", min_value=0, value=1000, key=f"i_{leg}"))
        out_v.append(c2.number_input(f"Out", min_value=0, value=1000, key=f"o_{leg}"))
    u_p, s_p = st.slider("U-Turn %", 0, 15, 2), st.slider("Straight %", 40, 95, 70)

df = calc_matrix(in_v, out_v, legs, u_p, s_p)
# Mapping for Diagram (L=Left, T=Through, R=Right)
d = {
    "N": {"T": df.iloc[0,1], "R": df.iloc[0,2], "L": df.iloc[0,3], "In": in_v[0], "Out": out_v[0]},
    "S": {"T": df.iloc[1,0], "R": df.iloc[1,3], "L": df.iloc[1,2], "In": in_v[1], "Out": out_v[1]},
    "E": {"T": df.iloc[2,3], "R": df.iloc[2,0], "L": df.iloc[2,1], "In": in_v[2], "Out": out_v[2]},
    "W": {"T": df.iloc[3,2], "R": df.iloc[3,1], "L": df.iloc[3,0], "In": in_v[3], "Out": out_v[3]},
}

st.title("📍 Traffic Movement Diagram (Compact & Correct Flow)")

# --- SVG Drawing (ปรับขนาดให้เล็กลง และแยกฝั่ง In/Out ให้ถูกต้องตามเลนไทย) ---
svg = f"""
<svg viewBox="0 0 500 500" xmlns="http://www.w3.org/2000/svg" style="background:#fff; display:block; margin:auto; border:1px solid #ddd;">
    <path d="M 200 0 v 200 h -200 M 0 300 h 200 v 200 M 300 500 v -200 h 200 M 500 200 h -200 v -200" fill="none" stroke="#333" stroke-width="2"/>
    
    <text x="450" y="40" font-size="12" font-weight="bold">N ▲</text>

    <g transform="translate(200, 10)">
        <text x="50" y="15" text-anchor="middle" font-size="11" font-weight="bold">ติวานนท์</text>
        <rect x="5" y="25" width="40" height="18" fill="#f0f0f0" stroke="black"/> <text x="25" y="38" text-anchor="middle" font-size="9">{d['N']['In']}</text>
        <rect x="55" y="25" width="40" height="18" fill="white" stroke="black"/> <text x="75" y="38" text-anchor="middle" font-size="9">{d['N']['Out']}</text>
        <rect x="5" y="155" width="28" height="18" fill="white" stroke="black"/> <text x="19" y="168" text-anchor="middle" font-size="8">{d['N']['R']:.0f}</text>
        <rect x="33" y="155" width="28" height="18" fill="white" stroke="black"/> <text x="47" y="168" text-anchor="middle" font-size="8">{d['N']['T']:.0f}</text>
        <rect x="61" y="155" width="28" height="18" fill="white" stroke="black"/> <text x="75" y="168" text-anchor="middle" font-size="8">{d['N']['L']:.0f}</text>
        <path d="M 19 178 v 15 M 47 178 v 15 M 75 178 v 15" fill="none" stroke="black" marker-end="url(#arr)"/>
    </g>

    <g transform="translate(200, 310)">
        <text x="50" y="180" text-anchor="middle" font-size="11" font-weight="bold">แคราย</text>
        <rect x="5" y="145" width="40" height="18" fill="white" stroke="black"/> <text x="25" y="158" text-anchor="middle" font-size="9">{d['S']['Out']}</text>
        <rect x="55" y="145" width="40" height="18" fill="#f0f0f0" stroke="black"/> <text x="75" y="158" text-anchor="middle" font-size="9">{d['S']['In']}</text>
        <rect x="11" y="0" width="28" height="18" fill="white" stroke="black"/> <text x="25" y="13" text-anchor="middle" font-size="8">{d['S']['L']:.0f}</text>
        <rect x="39" y="0" width="28" height="18" fill="white" stroke="black"/> <text x="53" y="13" text-anchor="middle" font-size="8">{d['S']['T']:.0f}</text>
        <rect x="67" y="0" width="28" height="18" fill="white" stroke="black"/> <text x="81" y="13" text-anchor="middle" font-size="8">{d['S']['R']:.0f}</text>
        <path d="M 25 -5 v -15 M 53 -5 v -15 M 81 -5 v -15" fill="none" stroke="black" marker-end="url(#arr)"/>
    </g>

    <g transform="translate(10, 200)">
        <rect x="5" y="5" width="40" height="18" fill="#f0f0f0" stroke="black"/> <text x="25" y="18" text-anchor="middle" font-size="9">{d['W']['In']}</text>
        <rect x="5" y="77" width="40" height="18" fill="white" stroke="black"/> <text x="25" y="90" text-anchor="middle" font-size="9">{d['W']['Out']}</text>
        <rect x="155" y="5" width="28" height="18" fill="white" stroke="black"/> <text x="169" y="18" text-anchor="middle" font-size="8">{d['W']['L']:.0f}</text>
        <rect x="155" y="33" width="28" height="18" fill="white" stroke="black"/> <text x="169" y="46" text-anchor="middle" font-size="8">{d['W']['T']:.0f}</text>
        <rect x="155" y="61" width="28" height="18" fill="white" stroke="black"/> <text x="169" y="74" text-anchor="middle" font-size="8">{d['W']['R']:.0f}</text>
        <path d="M 188 14 h 15 M 188 42 h 15 M 188 70 h 15" fill="none" stroke="black" marker-end="url(#arr)"/>
    </g>

    <g transform="translate(290, 200)">
        <text x="100" y="-10" text-anchor="middle" font-size="11" font-weight="bold">งามวงศ์วาน</text>
        <rect x="155" y="5" width="40" height="18" fill="white" stroke="black"/> <text x="175" y="18" text-anchor="middle" font-size="9">{d['E']['Out']}</text>
        <rect x="155" y="77" width="40" height="18" fill="#f0f0f0" stroke="black"/> <text x="175" y="90" text-anchor="middle" font-size="9">{d['E']['In']}</text>
        <rect x="5" y="12" width="28" height="18" fill="white" stroke="black"/> <text x="19" y="25" text-anchor="middle" font-size="8">{d['E']['R']:.0f}</text>
        <rect x="5" y="40" width="28" height="18" fill="white" stroke="black"/> <text x="19" y="53" text-anchor="middle" font-size="8">{d['E']['T']:.0f}</text>
        <rect x="5" y="68" width="28" height="18" fill="white" stroke="black"/> <text x="19" y="81" text-anchor="middle" font-size="8">{d['E']['L']:.0f}</text>
        <path d="M 0 21 h -15 M 0 49 h -15 M 0 77 h -15" fill="none" stroke="black" marker-end="url(#arr)"/>
    </g>

    <defs>
        <marker id="arr" markerWidth="8" markerHeight="8" refX="4" refY="4" orient="auto">
            <path d="M 0 0 L 8 4 L 0 8 z" fill="black" />
        </marker>
    </defs>
</svg>
"""

st.components.v1.html(svg, height=520)
st.info("✅ ปรับขนาด Compact เห็นภาพรวมทั้งหมด และแยกฝั่ง Inbound (สีเทา) / Outbound (สีขาว) ให้ถูกต้องตามเลนไทยแล้วครับ")
