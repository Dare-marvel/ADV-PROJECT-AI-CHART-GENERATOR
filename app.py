import streamlit as st
import pandas as pd
import os
from utils import generate_visualizations, get_gemini_response_multiple, parse_gemini_response_multiple, get_gemini_response, parse_gemini_response
from dotenv import load_dotenv

load_dotenv()

# Set up Google Gemini API key
GENAI_API_KEY = os.getenv("GEMINI_API_KEY")  # Replace with your actual Gemini API key

# Set up the page configuration
st.set_page_config(
    page_title="StellarData - Data Visualization and Insights",
    page_icon="✨",
    layout="wide"
)

# Apply a sci-fi theme with custom HTML and CSS
def sci_fi_theme():
    st.markdown("""
        <style>
        body {
            background-color: #000d1a;
            font-family: 'Orbitron', sans-serif;
            color: #00eaff;
            overflow-x: hidden;
        }
        h1, h2, h3, h4, h5, h6 {
            text-transform: uppercase;
            color: #00eaff;
            text-shadow: 0 0 20px #00eaff, 0 0 30px #004080;
        }
        .stButton>button {
            background: linear-gradient(135deg, #00eaff 30%, #004080 90%);
            border: none;
            color: white;
            padding: 10px 20px;
            font-size: 1rem;
            text-transform: uppercase;
            box-shadow: 0 0 15px #00eaff;
        }
        .stButton>button:hover {
            background: linear-gradient(135deg, #004080 30%, #00eaff 90%);
            box-shadow: 0 0 30px #00eaff;
        }
        .stFileUploader label {
            color: #00eaff;
        }
        .stTextInput>div {
            background: rgba(0, 0, 50, 0.8);
            color: white;
            border: 1px solid #00eaff;
            border-radius: 10px;
            box-shadow: 0 0 20px #00eaff;
        }
        .css-1aumxhk {
            background-color: #002b5c !important;
            box-shadow: 0 0 30px #00eaff;
        }
        </style>
        <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap" rel="stylesheet">
    """, unsafe_allow_html=True)


# Apply the sci-fi theme
sci_fi_theme()


# Title and Description
st.title("🌌 StellarData: AI-Powered Data Visualization Tool")
st.markdown("""
    **StellarData** is your gateway to the future of data visualization. Powered by AI, it brings to life
    the hidden patterns in your datasets through stunning and insightful visualizations. Simply upload your CSV file,
    ask natural language questions, and let the magic unfold. 🚀
""")

# File upload for CSV
uploaded_file = st.file_uploader("Upload a CSV file", type="csv")
if uploaded_file is not None:
    # Load and display the uploaded dataset
    df = pd.read_csv(uploaded_file)
    st.write("### Dataset Preview")
    st.dataframe(df.head(), width=1000)  # Adjusted the size for a larger display
    
    # Natural language query input
    st.write("### Ask a question about the dataset:")
    query = st.text_input("Type your question here:")
    if query:
        # Get response from Gemini model
        response = get_gemini_response(query, df, GENAI_API_KEY)
        st.subheader("🧠 Gemini's Answer")
        st.write(response)

        # Parse the response to get chart details
        chart_type, chart_code, x_label, y_label = parse_gemini_response(response)

        # Generate and display the visualizations
        generate_visualizations(df, chart_type, chart_code, x_label, y_label)

    # Generate 5 initial visualizations based on the dataset
    st.write("### Important visualizations from the dataset:")
    
    # Get 5 visualizations in one go from the model
    response = get_gemini_response_multiple(df, GENAI_API_KEY)
    
    # Parse the response to get chart details
    visualizations = parse_gemini_response_multiple(response)
    for chart_type, chart_code, x_label, y_label in visualizations:
        # Generate and display each visualization
        generate_visualizations(df, chart_type, chart_code, x_label, y_label)
