import streamlit as st
import pandas as pd

# --- 1. SETUP ---
st.set_page_config(
    page_title="TechChoose - AI Gadget Finder",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. LOAD DATA ---
@st.cache_data(ttl=60)
def load_data():
    # 👇👇👇 ลิงก์ CSV ของพี่ 👇👇👇
    sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQqoziKy640ID3oDos-DKk49txgsNPdMJGb_vAH1_WiRG88kewDPneVgo9iSHq2u5DXYI_g_n6se14k/pub?output=csv"
    try:
        df = pd.read_csv(sheet_url)
        df['os_type'] = df['name'].apply(lambda x: 'iOS' if 'iPhone' in str(x) else 'Android')
        return df
    except:
        return pd.DataFrame()

# --- 3. STYLE ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    .stApp { background-color: #0F172A; color: #F8FAFC; font-family: 'Inter', sans-serif; }
    
    /* Highlight Text */
    .highlight { color: #FBBF24; font-weight: bold; }
    
    /* Progress Bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #3B82F6 0%, #8B5CF6 100%);
        height: 10px !important; border-radius: 6px;
    }
    
    /* Card Design */
    .product-card {
        background: #1E293B; border: 1px solid #334155;
        padding: 20px; border-radius: 16px; margin-bottom: 15px;
        transition: transform 0.2s;
    }
    .product-card:hover { transform: translateY(-5px); border-color: #FBBF24; }
    
    /* Button */
    .cta-btn {
        background: linear-gradient(90deg, #F59E0B, #D97706);
        color: white !important; padding: 12px 24px; border-radius: 8px;
        text-decoration: none; font-weight: bold; display: inline-block;
        margin-top: 10px; box-shadow: 0 4px 10px rgba(245, 158, 11, 0.3);
    }
    .cta-btn:hover { transform: scale(1.05); color: white !important; }
</style>
""", unsafe_allow_html=True)

# --- 4. SIDEBAR ---
with st.sidebar:
    st.title("🤖 TechChoose AI")
    st.caption("Smart Recommendations in 3 clicks.")
    st.write("---")
    
    st.markdown("### 1️⃣ Ecosystem")
    os_choice = st.radio("Select OS:", ["Show All", "🍎 iOS (iPhone)", "🤖 Android"], index=0)
    
    st.markdown("### 2️⃣ What matters most?")
    # Helper to convert text to number
    def score(t): return {"Low": 1, "Medium": 5, "High": 8, "Max": 10}[t]
    
    w_perf = score(st.select_slider("Gaming / Speed", ["Low", "Medium", "High", "Max"], "High"))
    w_cam = score(st.select_slider("Camera Quality", ["Low", "Medium", "High", "Max"], "High"))
    w_batt = score(st.select_slider("Battery Life", ["Low", "Medium", "High", "Max"], "Medium"))
    w_val = score(st.select_slider("Price / Value", ["Low", "Medium", "High", "Max"], "Medium"))
    
    st.write("---")
    if st.button("🚀 Run Analysis", type="primary"):
        st.rerun()

# --- 5. MAIN LOGIC ---
df = load_data()

if not df.empty:
    # Filter OS
    if "iOS" in os_choice: df = df[df['os_type'] == 'iOS']
    elif "Android" in os_choice: df = df[df['os_type'] == 'Android']
    
    # Calculate Score
    df['score'] = (df['performance']*w_perf) + (df['camera']*w_cam) + (df['battery']*w_batt) + (df['value']*w_val)
    max_score = (10*w_perf) + (10*w_cam) + (10*w_batt) + (10*w_val)
    df['match'] = (df['score'] / max_score) * 100
    df = df.sort_values('match', ascending=False).reset_index(drop=True)
    
    top = df.iloc[0]

    # --- SHOWCASE ---
    c1, c2 = st.columns([1.5, 1], gap="large")
    
    with c1:
        st.caption(f"🏆 TOP MATCH ({top['match']:.0f}%)")
        st.markdown(f"# {top['name']}")
        st.markdown(f"<h2 style='color:#FBBF24'>${top['price']:,}</h2>", unsafe_allow_html=True)
        
        st.markdown("### 📊 AI Analysis")
        st.progress(int(top['performance']*10), f"Speed: {top['performance']}/10")
        st.progress(int(top['camera']*10), f"Camera: {top['camera']}/10")
        st.progress(int(top['battery']*10), f"Battery: {top['battery']}/10")
        
        st.markdown(f"""
            <br>
            <a href="{top['link']}" target="_blank" class="cta-btn">
                🛒 Check Price & Reviews on Amazon
            </a>
        """, unsafe_allow_html=True)

    with c2:
        st.subheader("🥈 Runner-ups")
        for i, row in df.iloc[1:5].iterrows():
            st.markdown(f"""
            <div class="product-card">
                <div style="display:flex; justify-content:space-between;">
                    <b>{row['name']}</b>
                    <span class="highlight">{row['match']:.0f}%</span>
                </div>
                <div style="color:#94A3B8; font-size:0.9em;">${row['price']:,}</div>
                <a href="{row['link']}" target="_blank" style="color:#FBBF24; text-decoration:none; font-weight:bold; font-size:0.9em;">View Deal ></a>
            </div>
            """, unsafe_allow_html=True)

    # --- DISCLAIMER (กฎเหล็ก) ---
    st.write("---")
    st.markdown("""
    <div style='text-align: center; color: #64748B; font-size: 0.8em;'>
        <p>Disclaimer: TechChoose is a participant in the Amazon Services LLC Associates Program. 
        As an Amazon Associate, we earn from qualifying purchases.</p>
        <p>© 2025 TechChoose. Prices and availability are subject to change.</p>
    </div>
    """, unsafe_allow_html=True)

else:
    st.error("Connection Error: Please check your Google Sheet Link.")