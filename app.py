import streamlit as st
import json
from PIL import Image

# Load data
with open('genes.json') as f:
    genes_data = json.load(f)['genes']

with open('structures.json') as f:
    structures_data = json.load(f)['structures']

# Function to get gene information
def get_gene_info(gene_name):
    for gene in genes_data:
        if gene["Gene"] == gene_name:
            return gene
    return None

# Custom CSS to adjust the layout
st.markdown(
    """
    <style>
        /* Generic selector to target the sidebar directly */
        .css-1e5imcs {
             width: 400px !important; /* Adjust the width here */
         }
        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 1rem;
            padding-left: 0rem;
            padding-right: 60rem;
        }
        .map-container {
            display: flex;
            justify-content: center;
            align-items: center;
            height: auto;
            width: 80%;
            margin: 0 auto;
            padding: 0;
        }
        .stImage > img {
            max-width: 100%;
            height: auto;
        }
        .main > div:first-child h1 {
            font-size: 30px;
            margin-bottom: 20px;
            text-align: center;
            margin-left: 250px;
        }
        .sidebar .block-container .st-bx {
            padding-left: 0px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Central area for the map
st.title("Cilia Structure Map")
map_image = Image.open("map.png")
st.image(map_image, width=900)

# Sidebar interaction for search
st.sidebar.title("Search and Filter")
search_option = st.sidebar.selectbox("Search by", ["Gene", "Structure"])

if search_option == "Gene":
    gene_name = st.sidebar.text_input("Enter gene name")
    if gene_name:
        gene_info = get_gene_info(gene_name)
        if gene_info:
            st.sidebar.header(f"Gene Information: {gene_info['Gene']}")
            for key, value in gene_info.items():
                if value and value != "None":  # Exclude elements with value "None"
                    if isinstance(value, dict):  # Check if the value is a dictionary
                        if value['references'] and value['references'] != "None":
                            st.sidebar.markdown(f"**{key}**: {value['text']}<sup>{value['references']}</sup>", unsafe_allow_html=True)
                        else:
                            st.sidebar.markdown(f"**{key}**: {value['text']}")
                    elif isinstance(value, list):  # Check if the value is a list
                        for item in value:
                            if item['references'] and item['references'] != "None":
                                st.sidebar.markdown(f"**{key}**: {item['text']}<sup>{item['references']}</sup>", unsafe_allow_html=True)
                            else:
                                st.sidebar.markdown(f"**{key}**: {item['text']}")
                    else:
                        st.sidebar.markdown(f"**{key}**: {value}")
        else:
            st.sidebar.write("Gene not found.")



