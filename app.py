import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(page_title="Traffic Analysis Dashboard", layout="wide")

# --- Custom CSS for Maximum Readability ---
st.markdown("""
    <style>
    .traffic-card {
        border: 3px solid #1e3a8a;
        padding: 20px;
        border-radius: 12px;
        background-color: #ffffff;
        text-align: center;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        margin-bottom: 15px;
    }
    .leg-name { color: #1e3a8a; font-size: 24px; font-weight: bold; margin-bottom: 10px; }
    .in-out-row { display: flex; justify-content: space-around; margin-bottom: 15px; background: #f0f7ff; padding: 10px; border-radius: 8px; }
    .val-in { color: #0284c7; font-size: 26px; font-weight: bold; }
    .val-out { color: #475569; font-size: 26px; font-weight: bold; }
    .movement-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; border-top: 2px solid #eee; pt: 10px; }
    .m-box { padding: 8px; border: 1px solid #e2e8f0; border-radius: 5px; }
    .m-label { font-size: 14px; color: #64748b; display: block; }
    .m-val { font-size: 22px; font-weight: bold; color: #b91c1c; }
    </style>
    """, unsafe_allow_html=True)

# --- Traffic Logic (Fratar Method) ---
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
    st.header("🚦 Input Traffic Data")
    legs = ["North (N)", "South (S)", "East (E)", "West (W)"]
    in_v, out_v = [], []
    for leg in legs:
        st.subheader(f"Leg: {leg}")
        c1, c2 = st.columns(2)
        in_v.append(c1.number_input(f"Inbound", min_value=0, value=1000, key=f"i_{leg}"))
        out_v.append(c2.number_input(f"Outbound", min_value=0, value=1000, key=f"o_{leg}"))
    st.divider()
    u_p = st.slider("U-Turn %", 0, 15, 2)
    s_p = st.slider("Straight %", 40, 95, 70)

# --- Process Data ---
df = calc_matrix(in_v, out_v, legs, u_p, s_p)
d = {
    "N": {"In": in_v[0], "Out": out_v[0], "U": df.iloc[0,0], "T": df.iloc[0,1], "R": df.iloc[0,2], "L": df.iloc[0,3], "Name": "ติวานนท์"},
    "S": {"In": in_v[1], "Out": out_v[1], "U": df.iloc[1,1], "T": df.iloc[1,0], "R": df.iloc[1,3], "L": df.iloc[1,2], "Name": "แคราย"},
    "E": {"In": in_v[2], "Out": out_v[2], "U": df.iloc[2,2], "T": df.iloc[2,3], "R": df.iloc[2,0], "L": df.iloc[2,1], "Name": "งามวงศ์วาน"},
    "W": {"In": in_v[3], "Out": out_v[3], "U": df.iloc[3,3], "T": df.iloc[3,2], "R": df.iloc[3,1], "L": df.iloc[3,0], "Name": "West Leg"},
}

st.title("📊 Intersection Movement Analysis Dashboard")

# --- Layout: 3 Columns for Clean Organization ---
top_spacer, center_n, end_spacer = st.columns([1, 2, 1])
with center_n:
    # NORTH CARD
    st.markdown(f"""<div class="traffic-card">
        <div class="leg-name">{d['N']['Name']} (North)</div>
        <div class="in-out-row">
            <div><span style="font-size:14px">IN</span><br><span class="val-in">{d['N']['In']}</span></div>
            <div><span style="font-size:14px">OUT</span><br><span class="val-out">{d['N']['Out']}</span></div>
        </div>
        <div class="movement-grid">
            <div class="m-box"><span class="m-label">↶ U-Turn</span><span class="m-val">{d['N']['U']:.0f}</span></div>
            <div class="m-box"><span class="m-label">↓ Straight</span><span class="m-val">{d['N']['T']:.0f}</span></div>
            <div class="m-box"><span class="m-label">→ Right</span><span class="m-val">{d['N']['R']:.0f}</span></div>
            <div class="m-box"><span class="m-label">← Left</span><span class="m-val">{d['N']['L']:.0f}</span></div>
        </div>
    </div>""", unsafe_allow_html=True)

mid_w, mid_icon, mid_e = st.columns([2, 1, 2])
with mid_w:
    # WEST CARD
    st.markdown(f"""<div class="traffic-card">
        <div class="leg-name">{d['W']['Name']}</div>
        <div class="in-out-row">
            <div><span style="font-size:14px">IN</span><br><span class="val-in">{d['W']['In']}</span></div>
            <div><span style="font-size:14px">OUT</span><br><span class="val-out">{d['W']['Out']}</span></div>
        </div>
        <div class="movement-grid">
            <div class="m-box"><span class="m-label">← Left</span><span class="m-val">{d['W']['L']:.0f}</span></div>
            <div class="m-box"><span class="m-label">→ Straight</span><span class="m-val">{d['W']['T']:.0f}</span></div>
            <div class="m-box"><span class="m-label">↓ Right</span><span class="m-val">{d['W']['R']:.0f}</span></div>
            <div class="m-box"><span class="m-label">↶ U-Turn</span><span class="m-val">{d['W']['U']:.0f}</span></div>
        </div>
    </div>""", unsafe_allow_html=True)

with mid_icon:
    st.markdown("<div style='text-align:center; padding-top:40px;'><h1 style='font-size:60px;'>✛</h1><p>JUNCTION</p></div>", unsafe_allow_html=True)

with mid_e:
    # EAST CARD
    st.markdown(f"""<div class="traffic-card">
        <div class="leg-name">{d['E']['Name']}</div>
        <div class="in-out-row">
            <div><span style="font-size:14px">IN</span><br><span class="val-in">{d['E']['In']}</span></div>
            <div><span style="font-size:14px">OUT</span><br><span class="val-out">{d['E']['Out']}</span></div>
        </div>
        <div class="movement-grid">
            <div class="m-box"><span class="m-label">→ Right</span><span class="m-val">{d['E']['R']:.0f}</span></div>
            <div class="m-box"><span class="m-label">← Straight</span><span class="m-val">{d['E']['T']:.0f}</span></div>
            <div class="m-box"><span class="m-label">↓ Left</span><span class="m-val">{d['E']['L']:.0f}</span></div>
            <div class="m-box"><span class="m-label">↶ U-Turn</span><span class="m-val">{d['E']['U']:.0f}</span></div>
        </div>
    </div>""", unsafe_allow_html=True)

bot_spacer, center_s, end_spacer_b = st.columns([1, 2, 1])
with center_s:
    # SOUTH CARD
    st.markdown(f"""<div class="traffic-card">
        <div class="leg-name">{d['S']['Name']} (South)</div>
        <div class="in-out-row">
            <div><span style="font-size:14px">IN</span><br><span class="val-in">{d['S']['In']}</span></div>
            <div><span style="font-size:14px">OUT</span><br><span class="val-out">{d['S']['Out']}</span></div>
        </div>
        <div class="movement-grid">
            <div class="m-box"><span class="m-label">← Left</span><span class="m-val">{d['S']['L']:.0f}</span></div>
            <div class="m-box"><span class="m-label">↑ Straight</span><span class="m-val">{d['S']['T']:.0f}</span></div>
            <div class="m-box"><span class="m-label">→ Right</span><span class="m-val">{d['S']['R']:.0f}</span></div>
            <div class="m-box"><span class="m-label">↶ U-Turn</span><span class="m-val">{d['S']['U']:.0f}</span></div>
        </div>
    </div>""", unsafe_allow_html=True)
