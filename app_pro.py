import streamlit as st
import pandas as pd
import plotly.express as px
from urllib.parse import urlparse

# 1. PAGE CONFIGURATION (Must be the first command)
st.set_page_config(
    page_title="No-Hype News",
    page_icon="🛡️",
    layout="wide",  # Use the full screen width
    initial_sidebar_state="expanded"
)

# Custom CSS to make cards look modern
st.markdown("""
<style>
    .stMetric {
        background-color: #0E1117;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #262730;
    }
    .css-1r6slb0 {
        border: 1px solid #262730;
        padding: 20px;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# 2. HELPER FUNCTIONS
def load_data():
    try:
        df = pd.read_csv("final_feed.csv")
        # Extract domain from URL (e.g., 'theverge.com')
        df['source'] = df['original_link'].apply(lambda x: urlparse(x).netloc.replace('www.', ''))
        return df
    except FileNotFoundError:
        return pd.DataFrame()

def get_hype_color(score):
    if score > 7: return "red"
    if score > 4: return "orange"
    return "green"

# 3. LOAD DATA
df = load_data()

# 4. SIDEBAR FILTERS
with st.sidebar:
    st.title("🛡️ No-Hype News")
    st.markdown("---")
    
    if not df.empty:
        # Category Filter
        categories = ["All"] + list(df['category'].unique())
        selected_category = st.selectbox("📂 Filter by Category", categories)
        
        # Hype Slider
        max_hype = st.slider("🚫 Max Hype Allowed", 1, 10, 10, help="Filter out sensationalist articles")
        
        # Source Filter
        sources = ["All"] + list(df['source'].unique())
        selected_source = st.selectbox("🌐 Filter by Source", sources)
        
        st.markdown("---")
        st.caption(f"Loaded {len(df)} articles processed by Llama 3.")

# 5. MAIN DASHBOARD
if df.empty:
    st.warning("⚠️ No data found. Please run the `processor.py` script first.")
else:
    # --- FILTERING LOGIC ---
    filtered_df = df.copy()
    if selected_category != "All":
        filtered_df = filtered_df[filtered_df['category'] == selected_category]
    if selected_source != "All":
        filtered_df = filtered_df[filtered_df['source'] == selected_source]
    filtered_df = filtered_df[filtered_df['hype_score'] <= max_hype]

    # --- TABS FOR DIFFERENT VIEWS ---
    tab1, tab2 = st.tabs(["📰 News Feed", "📊 Analytics"])

    with tab1:
        # Top Metrics Row
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Articles", len(filtered_df))
        col2.metric("Avg Hype Score", f"{filtered_df['hype_score'].mean():.1f}/10")
        col3.metric("Clickbait Avoided", len(df[df['hype_score'] > 7]))
        col4.metric("Sources Tracked", df['source'].nunique())

        st.divider()

        # News Cards
        for index, row in filtered_df.iterrows():
            with st.container():
                c1, c2 = st.columns([5, 1])
                
                with c1:
                    # Source Badge
                    st.caption(f"🌐 {row['source']} • {row['category']}")
                    
                    # Main Title
                    st.markdown(f"### {row['new_title']}")
                    
                    # Expander for details (Keeps UI clean)
                    with st.expander("👀 See Original Clickbait & Analysis"):
                        st.markdown(f"**Original Title:** *{row['original_title']}*")
                        if pd.notna(row['clickbait_element']):
                            st.error(f"**Clickbait Element:** {row['clickbait_element']}")
                        st.info(f"**Core Fact:** {row['main_fact']}")
                        st.markdown(f"[Read Full Article]({row['original_link']})")
                
                with c2:
                    # Score Circle
                    color = get_hype_color(row['hype_score'])
                    st.markdown(f"""
                        <div style="text-align: center; border: 2px solid {color}; border-radius: 10px; padding: 10px;">
                            <h2 style="color: {color}; margin:0;">{row['hype_score']}</h2>
                            <small>Hype Score</small>
                        </div>
                    """, unsafe_allow_html=True)
                
                st.divider()

    with tab2:
        st.header("📊 Hype Analytics")
        
        c1, c2 = st.columns(2)
        
        with c1:
            st.subheader("Hype by Category")
            fig_cat = px.box(df, x="category", y="hype_score", color="category", points="all")
            st.plotly_chart(fig_cat, use_container_width=True)
            
        with c2:
            st.subheader("Worst Offenders (Avg Hype Score)")
            source_hype = df.groupby("source")['hype_score'].mean().sort_values(ascending=False).reset_index()
            fig_source = px.bar(source_hype, x="source", y="hype_score", color="hype_score", color_continuous_scale="RdYlGn_r")
            st.plotly_chart(fig_source, use_container_width=True)