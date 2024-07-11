import os
import pandas as pd
import pyarrow.parquet as pq
from concurrent.futures import ProcessPoolExecutor, as_completed
from tqdm import tqdm

# Define the order of the suffixes
suffix_order =["n",
"n1",
"n2",
"n3",
"n4",
"n5",
"n6",
"n7",
"n8",
"n9",
"n10",
"n11",
"n12",
"pron",
"pron1",
"pron2",
"pron3",
"pron4",
"pron5",
"adj",
"adj1",
"adj2",
"adj3",
"adj4",
"adj5",
"adj6",
"v",
"v1",
"v3",
"v3",
"v4",
"v5",
"v6",
"v7",
"v8",
"v9",
"v10",
"v11",
"v12",
"v13",
"adv",
"adv1",
"adv2",
"adv3",
"adv4",
"adv5",
"prep",
"prep1",
"prep2",
"prep3",
"conj",
"conj1",
"conj2",
"conj3",
"int",
"int1",
"int2",
"int3",
"prefix",
"prefix1",
"prefix2",
"prefix3",
"prefix4",
"prefix5",
"prefix6",
"suffix",
"suffix1",
"suffix2",
"suffix3",
"suffix4",
"suffix5",
"suffix6",
"combform",
"combform1",
"combform2",
"combform3",
"combform4",]
                

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

# Function to fetch URLs (example CPU-bound task)
def fetch_url(url):
    # Placeholder CPU-bound task
    return url

# Main function to orchestrate processing
def main():
    # Define the input file path and output file paths
    input_file_path = r"C:\Users\style\Desktop\10 july py\oxfor dictionary urls.txt"
    output_txt_path = "sorted my fuck.txt"
    non_included_suffix_txt_path = "non_included_suffixsf.txt"

    # Direct input of URLs (with options for double quotes and commas, or by space)
    direct_input = ""  # Add your URLs here, either as a list of strings or a single string separated by spaces
    direct_input_urls = []

    if direct_input:
        if '"' in direct_input or ',' in direct_input:
            direct_input_urls = [url.strip() for url in direct_input.split(',')]
        else:
            direct_input_urls = direct_input.split()

    # Read URLs from the input file
    urls = []
    if os.path.exists(input_file_path):
        urls.extend(read_urls_from_txt(input_file_path))
    urls.extend(direct_input_urls)

    # Count total input URLs
    total_input_urls = len(urls)

    # Sort URLs based on the custom sort function
    sorted_urls = sorted(urls, key=custom_sort_key)

    # Process URLs using multiprocessing for CPU-bound tasks
    processed_urls = []
    urls_not_included = []
    suffix_counts = {suffix: 0 for suffix in suffix_order}

    # Calculate total items for tqdm
    total_items = len(sorted_urls)

    # Using ProcessPoolExecutor for concurrent processing
    with ProcessPoolExecutor() as executor:
        futures = [executor.submit(fetch_url, url) for url in sorted_urls]

        for future in tqdm(as_completed(futures), total=total_items, desc="Processing URLs"):
            url = future.result()
            processed_urls.append(url)
            suffix = extract_suffix(url)
            if suffix in suffix_order:
                suffix_counts[suffix] += 1
            else:
                urls_not_included.append(url)

    # Calculate total output URLs
    total_output_urls = len(processed_urls)

    # Save the results to different formats
    with open(output_txt_path, 'w') as file:
        for url in processed_urls:
            file.write(f"{url}\n")

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

if __name__ == "__main__":
    main()
