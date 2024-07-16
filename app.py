import streamlit as st
import json
from PIL import Image

# Load data
with open('genes.json') as f:
    genes_data = json.load(f)['genes']

with open('structures.json') as f:
    structures_data = json.load(f)['structures']

with open('references.json') as f:
    references_data = json.load(f)['references']

# Function to get gene information
def get_gene_info(gene_name):
    for gene in genes_data:
        if gene["Gene"] == gene_name:
            return gene
    return None

# Function to get full citation from references
def get_full_citation(ref_number):
    return references_data.get(ref_number, None)

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

# if search_option == "Gene":
#     gene_name = st.sidebar.text_input("Enter gene name")
#     if gene_name:
#         gene_info = get_gene_info(gene_name)
#         if gene_info:
#             st.sidebar.header(f"Gene Information: {gene_info['Gene']}")
#             used_references = set()
#             for key, value in gene_info.items():
#                 if value and value != "None":  # Exclude elements with value "None"
#                     if isinstance(value, dict):  # Check if the value is a dictionary
#                         if value['references'] and value['references'] != "None":
#                             st.sidebar.markdown(f"**{key}**: {value['text']}<sup>{value['references']}</sup>", unsafe_allow_html=True)
#                             for ref in value['references'].split(','):
#                                 used_references.add(ref.strip())
#                         else:
#                             st.sidebar.markdown(f"**{key}**: {value['text']}")
#                     elif isinstance(value, list):  # Check if the value is a list
#                         for item in value:
#                             if item['references'] and item['references'] != "None":
#                                 st.sidebar.markdown(f"**{key}**: {item['text']}<sup>{item['references']}</sup>", unsafe_allow_html=True)
#                                 for ref in item['references'].split(','):
#                                     used_references.add(ref.strip())
#                             else:
#                                 st.sidebar.markdown(f"**{key}**: {item['text']}")
#                     else:
#                         st.sidebar.markdown(f"**{key}**: {value}")
#
#             # Display the references used
#             if used_references:
#                 st.sidebar.header("References")
#                 for ref in sorted(used_references):
#                     full_citation = get_full_citation(ref)
#                     if full_citation:
#                         st.sidebar.markdown(f"<sup>{ref}</sup> {full_citation}", unsafe_allow_html=True)
#         else:
#             st.sidebar.write("Gene not found.")
# elif search_option == "Structure":
#     structure_name = st.sidebar.selectbox("Select structure to view genes:", ["Select a structure"] + list(structures_data.keys()))
#     if structure_name and structure_name != "Select a structure":
#         genes_list = structures_data[structure_name]
#         st.sidebar.header(f"Genes in {structure_name}:")
#         for gene in genes_list:
#             gene_info = get_gene_info(gene)
#             if gene_info:
#                 st.sidebar.write(f"{gene_info['Gene']} - {gene_info['Locus']}")

if search_option == "Gene":
    gene_name = st.sidebar.text_input("Enter gene name")
    if gene_name:
        gene_info = get_gene_info(gene_name)
        if gene_info:
            st.sidebar.header(f"**{gene_info['Gene']}**")

            with st.sidebar.expander("**Gene Information**"):
                used_references = set()
                for key, value in gene_info.items():
                    if value and value != "None":  # Exclude elements with value "None"
                        if isinstance(value, dict):  # Check if the value is a dictionary
                            if value['references'] and value['references'] != "None":
                                st.markdown(f"**{key}**: {value['text']}<sup>{value['references']}</sup>",
                                            unsafe_allow_html=True)
                                for ref in value['references'].split(','):
                                    used_references.add(ref.strip())
                            else:
                                st.markdown(f"**{key}**: {value['text']}")
                        elif isinstance(value, list):  # Check if the value is a list
                            for item in value:
                                if item['references'] and item['references'] != "None":
                                    st.markdown(f"**{key}**: {item['text']}<sup>{item['references']}</sup>",
                                                unsafe_allow_html=True)
                                    for ref in item['references'].split(','):
                                        used_references.add(ref.strip())
                                else:
                                    st.markdown(f"**{key}**: {item['text']}")
                        else:
                            st.markdown(f"**{key}**: {value}")

            with st.sidebar.expander("**References**"):
                if used_references:
                    for ref in sorted(used_references):
                        full_citation = get_full_citation(ref)
                        if full_citation:
                            st.markdown(f"<sup>{ref}</sup> {full_citation}", unsafe_allow_html=True)

            with st.sidebar.expander("**Patient Database**"):
                st.write("Patient Database information placeholder.")

        else:
            st.sidebar.write("Gene not found.")
elif search_option == "Structure":
    structure_name = st.sidebar.selectbox("Select structure to view genes:",
                                          ["Select a structure"] + list(structures_data.keys()))
    if structure_name and structure_name != "Select a structure":
        genes_list = structures_data[structure_name]
        st.sidebar.header(f"Genes in {structure_name}:")
        for gene in genes_list:
            gene_info = get_gene_info(gene)
            if gene_info:
                st.sidebar.write(f"{gene_info['Gene']} - {gene_info['Locus']}")