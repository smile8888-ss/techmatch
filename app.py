import streamlit as st
import pandas as pd

# --- 1. CONFIG ---
st.set_page_config(
    page_title="TechChoose - Pro Dashboard",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. LOAD DATA ---
@st.cache_data(ttl=60)
def load_data():
    sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQqoziKy640ID3oDos-DKk49txgsNPdMJGb_vAH1_WiRG88kewDPneVgo9iSHq2u5DXYI_g_n6se14k/pub?output=csv"
    try:
        df = pd.read_csv(sheet_url)
        df['os_type'] = df['name'].apply(lambda x: 'iOS' if 'iPhone' in str(x) else 'Android')
        return df
    except Exception:
        return pd.DataFrame()

# --- 3. CSS (ธีม Pro ที่แก้เรื่องสีจมแล้ว) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700;900&display=swap');
    
    /* Global Font */
    .stApp { background-color: #0B1121; color: #E2E8F0; font-family: 'Inter', sans-serif; }
    
    /* --- SIDEBAR FIX (แก้สีจมให้ชัดเป๊ะ) --- */
    section[data-testid="stSidebar"] { background-color: #020617; border-right: 1px solid #1E293B; }
    
    /* บังคับสี Dropdown และ Slider */
    div[data-baseweb="select"] > div {
        background-color: #1E293B !important;
        color: white !important;
        border-color: #475569 !important;
    }
    div[data-baseweb="select"] span { color: white !important; }
    div[data-testid="stMarkdownContainer"] p { color: #CBD5E1; }

    /* --- WINNER CARD --- */
    .winner-card {
        background: linear-gradient(145deg, #1E293B 0%, #0F172A 100%);
        border: 1px solid #3B82F6; border-radius: 20px; padding: 35px;
        box-shadow: 0 10px 40px rgba(59, 130, 246, 0.15);
    }
    
    .rank-badge {
        background: #F59E0B; color: #000; font-weight: 800; 
        padding: 6px 16px; border-radius: 30px; 
        text-transform: uppercase; letter-spacing: 1px; font-size: 0.8em;
        display: inline-block; margin-bottom: 15px;
    }

    .hero-name {
        font-size: 3em; font-weight: 900; background: -webkit-linear-gradient(#fff, #94A3B8);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin: 10px 0; line-height: 1.1;
    }

    .hero-price { color: #FBBF24; font-size: 2.2em; font-weight: 700; margin-bottom: 25px; }

    /* --- STAT GRID (ตารางค่าพลัง 3 สี) --- */
    .stat-grid {
        display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px;
        background: #0B1121; padding: 20px; border-radius: 15px; border: 1px solid #334155;
    }
    .stat-box { text-align: center; }
    .stat-label { color: #94A3B8; font-size: 0.85em; font-weight: 600; text-transform: uppercase; margin-bottom: 5px; }
    .stat-value { font-size: 1.5em; font-weight: 800; color: white; }
    .stat-bar-bg { width: 100%; height: 6px; background: #334155; border-radius: 3px; margin-top: 8px; overflow: hidden; }
    .stat-bar-fill { height: 100%; border-radius: 3px; }

    /* --- ALTERNATIVES --- */
    .alt-row {
        background: #1E293B; border-bottom: 1px solid #334155;
        padding: 20px; border-radius: 12px; margin-bottom: 12px;
        display: flex; justify-content: space-between; align-items: center;
        transition: 0.2s;
    }
    .alt-row:hover { background: #28364A; border-color: #3B82F6; }

    /* BUTTON */
    .cta-btn {
        background: linear-gradient(90deg, #F59E0B, #D97706);
        color: white; padding: 15px 30px; border-radius: 50px; text-decoration: none;
        font-weight: bold; display: block; text-align: center; margin-top: 25px;
        box-shadow: 0 4px 15px rgba(245, 158, 11, 0.3); transition: 0.3s;
    }
    .cta-btn:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(245, 158, 11, 0.5); color:white;}

</style>
""", unsafe_allow_html=True)

# --- 4. SIDEBAR ---
with st.sidebar:
    st.markdown("### ⚙️ PREFERENCES")
    
    os_choice = st.selectbox("📱 Mobile Ecosystem", ["Any", "iOS (Apple)", "Android"])
    
    st.write("")
    lifestyle = st.selectbox("👤 User Persona", [
        "🎮 Hardcore Gamer", 
        "📸 Content Creator", 
        "💼 Business Professional", 
        "💰 Student / Budget Saver", 
        "🛠️ Custom Configuration"
    ])
    
    st.write("")
    budget = st.slider("💰 Maximum Budget ($)", 300, 2000, 2000, step=50)

    # Weights Logic
    p, c, b, v = 5, 5, 5, 5
    if "Gamer" in lifestyle: p,c,b,v = 10,3,8,5
    elif "Creator" in lifestyle: p,c,b,v = 7,10,8,5
    elif "Business" in lifestyle: p,c,b,v = 8,6,9,6
    elif "Student" in lifestyle: p,c,b,v = 5,5,7,10
    else: 
        st.divider()
        st.caption("Manual Sliders")
        p = st.slider("Performance", 1, 10, 8)
        c = st.slider("Camera", 1, 10, 8)
        b = st.slider("Battery", 1, 10, 5)
        v = st.slider("Value", 1, 10, 5)

    st.divider()
    st.button("🚀 RUN ANALYSIS", type="primary", use_container_width=True)

# --- 5. FUNCTIONS ---
def generate_pro_verdict(row, mode):
    # คำอธิบายแบบ Pro
    if "Gamer" in mode:
        return f"Engineered for dominance. The **{row['name']}** delivers elite frame rates, making it the definitive choice for mobile esports."
    elif "Creator" in mode:
        return f"Studio quality in your pocket. **{row['name']}** features a class-leading camera system for professional content creation."
    elif "Student" in mode:
        return f"Maximum efficiency per dollar. **{row['name']}** outperforms its price bracket, offering flagship features at an entry-level investment."
    else:
        return f"The perfect daily driver. **{row['name']}** offers a balanced synergy of speed, battery life, and build quality."

def stat_bar_html(label, score, color):
    percent = score * 10
    return f"""
    <div class="stat-box">
        <div class="stat-label">{label}</div>
        <div class="stat-value">{score}/10</div>
        <div class="stat-bar-bg">
            <div class="stat-bar-fill" style="width:{percent}%; background:{color};"></div>
        </div>
    </div>
    """

# --- 6. MAIN LOGIC ---
df = load_data()

if not df.empty:
    if "iOS" in os_choice: df = df[df['os_type'] == 'iOS']
    elif "Android" in os_choice: df = df[df['os_type'] == 'Android']
    df = df[df['price'] <= budget]

    df['score'] = (df['performance']*p) + (df['camera']*c) + (df['battery']*b) + (df['value']*v)
    max_score = (10*p) + (10*c) + (10*b) + (10*v)
    df['match'] = (df['score'] / max_score) * 100
    df = df.sort_values(by='match', ascending=False).reset_index(drop=True)

    if len(df) > 0:
        winner = df.iloc[0]
        c1, c2 = st.columns([1.3, 1], gap="large")

        # --- WINNER SECTION ---
        with c1:
            st.markdown(f"""
            <div class='winner-card'>
                <span class='rank-badge'>🏆 #1 Top Recommendation</span>
                <div class='hero-name'>{winner['name']}</div>
                <div class='hero-price'>${winner['price']:,}</div>
                
                <div style='margin-bottom:25px; color:#94A3B8; line-height:1.6;'>
                    {generate_pro_verdict(winner, lifestyle)}
                </div>
                
                <div class="stat-grid">
                    {stat_bar_html("🚀 Performance", winner['performance'], "#3B82F6")}
                    {stat_bar_html("📸 Camera", winner['camera'], "#A855F7")}
                    {stat_bar_html("🔋 Battery", winner['battery'], "#22C55E")}
                </div>

                <a href="{winner['link']}" target="_blank" class="cta-btn">
                    🛒 Check Current Price on Amazon
                </a>
            </div>
            """, unsafe_allow_html=True)

        # --- ALTERNATIVES SECTION ---
        with c2:
            st.markdown("### 📊 Market Comparison")
            st.markdown(f"<div style='color:#64748B; margin-bottom:15px;'>Filtered for budget: < ${budget:,}</div>", unsafe_allow_html=True)
            
            for i, row in df.iloc[1:5].iterrows():
                diff = winner['price'] - row['price']
                save_tag = f"<span style='color:#4ADE80; font-size:0.8em; font-weight:bold;'>Save ${diff:,}</span>" if diff > 0 else ""
                
                st.markdown(f"""
                <div class='alt-row'>
                    <div>
                        <div style='font-weight:700; font-size:1.1em; color:#F1F5F9;'>{i}. {row['name']}</div>
                        <div style='color:#94A3B8; font-size:0.9em;'>Est. ${row['price']:,} &nbsp; {save_tag}</div>
                    </div>
                    <div style='text-align:right;'>
                        <div style='font-size:1.2em; font-weight:900; color:#3B82F6;'>{row['match']:.0f}%</div>
                        <a href="{row['link']}" target="_blank" style='color:#F59E0B; text-decoration:none; font-size:0.8em; font-weight:600;'>View Deal ></a>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    else:
        st.warning("No devices found in this range.")
else:
    st.error("Data Source Error")