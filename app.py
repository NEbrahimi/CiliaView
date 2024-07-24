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


# Function to get full citation
def get_full_citation(reference_key):
    if reference_key in references_data:
        ref_value = references_data[reference_key]
        bibtex = ref_value['bibtex']
        title = bibtex['title']
        author = bibtex['author']
        journal = bibtex['journal']
        volume = bibtex['volume']
        # number = bibtex['number']
        number = bibtex.get('number', '')
        pages = bibtex.get('pages', '')
        year = bibtex['year']
        publisher = bibtex['publisher']
        doi = bibtex.get('doi', '')
        citation = f"{author}. {title}. {journal}. {year};{volume}({number}):{pages}. {publisher}. [DOI]({doi})"
        return citation
    return None


# Function to display gene information with reordered references
def display_gene_info(gene_info):
    used_references = {}
    ref_counter = 1

    def get_sequential_ref(ref):
        nonlocal ref_counter
        if ref not in used_references:
            used_references[ref] = ref_counter
            ref_counter += 1
        return used_references[ref]

    def normalize_references(ref_str):
        return [ref.strip() for ref in ref_str.replace(" ", "").split(",")]

    for key, value in gene_info.items():
        if key not in ["Gene", "Locus", "Other Names"] and value:
            if isinstance(value, list) and len(value) > 0:
                st.markdown(f"**{key}:**")
                for sub_value in value:
                    text = sub_value['text']
                    references = sub_value['references']
                    if references == "None":
                        st.markdown(f"**{key}:** {text}")
                        continue
                    ref_numbers = normalize_references(references)
                    ref_text = ''.join([f"<sup>{get_sequential_ref(ref.strip())}, </sup>" for ref in ref_numbers])
                    ref_text = ref_text.rstrip(", </sup>") + '</sup>'
                    st.markdown(f"- {text} {ref_text}", unsafe_allow_html=True)
            else:
                text = value['text']
                references = value['references']
                if references == "None":
                    st.markdown(f"**{key}:** {text}")
                    continue
                if references:
                    ref_numbers = normalize_references(references)
                    ref_text = ''.join([f"<sup>{get_sequential_ref(ref.strip())}, </sup>" for ref in ref_numbers])
                    ref_text = ref_text.rstrip(", </sup>") + '</sup>'
                    st.markdown(f"**{key}:** {text} {ref_text}", unsafe_allow_html=True)
                else:
                    st.markdown(f"**{key}:** {text}")
    return used_references




# Custom CSS to adjust the layout
st.markdown(
    """
    <style>
        .css-1e5imcs {
            width: 400px !important;
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
        ul {
            margin: 0;
            padding-left: 20px; /* Adjust as needed for indentation */
            margin-bottom: 13px; /* Space after the list */
        }
        li {
            margin: 0 0 0px 0; /* Adjust bottom margin for spacing between list items */
            padding-left: 10px; /* Adjust padding to create space between bullet and text */
            line-height: 1.5; /* Adjust line height to reduce spacing between lines */
        }
        p {
            margin: 0 0 13px 0; /* Adjust this value to control the space after paragraphs */
        }
        
        h2, h3, h4, h5, h6 {
            margin: 0 0 13px 0; /* Adjust this value to control the space after headings */
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Central area for the map
st.title("Cilia Structure Map")
map_image = Image.open("map.png")
st.image(map_image, width=900, caption='')

# Sidebar interaction for search
st.sidebar.title("Search and Filter")
search_option = st.sidebar.selectbox("Search by", ["Gene", "Structure"])

if search_option == "Gene":
    gene_name = st.sidebar.text_input("Enter gene name")
    if gene_name:
        gene_info = get_gene_info(gene_name)
        if gene_info:
            with st.sidebar.expander("**Gene Information**"):
                st.markdown(f"**{gene_info['Gene']}**")
                used_references = display_gene_info(gene_info)

            with st.sidebar.expander("**References**"):
                if used_references:
                    sorted_references = sorted(used_references.items(), key=lambda x: x[1])
                    for original_ref, new_ref in sorted_references:
                        full_citation = get_full_citation(f"reference_{original_ref}")
                        if full_citation:
                            st.markdown(f"<sup>{new_ref}</sup> {full_citation}", unsafe_allow_html=True)

            with st.sidebar.expander("**Patient Database**"):
                st.write("Patient Database information placeholder.")

        else:
            st.sidebar.write("Gene not found.")

elif search_option == "Structure":
    structure_name = st.sidebar.selectbox("Select structure to view genes:", ["Select a structure"] + list(structures_data.keys()), key="structure_select")
    if structure_name and structure_name != "Select a structure":
        genes_list = structures_data[structure_name]
        with st.sidebar.expander(f"**Genes associated with {structure_name}:**", expanded=True):
            for gene in genes_list:
                st.write(gene)
        gene_name = st.sidebar.text_input("Enter gene name to view details", key="gene_name_input")
        if gene_name:
            gene_info = get_gene_info(gene_name)
            if gene_info:
                with st.sidebar.expander("**Gene Information**"):
                    st.markdown(f"**{gene_info['Gene']}**")
                    used_references = display_gene_info(gene_info)

                with st.sidebar.expander("**References**"):
                    if used_references:
                        sorted_references = sorted(used_references.items(), key=lambda x: x[1])
                        for original_ref, new_ref in sorted_references:
                            full_citation = get_full_citation(f"reference_{original_ref}")
                            if full_citation:
                                st.markdown(f"<sup>{new_ref}</sup> {full_citation}", unsafe_allow_html=True)

                with st.sidebar.expander("**Patient Database**"):
                    st.write("Patient Database information placeholder.")

            else:
                st.sidebar.write("Gene not found.")