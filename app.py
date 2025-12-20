import streamlit as st
import pandas as pd

# --- 1. SETUP ---
st.set_page_config(
    page_title="TechChoose - Smart Comparison",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. LOAD DATA ---
@st.cache_data(ttl=60)
def load_data():
    # 👇👇👇 ลิงก์ CSV ของพี่ ใส่ตรงนี้ครับ 👇👇👇
    sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQqoziKy640ID3oDos-DKk49txgsNPdMJGb_vAH1_WiRG88kewDPneVgo9iSHq2u5DXYI_g_n6se14k/pub?output=csv"
    try:
        df = pd.read_csv(sheet_url)
        df['os_type'] = df['name'].apply(lambda x: 'iOS' if 'iPhone' in str(x) else 'Android')
        return df
    except:
        return pd.DataFrame()

# --- 3. STYLE (Neon & Comparison) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    .stApp { background-color: #0B1120; color: #E2E8F0; font-family: 'Inter', sans-serif; }
    
    /* Comparison Box */
    .vs-box {
        background: #1E293B;
        border: 2px solid #334155;
        border-radius: 15px;
        padding: 20px;
        margin-top: 20px;
        text-align: center;
    }
    
    /* Winner Label */
    .winner-badge {
        background-color: #F59E0B; color: black; 
        padding: 5px 15px; border-radius: 20px; 
        font-weight: bold; font-size: 0.8em;
    }
    
    /* Metric Enhancement */
    [data-testid="stMetricValue"] { font-size: 1.8rem !important; }
    
    /* Button */
    .cta-btn {
        background: linear-gradient(90deg, #F59E0B, #D97706);
        color: white !important; padding: 15px 30px; border-radius: 10px;
        text-decoration: none; font-weight: 800; display: block;
        margin-top: 20px; text-align: center;
        box-shadow: 0 4px 15px rgba(245, 158, 11, 0.4);
    }
    .cta-btn:hover { transform: scale(1.02); }
</style>
""", unsafe_allow_html=True)

# --- 4. SIDEBAR ---
with st.sidebar:
    st.title("⚖️ TechChoose")
    st.markdown("Compare & Decide in seconds.")
    st.write("---")
    
    st.header("📱 Ecosystem")
    os_choice = st.radio("System:", ["Any", "iOS (iPhone)", "Android"], index=0)
    
    st.write("---")
    st.header("🎯 Priorities")
    def score(t): return {"Low": 1, "Medium": 5, "High": 8, "Max": 10}[t]
    
    w_perf = score(st.select_slider("Gaming/Speed", ["Low", "Medium", "High", "Max"], "High"))
    w_cam = score(st.select_slider("Camera", ["Low", "Medium", "High", "Max"], "High"))
    w_batt = score(st.select_slider("Battery", ["Low", "Medium", "High", "Max"], "Medium"))
    w_val = score(st.select_slider("Value", ["Low", "Medium", "High", "Max"], "Medium"))
    
    st.write("---")
    if st.button("🚀 Analyze Now", type="primary"):
        st.rerun()

# --- 5. MAIN LOGIC ---
df = load_data()

if not df.empty:
    # Filter & Calculate
    if "iOS" in os_choice: df = df[df['os_type'] == 'iOS']
    elif "Android" in os_choice: df = df[df['os_type'] == 'Android']
    
    df['score'] = (df['performance']*w_perf) + (df['camera']*w_cam) + (df['battery']*w_batt) + (df['value']*w_val)
    max_score = (10*w_perf) + (10*w_cam) + (10*w_batt) + (10*w_val)
    df['match'] = (df['score'] / max_score) * 100
    df = df.sort_values('match', ascending=False).reset_index(drop=True)
    
    winner = df.iloc[0]
    
    # --- UI LAYOUT ---
    st.caption(f"✅ AI Analysis Complete based on your {w_perf/10*100:.0f}% focus on performance.")
    
    # 🏆 ส่วนโชว์ผู้ชนะ (Hero Section)
    col1, col2 = st.columns([1.5, 1])
    with col1:
        st.markdown(f"<span class='winner-badge'>🏆 #1 BEST CHOICE ({winner['match']:.0f}%)</span>", unsafe_allow_html=True)
        st.title(winner['name'])
        st.markdown(f"<h1 style='color:#FBBF24; margin-top:-20px;'>${winner['price']:,}</h1>", unsafe_allow_html=True)
        st.markdown(f"""
            <a href="{winner['link']}" target="_blank" class="cta-btn">
                🛒 See Today's Deal on Amazon
            </a>
        """, unsafe_allow_html=True)

    # ⚔️ ส่วนเปรียบเทียบ (Head-to-Head) - ฟีเจอร์ใหม่!
    if len(df) > 1:
        runner_up = df.iloc[1]
        
        st.write("---")
        st.subheader("🥊 Head-to-Head: Why #1 Won?")
        
        # กล่องเปรียบเทียบ
        with st.container():
            c1, c2, c3 = st.columns([1, 0.5, 1])
            
            # ฝั่งผู้ชนะ
            with c1:
                st.info(f"🏆 {winner['name']}")
                st.metric("Speed", f"{winner['performance']}/10", f"{winner['performance'] - runner_up['performance']}")
                st.metric("Camera", f"{winner['camera']}/10", f"{winner['camera'] - runner_up['camera']}")
                st.metric("Battery", f"{winner['battery']}/10", f"{winner['battery'] - runner_up['battery']}")
            
            # ตรงกลาง (VS)
            with c2:
                st.markdown("<br><br><h1 style='text-align:center; color:#64748B;'>VS</h1>", unsafe_allow_html=True)
            
            # ฝั่งที่ 2
            with c3:
                st.write(f"🥈 {runner_up['name']}")
                st.metric("Speed", f"{runner_up['performance']}/10", delta_color="off")
                st.metric("Camera", f"{runner_up['camera']}/10", delta_color="off")
                st.metric("Battery", f"{runner_up['battery']}/10", delta_color="off")

        # สรุปเหตุผล (Verdict)
        diff_price = runner_up['price'] - winner['price']
        verdict = ""
        if winner['performance'] > runner_up['performance']:
            verdict += f"The **{winner['name']}** is faster. "
        if winner['camera'] > runner_up['camera']:
            verdict += "It has a better camera system. "
        if diff_price > 0:
            verdict += f"Plus, it is **${diff_price} cheaper** than the {runner_up['name']}!"
        elif diff_price < 0:
            verdict += f"It costs a bit more, but the specs are worth it."
            
        st.success(f"💡 **AI Verdict:** {verdict}")

    # --- DISCLAIMER ---
    st.write("---")
    st.caption("Disclaimer: TechChoose is a participant in the Amazon Services LLC Associates Program. Prices are subject to change.")

else:
    st.error("Please connect your Google Sheet.")