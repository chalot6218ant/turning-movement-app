import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(page_title="Compact Traffic Diagram", layout="wide")

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
    st.header("🚦 ตั้งค่าปริมาณจราจร")
    legs = ["North (N)", "South (S)", "East (E)", "West (W)"]
    in_v, out_v = [], []
    for leg in legs:
        st.subheader(f"ทิศ {leg}")
        c1, c2 = st.columns(2)
        in_v.append(c1.number_input(f"ขาเข้า (In)", min_value=0, value=1000, key=f"in_{leg}"))
        out_v.append(c2.number_input(f"ขาออก (Out)", min_value=0, value=1000, key=f"out_{leg}"))
    u_p = st.slider("U-Turn (%)", 0, 10, 2)
    s_p = st.slider("ตรงไป (%)", 40, 95, 70)

# --- Data Preparation ---
df = calc_matrix(in_v, out_v, legs, u_p, s_p)
# d[ทิศ][เลน] -> L: ซ้าย, T: ตรง, R: ขวา
d = {
    "N": {"T": df.iloc[0,1], "R": df.iloc[0,2], "L": df.iloc[0,3], "In": in_v[0], "Out": out_v[0]},
    "S": {"T": df.iloc[1,0], "R": df.iloc[1,3], "L": df.iloc[1,2], "In": in_v[1], "Out": out_v[1]},
    "E": {"T": df.iloc[2,3], "R": df.iloc[2,0], "L": df.iloc[2,1], "In": in_v[2], "Out": out_v[2]},
    "W": {"T": df.iloc[3,2], "R": df.iloc[3,1], "L": df.iloc[3,0], "In": in_v[3], "Out": out_v[3]},
}

st.title("🚦 Turning Movement Diagram (Compact)")

# --- SVG Drawing: เน้นขนาดเล็กและทิศทางถูกต้อง ---
svg_code = f"""
<svg viewBox="0 0 600 600" xmlns="http://www.w3.org/2000/svg" style="background:#fff; border:1px solid #ccc; display:block; margin:auto;">
    <path d="M 240 0 v 240 h -240 M 0 360 h 240 v 240 M 360 600 v -240 h 240 M 600 240 h -240 v -240" 
          fill="none" stroke="#666" stroke-width="1.5"/>
    
    <text x="540" y="50" font-size="12" font-weight="bold">N ▲</text>

    <g transform="translate(240, 10)">
        <text x="60" y="20" text-anchor="middle" font-weight="bold" font-size="12">ติวานนท์</text>
        <rect x="5" y="30" width="50" height="20" fill="none" stroke="black"/> <text x="30" y="44" text-anchor="middle" font-size="10">{d['N']['In']}</text>
        <rect x="65" y="30" width="50" height="20" fill="none" stroke="black"/> <text x="90" y="44" text-anchor="middle" font-size="10">{d['N']['Out']}</text>
        <rect x="5" y="190" width="35" height="20" fill="white" stroke="black"/> <text x="22" y="204" text-anchor="middle" font-size="9">{d['N']['R']:.0f}</text>
        <rect x="40" y="190" width="40" height="20" fill="white" stroke="black"/> <text x="60" y="204" text-anchor="middle" font-size="9">{d['N']['T']:.0f}</text>
        <rect x="80" y="190" width="35" height="20" fill="white" stroke="black"/> <text x="97" y="204" text-anchor="middle" font-size="9">{d['N']['L']:.0f}</text>
        <path d="M 22 215 v 15 M 60 215 v 15 M 97 215 v 15" fill="none" stroke="black" stroke-width="1.5" marker-end="url(#arr)"/>
    </g>

    <g transform="translate(240, 420)">
        <text x="60" y="160" text-anchor="middle" font-weight="bold" font-size="12">แคราย</text>
        <rect x="5" y="120" width="50" height="20" fill="none" stroke="black"/> <text x="30" y="134" text-anchor="middle" font-size="10">{d['S']['Out']}</text>
        <rect x="65" y="120" width="50" height="20" fill="none" stroke="black"/> <text x="90" y="134" text-anchor="middle" font-size="10">{d['S']['In']}</text>
        <rect x="5" y="0" width="35" height="20" fill="white" stroke="black"/> <text x="22" y="14" text-anchor="middle" font-size="9">{d['S']['L']:.0f}</text>
        <rect x="40" y="0" width="40" height="20" fill="white" stroke="black"/> <text x="60" y="14" text-anchor="middle" font-size="9">{d['S']['T']:.0f}</text>
        <rect x="80" y="0" width="35" height="20" fill="white" stroke="black"/> <text x="97" y="14" text-anchor="middle" font-size="9">{d['S']['R']:.0f}</text>
        <path d="M 22 -5 v -15 M 60 -5 v -15 M 97 -5 v -15" fill="none" stroke="black" stroke-width="1.5" marker-end="url(#arr)"/>
    </g>

    <g transform="translate(10, 240)">
        <rect x="10" y="5" width="50" height="20" fill="none" stroke="black"/> <text x="35" y="19" text-anchor="middle" font-size="10">{d['W']['In']}</text>
        <rect x="10" y="95" width="50" height="20" fill="none" stroke="black"/> <text x="35" y="109" text-anchor="middle" font-size="10">{d['W']['Out']}</text>
        <rect x="190" y="5" width="35" height="20" fill="white" stroke="black"/> <text x="207" y="19" text-anchor="middle" font-size="9">{d['W']['L']:.0f}</text>
        <rect x="190" y="40" width="40" height="20" fill="white" stroke="black"/> <text x="210" y="54" text-anchor="middle" font-size="9">{d['W']['T']:.0f}</text>
        <rect x="190" y="75" width="35" height="20" fill="white" stroke="black"/> <text x="207" y="89" text-anchor="middle" font-size="9">{d['W']['R']:.0f}</text>
        <path d="M 230 15 h 15 M 230 50 h 15 M 230 85 h 15" fill="none" stroke="black" stroke-width="1.5" marker-end="url(#arr)"/>
    </g>

    <g transform="translate(360, 240)">
        <text x="120" y="-15" text-anchor="end" font-weight="bold" font-size="12">งามวงศ์วาน</text>
        <rect x="170" y="5" width="50" height="20" fill="none" stroke="black"/> <text x="195" y="19" text-anchor="middle" font-size="10">{d['E']['Out']}</text>
        <rect x="170" y="95" width="50" height="20" fill="none" stroke="black"/> <text x="195" y="109" text-anchor="middle" font-size="10">{d['E']['In']}</text>
        <rect x="0" y="5" width="35" height="20" fill="white" stroke="black"/> <text x="17" y="19" text-anchor="middle" font-size="9">{d['E']['R']:.0f}</text>
        <rect x="0" y="40" width="40" height="20" fill="white" stroke="black"/> <text x="20" y="54" text-anchor="middle" font-size="9">{d['E']['T']:.0f}</text>
        <rect x="0" y="75" width="35" height="20" fill="white" stroke="black"/> <text x="17" y="89" text-anchor="middle" font-size="9">{d['E']['L']:.0f}</text>
        <path d="M -5 15 h -15 M -5 50 h -15 M -5 85 h -15" fill="none" stroke="black" stroke-width="1.5" marker-end="url(#arr)"/>
    </g>

    <defs>
        <marker id="arr" markerWidth="10" markerHeight="10" refX="5" refY="5" orient="auto">
            <path d="M 0 0 L 10 5 L 0 10 z" fill="black" />
        </marker>
    </defs>
</svg>
"""

st.components.v1.html(svg_code, height=620)
st.success("✅ แก้ไขให้ขนาดเล็กลงและทิศทางลูกศรตรงตามเลนจราจรไทยเรียบร้อยครับ")
