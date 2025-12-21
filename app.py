import streamlit as st
import pandas as pd
import plotly.graph_objects as go # พระเอกของเรา (กราฟแมงมุม)

# --- 1. CONFIG ---
st.set_page_config(
    page_title="TechChoose - Pro Analyst",
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

# --- 3. PRO CSS (Data Viz Style) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Inter:wght@400;600;800&display=swap');
    
    .stApp { background-color: #0B0E14; color: #E2E8F0; font-family: 'Inter', sans-serif; }
    
    /* Sidebar */
    section[data-testid="stSidebar"] { background-color: #050505; border-right: 1px solid #1E1E1E; }
    section[data-testid="stSidebar"] div[data-baseweb="select"] > div { background-color: #1A1A1A !important; color: white !important; border: 1px solid #333; }
    
    /* Winner Card */
    .winner-card {
        background: #11151C;
        border: 1px solid #3B82F6; border-left: 5px solid #3B82F6;
        border-radius: 12px; padding: 30px;
        box-shadow: 0 4px 30px rgba(59, 130, 246, 0.1);
    }
    
    .hero-name {
        font-family: 'Inter', sans-serif;
        font-size: 3.5em; font-weight: 900; letter-spacing: -1px;
        background: -webkit-linear-gradient(0deg, #fff, #94A3B8);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 5px;
    }
    
    .price-tag {
        font-family: 'JetBrains Mono', monospace;
        color: #FBBF24; font-size: 1.8em; font-weight: bold;
    }
    
    .tier-badge {
        background: #333; color: #aaa; padding: 2px 8px; border-radius: 4px;
        font-size: 0.5em; vertical-align: middle; margin-left: 10px;
        font-family: 'JetBrains Mono', monospace;
    }

    /* Tags */
    .spec-tag {
        display: inline-block; background: #1E293B; color: #94A3B8;
        padding: 5px 12px; border-radius: 20px; font-size: 0.85em; margin-right: 5px; margin-top: 10px;
        border: 1px solid #334155;
    }

    /* Button */
    .amazon-btn {
        background: #F59E0B; color: black !important; padding: 15px 40px; 
        border-radius: 4px; text-decoration: none; font-weight: 800; 
        display: inline-block; margin-top: 25px; text-transform: uppercase; letter-spacing: 1px;
        transition: 0.2s;
    }
    .amazon-btn:hover { background: #fff; box-shadow: 0 0 20px rgba(255,255,255,0.3); }

    /* Alternatives */
    .alt-row {
        background: #11151C; border-bottom: 1px solid #222;
        padding: 20px; display: flex; justify-content: space-between; align-items: center;
        transition: 0.2s;
    }
    .alt-row:hover { background: #1A1F29; border-left: 3px solid #F59E0B; }
    
</style>
""", unsafe_allow_html=True)

# --- 4. GRAPH FUNCTION (RADAR CHART) ---
def create_radar_chart(row):
    categories = ['Performance', 'Camera', 'Battery', 'Value']
    values = [row['performance'], row['camera'], row['battery'], row['value']]
    
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        fillcolor='rgba(59, 130, 246, 0.2)',
        line_color='#3B82F6',
        linewidth=2
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 10], color='#555'),
            bgcolor='rgba(0,0,0,0)'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=20, b=20),
        height=300,
        font=dict(color='#E2E8F0', family="Inter")
    )
    return fig

def get_price_tier(price):
    if price < 500: return "$"
    elif price < 800: return "$$"
    elif price < 1100: return "$$$"
    else: return "$$$$"

# --- 5. SIDEBAR ---
with st.sidebar:
    st.title("⚡ TechChoose")
    st.caption("ANALYTICS MODE")
    st.write("---")
    
    os_choice = st.selectbox("OPERATING SYSTEM", ["Any", "iOS", "Android"])
    st.write("")
    lifestyle = st.selectbox("TARGET USER", ["🎮 Gamer", "📸 Creator", "💼 Pro", "💰 Student", "🛠️ Custom"])
    st.write("")
    budget = st.slider("MAX BUDGET (USD)", 300, 2000, 2000, step=50)

    # Weights
    p, c, b, v = 5, 5, 5, 5
    if "Gamer" in lifestyle: p,c,b,v = 10,3,8,5
    elif "Creator" in lifestyle: p,c,b,v = 7,10,8,5
    elif "Pro" in lifestyle: p,c,b,v = 8,6,9,6
    elif "Student" in lifestyle: p,c,b,v = 5,5,7,10
    else: 
        p = st.slider("Perf", 1,10,8)
        c = st.slider("Cam", 1,10,8)
        b = st.slider("Batt", 1,10,5)
        v = st.slider("Value", 1,10,5)
    
    st.divider()
    st.button("RUN ANALYSIS", type="primary", use_container_width=True)

# --- 6. MAIN APP ---
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
        c1, c2 = st.columns([1.5, 1], gap="large")

        with c1:
            tier = get_price_tier(winner['price'])
            st.markdown(f"""
            <div class='winner-card'>
                <div style='color:#3B82F6; font-weight:bold; letter-spacing:2px; font-size:0.8em; margin-bottom:10px;'>TOP ANALYST PICK</div>
                <div class='hero-name'>{winner['name']}</div>
                <div class='price-tag'>
                    ${winner['price']:,} <span class='tier-badge'>{tier} Tier</span>
                </div>
                <div style='margin-top:20px;'>
                    <span class='spec-tag'>🚀 Speed {winner['performance']}/10</span>
                    <span class='spec-tag'>📸 Cam {winner['camera']}/10</span>
                    <span class='spec-tag'>🔋 Batt {winner['battery']}/10</span>
                </div>
                <p style='margin-top:25px; color:#94A3B8; line-height:1.6;'>
                    Based on your requirements for <b>{lifestyle}</b>, this device offers the optimal balance of specifications. 
                    It achieves a <b>{winner['match']:.1f}% match score</b> against our algorithm.
                </p>
                <a href="{winner['link']}" target="_blank" class="amazon-btn">VIEW OFFER ></a>
            </div>
            """, unsafe_allow_html=True)

        with c2:
            # 🔥 ตรงนี้คือทีเด็ด: กราฟแมงมุม 🔥
            st.markdown("### 📊 Performance Profile")
            fig = create_radar_chart(winner)
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
            
            # Alternatives Table
            st.markdown("### 📉 Market Alternatives")
            for i, row in df.iloc[1:5].iterrows():
                diff = winner['price'] - row['price']
                save_tag = f"<span style='color:#4ADE80; font-weight:bold;'>Save ${diff:,}</span>" if diff > 0 else ""
                
                st.markdown(f"""
                <div class='alt-row'>
                    <div>
                        <div style='font-weight:bold; font-size:1.1em;'>{i}. {row['name']}</div>
                        <div style='color:#666; font-family:"JetBrains Mono"; font-size:0.9em;'>${row['price']:,}</div>
                    </div>
                    <div style='text-align:right;'>
                        <div style='color:#3B82F6; font-weight:bold;'>{row['match']:.0f}%</div>
                        <a href="{row['link']}" target="_blank" style='color:#F59E0B; text-decoration:none; font-size:0.8em;'>View</a>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
    else:
        st.warning(f"No match found under ${budget}")
else:
    st.error("Data Error")