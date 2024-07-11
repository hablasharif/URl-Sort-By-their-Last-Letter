import pandas as pd
from PyPDF2 import PdfReader
from bs4 import BeautifulSoup
import os
from tqdm import tqdm

# Define the order of the suffixes
suffix_order = ["n", "n1", "n2", "n3", "n4", "n5", "n6", "pro", "v", "v1", "v2", "adj", "adj1", "adj2", "adv", "adv1", "pre", "con", "conj"]

# Function to extract suffix from URL
def extract_suffix(url):
    return url.split('_')[-1]

# Custom sort function that considers the predefined order
def custom_sort_key(url):
    suffix = extract_suffix(url)
    if suffix in suffix_order:
        return suffix_order.index(suffix)
    else:
        return len(suffix_order)

# Function to read URLs from a text file
def read_urls_from_txt(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]

# Function to read URLs from an Excel file
def read_urls_from_excel(file_path):
    df = pd.read_excel(file_path)
    return df[df.columns[0]].tolist()

# Function to read URLs from a PDF file
def read_urls_from_pdf(file_path):
    reader = PdfReader(file_path)
    urls = []
    for page in reader.pages:
        text = page.extract_text()
        urls.extend([line.strip() for line in text.splitlines() if line.startswith("http")])
    return urls

# Function to read URLs from an HTML file
def read_urls_from_html(file_path):
    with open(file_path, 'r') as file:
        soup = BeautifulSoup(file, 'html.parser')
    return [a['href'] for a in soup.find_all('a', href=True) if a['href'].startswith("http")]

# Function to read URLs from any file
def read_urls(file_path):
    if file_path.endswith('.txt'):
        return read_urls_from_txt(file_path)
    elif file_path.endswith('.xlsx'):
        return read_urls_from_excel(file_path)
    elif file_path.endswith('.pdf'):
        return read_urls_from_pdf(file_path)
    elif file_path.endswith('.html'):
        return read_urls_from_html(file_path)
    else:
        raise ValueError("Unsupported file type: {}".format(file_path))

# Define the input file path and output file paths
input_file_path = r"C:\Users\style\Desktop\10 july py\oxfor dictionary urls.txt"
output_txt_path = "oed dictionary.txt"
output_excel_path = "oed dictionary.xlsx"
output_html_path = "oed dictionary.html"
non_included_suffix_txt_path = "non_included_suffix.txt"

# Read URLs from the input file
urls = read_urls(input_file_path)

# Count total input URLs
total_input_urls = len(urls)

# Sort URLs based on the custom sort function
sorted_urls = sorted(urls, key=custom_sort_key)

# Filter URLs based on suffix and count occurrences
urls_to_display = []
urls_not_included = []
suffix_counts = {suffix: 0 for suffix in suffix_order}

for url in tqdm(sorted_urls, desc="Processing URLs"):
    suffix = extract_suffix(url)
    if suffix in suffix_order:
        urls_to_display.append(url)
        suffix_counts[suffix] += 1
    else:
        urls_not_included.append(url)

# Count total output URLs
total_output_urls = len(urls_to_display)

# Save the results to different formats
with open(output_txt_path, 'w') as file:
    for url in urls_to_display:
        file.write(f"{url}\n")

df = pd.DataFrame(urls_to_display, columns=["URL"])
df.to_excel(output_excel_path, index=False)

html_content = '<html><body><ul>'
for url in urls_to_display:
    html_content += f'<li><a href="{url}">{url}</a></li>'
html_content += '</ul></body></html>'

with open(output_html_path, 'w') as file:
    file.write(html_content)

# Save URLs with suffixes not included in the predefined order
with open(non_included_suffix_txt_path, 'w') as file:
    for url in urls_not_included:
        file.write(f"{url}\n")

# Display results
print("Total input URLs:", total_input_urls)
print("Total output URLs:", total_output_urls)
print("Counts by suffix:")
for suffix, count in suffix_counts.items():
    print(f"{suffix}: {count}")

print("\nURLs with suffixes not included in the predefined order:")
for url in urls_not_included:
    print(url)
