import streamlit as st  # type: ignore
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set the page configuration
st.set_page_config(
    page_title="Your HR Satya",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Title of the Dashboard
st.title("📊 Your HR Satya")

# Sidebar for File Upload and Filters
st.sidebar.header("🔽 Upload and Filter Data")

def load_data():
    """
    Function to load data from an uploaded Excel file.
    """
    uploaded_file = st.sidebar.file_uploader(
        "Upload your Excel file here",
        type=["xlsx", "xls"],
        help="Ensure the Excel file has 'id' and 'score' columns."
    )
    if uploaded_file is not None:
        try:
            df = pd.read_excel(uploaded_file, engine='openpyxl')
            # Validate columns
            if 'id' not in df.columns or 'score' not in df.columns:
                st.sidebar.error("The Excel file must contain 'id' and 'score' columns.")
                return None
            # Convert 'id' column to string
            df['id'] = df['id'].astype(str)
            # Convert 'score' column to numeric, forcing errors to NaN
            df['score'] = pd.to_numeric(df['score'], errors='coerce')
            # Drop rows where 'score' is NaN (i.e., conversion failed)
            df = df.dropna(subset=['score'])
            # Handle 'outliers' column if it exists
            if 'outliers' in df.columns:
                # Ensure 'outliers' is numeric
                df['outliers'] = pd.to_numeric(df['outliers'], errors='coerce').fillna(0).astype(int)
                # Create a 'Flagged' column
                df['Flagged'] = df['outliers'].apply(lambda x: 'Yes' if x == 1 else 'No')
            else:
                df['Flagged'] = 'No'
            return df
        except Exception as e:
            st.sidebar.error(f"Error loading Excel file: {e}")
            return None
    else:
        return None

# Function to highlight flagged candidates
def highlight_flagged(s):
    return ['background-color: yellow' if v == 'Yes' else '' for v in s]

# Load data
data = load_data()

if data is not None:
    # Display the DataFrame
    st.subheader("📋 Data Overview")
    st.dataframe(
        data.style
        .apply(highlight_flagged, subset=['Flagged'], axis=0)
        .highlight_max(subset=['score'], axis=0),
        height=300
    )

    # Sidebar Filters
    st.sidebar.subheader("📊 Filter Options")

    # Score Range Filter
    min_score = float(data['score'].min())
    max_score = float(data['score'].max())
    score_range = st.sidebar.slider(
        "Select Score Range",
        min_value=min_score,
        max_value=max_score,
        value=(min_score, max_score),
        step=1.0
    )

    # ID Search
    id_search = st.sidebar.text_input("Search by ID", "")

    # Filtered DataFrame
    filtered_data = data[
        (data['score'] >= score_range[0]) & 
        (data['score'] <= score_range[1]) & 
        (data['id'].str.contains(id_search))
    ]

    st.subheader("🔍 Filtered Data")
    st.write(f"Showing *{filtered_data.shape[0]}* records")
    st.dataframe(
        filtered_data.style
        .apply(highlight_flagged, subset=['Flagged'], axis=0)
        .highlight_max(subset=['score'], axis=0),
        height=300
    )

    # Visualization Section
    st.subheader("📈 Score Distribution")

    # Histogram
    fig_hist, ax_hist = plt.subplots(figsize=(10, 4))
    sns.histplot(data['score'], bins=20, kde=True, color='skyblue', ax=ax_hist)
    ax_hist.set_title('Histogram of Scores')
    ax_hist.set_xlabel('Score')
    ax_hist.set_ylabel('Frequency')
    st.pyplot(fig_hist)

    # Box Plot
    fig_box, ax_box = plt.subplots(figsize=(10, 2))
    sns.boxplot(x=data['score'], color='lightgreen', ax=ax_box)
    ax_box.set_title('Box Plot of Scores')
    st.pyplot(fig_box)

    # Top Performers
    st.subheader("🏆 Top Performers")
    top_n = st.slider("Select number of top performers to display", min_value=1, max_value=100, value=10)
    top_performers = data.nlargest(top_n, 'score')
    st.dataframe(
        top_performers.style
        .apply(highlight_flagged, subset=['Flagged'], axis=0)
        .highlight_max(subset=['score'], axis=0),
        height=300
    )

    # Compare Candidates
    st.subheader("🔎 Compare Candidates")
    candidate_ids = data['id'].unique()

    if len(candidate_ids) >= 2:
        candidate1_id = st.selectbox("Select Candidate 1", candidate_ids)
        candidate2_ids = [id for id in candidate_ids if id != candidate1_id]
        candidate2_id = st.selectbox("Select Candidate 2", candidate2_ids)

        if candidate1_id and candidate2_id:
            candidate1 = data[data['id'] == candidate1_id].iloc[0]
            candidate2 = data[data['id'] == candidate2_id].iloc[0]

            # Exclude the 'id' column in the attributes
            attributes = [col for col in data.columns if col != 'id']

            st.write("### Comparison of Selected Candidates")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"#### Candidate 1: {candidate1_id}")
                st.write(candidate1[attributes].to_frame())
            with col2:
                st.markdown(f"#### Candidate 2: {candidate2_id}")
                st.write(candidate2[attributes].to_frame())
    else:
        st.info("Not enough candidates to compare.")

    # Download Filtered Data
    st.subheader("⬇ Download Filtered Data")
    def convert_df(df):
        """
        Convert DataFrame to CSV for download.
        """
        return df.to_csv(index=False).encode('utf-8')

    csv = convert_df(filtered_data)

    st.download_button(
        label="📥 Download Filtered Data as CSV",
        data=csv,
        file_name='filtered_data.csv',
        mime='text/csv',
    )

else:
    st.info("Awaiting Excel file to be uploaded. Please upload a file to proceed.")