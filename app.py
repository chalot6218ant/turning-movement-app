import streamlit as st

st.set_page_config(layout="wide", page_title="Traffic Turning Movement Calculator")

# --- ส่วนการปรับแต่งที่ Sidebar ---
st.sidebar.header("⚙️ Settings")
title_text = st.sidebar.text_input("หัวข้อแผนภูมิ", "Year 2006 AM")
unit_text = st.sidebar.text_input("หน่วย", "หน่วย : PCU/Hr.")

st.sidebar.subheader("📍 ชื่อถนน")
rd_n = st.sidebar.text_input("ถนนทิศเหนือ", "ติวานนท์")
rd_s = st.sidebar.text_input("ถนนทิศใต้", "ติวานนท์")
rd_e = st.sidebar.text_input("ถนนทิศตะวันออก", "งามวงศ์วาน")
rd_w = st.sidebar.text_input("ถนนทิศตะวันตก", "รัตนาธิเบศร์")

# --- ส่วนการกรอกข้อมูล ---
st.subheader("📝 ป้อนข้อมูลปริมาณจราจร")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"**⬇️ จากทิศเหนือ ({rd_n})**")
    n_l = st.number_input("ซ้าย (L)", value=25, key="nl")
    n_t = st.number_input("ตรง (T)", value=1190, key="nt")
    n_r = st.number_input("ขวา (R)", value=2362, key="nr")
with col2:
    st.markdown(f"**⬆️ จากทิศใต้ ({rd_s})**")
    s_l = st.number_input("ซ้าย (L)", value=1693, key="sl")
    s_t = st.number_input("ตรง (T)", value=481, key="st")
    s_r = st.number_input("ขวา (R)", value=60, key="sr")
with col3:
    st.markdown(f"**⬅️ จากทิศตะวันออก ({rd_e})**")
    e_l = st.number_input("ซ้าย (L)", value=752, key="el")
    e_t = st.number_input("ตรง (T)", value=1762, key="et")
    e_r = st.number_input("ขวา (R)", value=1114, key="er")
with col4:
    st.markdown(f"**➡️ จากทิศตะวันตก ({rd_w})**")
    w_l = st.number_input("ซ้าย (L)", value=516, key="wl")
    w_t = st.number_input("ตรง (T)", value=3935, key="wt")
    w_r = st.number_input("ขวา (R)", value=37, key="wr")

# --- Logic การคำนวณ ---
in_n, in_s, in_e, in_w = (n_l+n_t+n_r), (s_l+s_t+s_r), (e_l+e_t+e_r), (w_l+w_t+w_r)
out_n = s_t + e_r + w_l
out_s = n_t + w_r + e_l
out_e = w_t + n_l + s_r
out_w = e_t + s_l + n_r

# --- แสดงผล Diagram ด้วย CSS ---
st.divider()

html_code = f"""
<style>
    .canvas {{
        width: 850px;
        height: 700px;
        background-color: white;
        border: 1px solid #999;
        margin: 0 auto;
        position: relative;
        background-image: linear-gradient(#eee 1px, transparent 1px), linear-gradient(90deg, #eee 1px, transparent 1px);
        background-size: 20px 20px;
        font-family: sans-serif;
    }}
    .title {{ text-align: center; width: 100%; padding-top: 20px; font-size: 18px; }}
    .val-box {{
        position: absolute; border: 1px solid black; background: white;
        text-align: center; font-size: 13px; min-width: 45px; height: 22px; line-height: 22px;
    }}
    .road-line-v {{ position: absolute; width: 2px; background: black; }}
    .road-line-h {{ position: absolute; height: 2px; background: black; }}
    .arrow-icon {{ position: absolute; font-size: 22px; font-weight: bold; }}
    .road-label {{ position: absolute; font-size: 12px; font-weight: bold; }}
</style>

<div class="canvas">
    <div class="title">{title_text}</div>

    <div class="road-line-v" style="left: 340px; top: 100px; height: 160px;"></div>
    <div class="road-line-v" style="left: 500px; top: 100px; height: 160px;"></div>
    <div class="road-label" style="left: 410px; top: 220px; transform: rotate(-90deg);">{rd_n}</div>
    <div class="val-box" style="left: 350px; top: 140px;">{out_n:,}</div>
    <div class="val-box" style="left: 440px; top: 140px;">{in_n:,}</div>
    <div class="val-box" style="left: 410px; top: 237px; min-width: 25px;">{n_l}</div>
    <div class="val-box" style="left: 437px; top: 237px; min-width: 35px;">{n_t}</div>
    <div class="val-box" style="left: 474px; top: 237px; min-width: 25px;">{n_r}</div>
    <div class="arrow-icon" style="left: 405px; top: 255px;">↧</div>
    <div class="arrow-icon" style="left: 443px; top: 255px;">↓</div>
    <div class="arrow-icon" style="left: 475px; top: 255px;">↴</div>

    <div class="road-line-v" style="left: 340px; top: 410px; height: 160px;"></div>
    <div class="road-line-v" style="left: 500px; top: 410px; height: 160px;"></div>
    <div class="val-box" style="left: 440px; top: 520px;">{out_s:,}</div>
    <div class="val-box" style="left: 350px; top: 520px;">{in_s:,}</div>
    <div class="val-box" style="left: 340px; top: 410px; min-width: 25px;">{s_r}</div>
    <div class="val-box" style="left: 367px; top: 410px; min-width: 35px;">{s_t}</div>
    <div class="val-box" style="left: 404px; top: 410px; min-width: 25px;">{s_l}</div>
    <div class="arrow-icon" style="left: 335px; top: 380px;">↰</div>
    <div class="arrow-icon" style="left: 373px; top: 380px;">↑</div>
    <div class="arrow-icon" style="left: 405px; top: 380px;">⤴</div>

    <div class="road-line-h" style="left: 500px; top: 260px; width: 250px;"></div>
    <div class="road-line-h" style="left: 500px; top: 410px; width: 250px;"></div>
    <div class="road-label" style="left: 600px; top: 340px;">{rd_e}</div>
    <div class="val-box" style="left: 670px; top: 310px;">{in_e:,}</div>
    <div class="val-box" style="left: 670px; top: 365px;">{out_e:,}</div>
    <div class="val-box" style="left: 550px; top: 337px; min-width: 40px;">{e_l}</div>
    <div class="val-box" style="left: 550px; top: 361px; min-width: 40px;">{e_t}</div>
    <div class="val-box" style="left: 550px; top: 385px; min-width: 40px;">{e_r}</div>
    <div class="arrow-icon" style="left: 515px; top: 332px;">↤</div>
    <div class="arrow-icon" style="left: 515px; top: 357px;">←</div>
    <div class="arrow-icon" style="left: 515px; top: 382px;">↲</div>

    <div class="road-line-h" style="left: 90px; top: 260px; width: 250px;"></div>
    <div class="road-line-h" style="left: 90px; top: 410px; width: 250px;"></div>
    <div class="val-box" style="left: 140px; top: 310px;">{in_w:,}</div>
    <div class="val-box" style="left: 140px; top: 365px;">{out_w:,}</div>
    <div class="val-box" style="left: 250px; top: 260px; min-width: 40px;">{w_r}</div>
    <div class="val-box" style="left: 250px; top: 2
