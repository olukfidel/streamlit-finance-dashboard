import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# --- PAGE CONFIGURATION ---
# Sets the title, icon, layout, and an initial message for the sidebar.
st.set_page_config(
    page_title="USA State Finance Dashboard",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- STYLING ---
# Custom CSS to inject for a more modern look.
st.markdown("""
<style>
    /* Main app background */
    .main {
        background-color: #f5f5f5;
    }
    /* Styling for headers */
    h1, h2, h3 {
        color: #1a1a1a;
    }
    /* Custom button style */
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 8px;
        border: none;
    }
    /* Customizing the tabs for a cleaner look */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #e0e0e0;
        border-radius: 4px 4px 0px 0px;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #f5f5f5;
    }
</style>
""", unsafe_allow_html=True)


# --- DATA LOADING ---
# Caching the data loading function for performance.
@st.cache_data
def load_data(uploaded_file):
    """Loads data from the uploaded CSV file."""
    try:
        df = pd.read_csv(uploaded_file)
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

# --- PLOTTING FUNCTIONS ---
# Each function corresponds to one of the original scripts.

def plot_revenue_vs_expenditure(df, state, year):
    """Plots a bar chart comparing total revenue and expenditure for a selected state and year."""
    df_melted = pd.melt(df,
                        id_vars=['State', 'Year'],
                        value_vars=['Totals.Revenue', 'Totals.Expenditure'],
                        var_name='Metric',
                        value_name='Amount')
    df_melted['Metric'] = df_melted['Metric'].str.replace('Totals.', '', regex=False)

    filtered_data = df_melted[(df_melted['State'] == state) & (df_melted['Year'] == year)]

    if filtered_data.empty:
        st.warning(f"No data available for {state} in {year}. Please select another combination.")
        return

    fig, ax = plt.subplots(figsize=(8, 6))
    sns.barplot(x='Metric', y='Amount', data=filtered_data, ax=ax, palette=['#4CAF50', '#F44336'])
    
    ax.set_title(f'Revenue vs. Expenditure for {state} in {year}', fontsize=16, weight='bold')
    ax.set_xlabel('Metric', fontsize=12)
    ax.set_ylabel('Amount (in USD)', fontsize=12)
    ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, p: format(int(x), ',')))
    plt.tight_layout()
    st.pyplot(fig)

def plot_expenditure_trends(df, state):
    """Plots line charts for health and education expenditure trends for a selected state."""
    health_col = 'Details.Health.Health Total Expenditure'
    edu_col = 'Details.Education.Education Total'

    # Check if required columns exist
    if health_col not in df.columns or edu_col not in df.columns:
        st.error("Error: Required expenditure columns not found in the dataset.")
        return

    state_data = df[df['State'] == state].sort_values('Year')

    if state_data.empty:
        st.warning(f"No data available for the state: {state}.")
        return

    col1, col2 = st.columns(2)

    with col1:
        fig1, ax1 = plt.subplots(figsize=(10, 6))
        sns.lineplot(x='Year', y=health_col, data=state_data, marker='o', linewidth=2.5, ax=ax1, color='dodgerblue')
        ax1.set_title(f'Health Expenditure Trend for {state}', fontsize=16, weight='bold')
        ax1.set_xlabel('Year', fontsize=12)
        ax1.set_ylabel('Total Health Expenditure (USD)', fontsize=12)
        ax1.grid(True, which='both', linestyle='--', linewidth=0.5)
        ax1.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, p: format(int(x), ',')))
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(fig1)

    with col2:
        fig2, ax2 = plt.subplots(figsize=(10, 6))
        sns.lineplot(x='Year', y=edu_col, data=state_data, marker='o', linewidth=2.5, ax=ax2, color='orange')
        ax2.set_title(f'Education Expenditure Trend for {state}', fontsize=16, weight='bold')
        ax2.set_xlabel('Year', fontsize=12)
        ax2.set_ylabel('Total Education Expenditure (USD)', fontsize=12)
        ax2.grid(True, which='both', linestyle='--', linewidth=0.5)
        ax2.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, p: format(int(x), ',')))
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(fig2)

def plot_revenue_rankings(df, year):
    """Plots bar charts for the top 10 and bottom 10 states by revenue for a selected year."""
    df_year = df[df['Year'] == year]

    if df_year.empty:
        st.warning(f"No data available for the year: {year}.")
        return

    state_revenues = df_year.groupby('State')['Totals.Revenue'].sum().sort_values(ascending=False)
    top_10_states = state_revenues.head(10)
    bottom_10_states = state_revenues.tail(10).sort_values(ascending=True)

    fig, axes = plt.subplots(2, 1, figsize=(12, 18))
    fig.suptitle(f'State Revenue Rankings for {year}', fontsize=20, weight='bold', y=1.02)
    
    # Top 10 Plot
    sns.barplot(x=top_10_states.values, y=top_10_states.index, ax=axes[0], palette='viridis')
    axes[0].set_title('Top 10 States by Revenue Collection', fontsize=16)
    axes[0].set_xlabel('Total Revenue (in USD)', fontsize=12)
    axes[0].set_ylabel('State', fontsize=12)
    axes[0].ticklabel_format(style='plain', axis='x')

    # Bottom 10 Plot
    sns.barplot(x=bottom_10_states.values, y=bottom_10_states.index, ax=axes[1], palette='plasma_r')
    axes[1].set_title('Bottom 10 States by Revenue Collection', fontsize=16)
    axes[1].set_xlabel('Total Revenue (in USD)', fontsize=12)
    axes[1].set_ylabel('State', fontsize=12)
    axes[1].ticklabel_format(style='plain', axis='x')

    plt.tight_layout(rect=[0, 0, 1, 0.98])
    st.pyplot(fig)


# --- MAIN APPLICATION ---

st.title("💰 USA State Financial Analysis Dashboard")
st.markdown("An interactive dashboard to explore and visualize financial data of US states over the years.")

# --- SIDEBAR ---
# Contains the file uploader and dynamic filters.
with st.sidebar:
    st.header("⚙️ Controls & Filters")
    uploaded_file = st.file_uploader("Upload your finance CSV file", type=["csv"])

    if uploaded_file is not None:
        df = load_data(uploaded_file)
        if df is not None:
            st.success("File loaded successfully!")
            
            # Get unique values for filters
            states = sorted(df['State'].unique())
            years = sorted(df['Year'].unique())
            
            # Create interactive widgets
            selected_state = st.selectbox("Select a State", states)
            selected_year = st.select_slider("Select a Year", options=years, value=years[-1]) # Default to the latest year
    else:
        st.info("Awaiting for a CSV file to be uploaded.")
        st.stop()


# --- TABS FOR DIFFERENT VISUALIZATIONS ---
tab1, tab2, tab3 = st.tabs(["📊 Revenue vs. Expenditure", "📈 Expenditure Trends", "🏆 State Rankings"])

with tab1:
    st.header(f"Revenue vs. Expenditure Analysis for {selected_state}")
    st.markdown(f"Comparing total revenue against total expenditure for the year **{selected_year}**.")
    plot_revenue_vs_expenditure(df, selected_state, selected_year)

with tab2:
    st.header(f"Health & Education Expenditure Trends for {selected_state}")
    st.markdown("Visualizing how spending on key sectors has evolved over the years.")
    plot_expenditure_trends(df, selected_state)

with tab3:
    st.header(f"State Revenue Rankings for {selected_year}")
    st.markdown("Discover the top 10 and bottom 10 states by total revenue collection.")
    plot_revenue_rankings(df, selected_year)