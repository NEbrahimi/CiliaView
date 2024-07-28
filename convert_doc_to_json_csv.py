import os
from docx import Document
import re
import json

def process_data(headers, data):
    processed_data = []
    reference_details = {}

    for row in data:
        entry = {}
        entry['Gene'] = row[0]['text']
        entry['Other Names'] = row[0]['other_names']
        entry['Locus'] = row[1]['text']

        for i, header in enumerate(headers):
            if header not in ["Gene", "Locus"]:
                refs = row[i]['references']
                entry[header] = {
                    'text': row[i]['text'],
                    'references': ', '.join(refs)
                }

                # Collect all unique references with a placeholder for the full citation
                for ref in refs:
                    if ref not in reference_details:
                        reference_details[ref] = ""

        processed_data.append(entry)

    return processed_data, reference_details

def extract_table_from_docx(docx_path):
    doc = Document(docx_path)
    data = []
    table = doc.tables[0]  # Assuming the table is the first one in the document

    # Manually define headers based on expected structure
    headers = ['Gene', 'Locus', 'Protein function', 'TEM', 'IF', 'HSVMA', 'nNO', 'Laterality defects',
               'Male infertility', 'Other clinical associations', 'Prevalence']

    # Ensure unique headers
    headers = make_unique(headers)

    # Extract table rows, skipping the first two rows
    for row in table.rows[2:]:
        row_data = [extract_references(cell.text.strip(), headers[i]) for i, cell in enumerate(row.cells)]
        data.append(row_data)
        # Debug: Print each row data
        print("Row data:", row_data)

    return headers, data

def make_unique(headers):
    seen = set()
    unique_headers = []
    for header in headers:
        if header in seen:
            count = 1
            new_header = f"{header}_{count}"
            while new_header in seen:
                count += 1
                new_header = f"{header}_{count}"
            unique_headers.append(new_header)
            seen.add(new_header)
        else:
            unique_headers.append(header)
            seen.add(header)
    return unique_headers

def extract_references(text, header):
    # Extract references and clean text, handle "Gene" differently to extract other names
    if header == "Gene":
        gene_parts = text.split('(')
        gene_name = gene_parts[0].strip()
        other_names = gene_parts[1].strip(')') if len(gene_parts) > 1 else ""
        return {'text': gene_name, 'other_names': other_names, 'references': []}

    if header == "Locus":
        return {'text': text, 'references': []}

    references = re.findall(r'\d+', text)
    clean_text = re.sub(r'\[\d+\]', '', text).strip()
    return {'text': clean_text, 'references': references}

def save_data_to_json(data, references, file_path):
    full_data = {
        "genes": data,
        "references": references
    }
    with open(file_path, 'w') as f:
        json.dump(full_data, f, indent=4)

if __name__ == '__main__':
    base_dir = os.path.dirname(os.path.abspath(__file__))
    docx_path = os.path.join(base_dir, 'C:/Users/z3541106/unsw/interactive_map/data.docx')
    json_path = os.path.join(base_dir, 'C:/Users/z3541106/unsw/interactive_map/data.json')

    headers, data = extract_table_from_docx(docx_path)
    processed_data, reference_details = process_data(headers, data)

    # Manually fill in the reference details as needed
    # This can be done through another script or manually before using the JSON
    reference_details["1"] = "Loges NT, Olbrich H, Fenske L, et al. DNAI2 mutations cause primary ciliary dyskinesia with defects in the outer dynein arm. Am J Hum Genet. 2008;83(5):547-558."
    reference_details["2"] = "Another reference detail here."
    reference_details["4"] = "Another reference detail here."
    reference_details["5"] = "Another reference detail here."
    reference_details["33"] = "Another reference detail here."
    # ... and so on for all references

    save_data_to_json(processed_data, reference_details, json_path)
