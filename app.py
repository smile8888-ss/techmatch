import streamlit as st
import pandas as pd

# --- 1. CONFIG ---
st.set_page_config(
    page_title="TechChoose - Smart Finder",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. LOAD DATA ---
@st.cache_data(ttl=60)
def load_data():
    # 👇👇👇 ใส่ลิงก์ CSV ของพี่เหมือนเดิมครับ 👇👇👇
    sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQqoziKy640ID3oDos-DKk49txgsNPdMJGb_vAH1_WiRG88kewDPneVgo9iSHq2u5DXYI_g_n6se14k/pub?output=csv" 
    try:
        df = pd.read_csv(sheet_url)
        df['os_type'] = df['name'].apply(lambda x: 'iOS' if 'iPhone' in str(x) else 'Android')
        return df
    except:
        return pd.DataFrame()

# --- 3. PREMIUM STYLE (NEON) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;900&display=swap');
    
    .stApp {
        background-color: #0F172A;
        color: #F8FAFC;
        font-family: 'Inter', sans-serif;
    }

    /* Winner Badge */
    .winner-badge {
        background: #F59E0B; color: black; font-weight: bold;
        padding: 8px 16px; border-radius: 20px; font-size: 0.9em;
        box-shadow: 0 0 10px rgba(245, 158, 11, 0.5);
    }

    /* Card สินค้า */
    .product-card {
        background: #1E293B; border: 1px solid #334155;
        padding: 20px; border-radius: 16px; margin-bottom: 20px;
        transition: transform 0.2s;
    }
    .product-card:hover { border-color: #3B82F6; transform: translateY(-5px); }

    /* ปุ่ม Amazon สีทอง (แก้สีตัวอักษรเป็นดำเข้ม) */
    .amazon-btn {
        background: linear-gradient(to bottom, #FFD814, #F7CA00);
        color: #000000 !important; /* สีดำสนิท */
        padding: 12px 24px; border-radius: 8px;
        text-decoration: none; font-weight: 800; display: inline-block;
        margin-top: 15px; text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .amazon-btn:hover { transform: scale(1.02); color: #000000 !important; }
    
    /* ตัวเลขราคา */
    .price-text { color: #FBBF24; font-weight: 900; font-size: 1.5em; }
    
    /* Progress Bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #3B82F6 0%, #60A5FA 100%);
    }
</style>
""", unsafe_allow_html=True)

# --- 4. SIDEBAR ---
with st.sidebar:
    st.title("🎯 Filter")
    st.divider()
    os_choice = st.radio("System:", ["Any", "iOS (iPhone)", "Android"], index=0)
    st.write("---")
    
    def get_score(label):
        return {"Don't Care": 1, "Nice to Have": 5, "Important": 8, "Essential!": 10}[label]

    p_opt = st.select_slider("Speed & Gaming", ["Don't Care", "Nice to Have", "Important", "Essential!"], "Important")
    c_opt = st.select_slider("Camera Quality", ["Don't Care", "Nice to Have", "Important", "Essential!"], "Important")
    b_opt = st.select_slider("Battery Life", ["Don't Care", "Nice to Have", "Important", "Essential!"], "Nice to Have")
    v_opt = st.select_slider("Price / Value", ["Don't Care", "Nice to Have", "Important", "Essential!"], "Nice to Have")

    w_perf, w_cam, w_batt, w_val = get_score(p_opt), get_score(c_opt), get_score(b_opt), get_score(v_opt)

    st.divider()
    if st.button("🚀 Find My Match", type="primary"):
        st.rerun()

# --- 5. MAIN LOGIC ---
df = load_data()

if not df.empty:
    if "iOS" in os_choice: df = df[df['os_type'] == 'iOS']
    elif "Android" in os_choice: df = df[df['os_type'] == 'Android']

    # Calc Score
    df['score_raw'] = (df['performance']*w_perf) + (df['camera']*w_cam) + (df['battery']*w_batt) + (df['value']*w_val)
    max_possible = (10*w_perf) + (10*w_cam) + (10*w_batt) + (10*w_val)
    df['match_percent'] = (df['score_raw'] / max_possible) * 100
    df = df.sort_values(by='match_percent', ascending=False).reset_index(drop=True)
    winner = df.iloc[0]

    col1, col2 = st.columns([1.6, 1.2], gap="large")

    # --- WINNER SECTION (กลับมาใช้แบบเดิมที่สวยๆ) ---
    with col1:
        st.markdown(f"""
        <div style='padding:30px; border:2px solid #F59E0B; border-radius:20px; background:linear-gradient(180deg, #1E293B 0%, #0F172A 100%); text-align:center;'>
            <span class='winner-badge'>🏆 #1 TOP PICK FOR YOU ({winner['match_percent']:.0f}%)</span>
            <h1 style='margin-top:15px; font-size:2.5em;'>{winner['name']}</h1>
            <div class='price-text'>${winner['price']:,}</div>
            <br>
        """, unsafe_allow_html=True)
        
        st.progress(int(winner['performance']*10), f"⚡ Speed: {winner['performance']}/10")
        st.progress(int(winner['camera']*10), f"📸 Camera: {winner['camera']}/10")
        st.progress(int(winner['battery']*10), f"🔋 Battery: {winner['battery']}/10")
        
        st.markdown(f"""
            <a href="{winner['link']}" target="_blank" class="amazon-btn">
                🛒 Buy on Amazon
            </a>
        </div>
        """, unsafe_allow_html=True)

    # --- RUNNERS UP & COMPARISON (แก้ให้เสถียร) ---
    with col2:
        st.subheader("🥈 Alternatives")
        for i, row in df.iloc[1:6].iterrows():
            with st.container():
                # Card HTML
                st.markdown(f"""
                <div class="product-card">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <b style="font-size:1.1em;">{row['name']}</b>
                        <span style="color:#3B82F6; font-weight:bold;">{row['match_percent']:.0f}%</span>
                    </div>
                    <div style="color:#94A3B8; margin-bottom:10px;">Est. ${row['price']:,}</div>
                    <a href='{row['link']}' target='_blank' style='color:#F59E0B; text-decoration:none; font-weight:bold; font-size:0.9em; display:block; margin-bottom:10px;'>
                        View Deal >
                    </a>
                </div>
                """, unsafe_allow_html=True)

                # 🔥 Feature เปรียบเทียบแบบ Native (ไม่พังแน่นอน)
                with st.expander(f"🆚 Compare vs {winner['name']}"):
                    c1, c2 = st.columns(2)
                    with c1:
                        st.caption("Winner")
                        st.write(f"**{winner['performance']}** Speed")
                        st.write(f"**{winner['camera']}** Cam")
                    with c2:
                        st.caption("This")
                        st.write(f"**{row['performance']}** Speed")
                        st.write(f"**{row['camera']}** Cam")
                    
                    diff = winner['price'] - row['price']
                    if diff > 0:
                        st.success(f"💰 Save ${diff:,}")
                    else:
                        st.info(f"💎 Premium")

    # --- Footer ---
    st.write("---")
    st.caption("Disclaimer: TechChoose is a participant in the Amazon Services LLC Associates Program. Prices are subject to change.")

else:
    st.error("Please connect your Google Sheet CSV.")