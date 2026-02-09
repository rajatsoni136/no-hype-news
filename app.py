import streamlit as st
import pandas as pd

# 1. PAGE CONFIGURATION
st.set_page_config(
    page_title="No-Hype News",
    page_icon="📰",
    layout="centered"
)

# 2. LOAD DATA
def load_data():
    try:
        df = pd.read_csv("final_feed.csv")
        return df
    except FileNotFoundError:
        return pd.DataFrame()

df = load_data()

# 3. TITLE & SIDEBAR
st.title("📰 The No-Hype News Feed")
st.markdown("### AI-Filtered News: Pure Facts, No Clickbait.")

# Sidebar for filters
with st.sidebar:
    st.header("Filters")
    if not df.empty:
        # Category Filter
        categories = ["All"] + list(df['category'].unique())
        selected_category = st.selectbox("Category", categories)
        
        # Hype Score Slider
        min_hype = st.slider("Max Hype Score Allowed", 1, 10, 10)
    else:
        selected_category = "All"
        min_hype = 10

    st.markdown("---")
    st.caption("Built with LangChain, OpenAI & Streamlit")

# 4. MAIN FEED DISPLAY
if df.empty:
    st.warning("No data found. Please run the processor script first!")
else:
    # Apply Filters
    if selected_category != "All":
        df = df[df['category'] == selected_category]
    
    df = df[df['hype_score'] <= min_hype]

    # Display Articles
    for index, row in df.iterrows():
        # Create a card-like container
        with st.container():
            col1, col2 = st.columns([3, 1])
            
            with col1:
                # The New, Boring Title (Big & Bold)
                st.subheader(row['new_title'])
                
                # The Original Clickbait Title (Small & Grey)
                st.caption(f"Original: {row['original_title']}")
                
                # The "Why" (Explain the Clickbait)
                if pd.notna(row['clickbait_element']):
                    st.markdown(f"**🚫 Clickbait Removed:** `{row['clickbait_element']}`")
                
                # Link
                st.markdown(f"[Read Source Article]({row['original_link']})")
            
            with col2:
                # The Score Card
                if row['hype_score'] > 7:
                    color = "red"
                elif row['hype_score'] > 4:
                    color = "orange"
                else:
                    color = "green"
                
                st.markdown(f":{color}[**Hype Score**]")
                st.markdown(f"## :{color}[{row['hype_score']}/10]")
                st.markdown(f"*{row['category']}*")

        st.divider()