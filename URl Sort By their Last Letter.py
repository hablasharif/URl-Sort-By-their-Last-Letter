urls = [
    "https://www.oed.com/dictionary/michelin-tyre_n",
    "https://www.oed.com/dictionary/michelin-tyre-man_n",
    "https://www.oed.com/dictionary/michelsberg_n",
    "https://www.oed.com/dictionary/michelson_n",
    "https://www.oed.com/dictionary/michelson-morley_n",
    "https://www.oed.com/dictionary/michenerite_n",
    "https://www.oed.com/dictionary/michery_n",
    "https://www.oed.com/dictionary/michi_n",
    "https://www.oed.com/dictionary/michigan_n",
    "https://www.oed.com/dictionary/michigander_n",
    "https://www.oed.com/dictionary/michiganian_n",
    "https://www.oed.com/dictionary/michler_n",
    "https://www.oed.com/dictionary/michurinism_n",
    "https://www.oed.com/dictionary/michurinist_adj",
    "https://www.oed.com/dictionary/mick_n1",
    "https://www.oed.com/dictionary/mick_n2",
    "https://www.oed.com/dictionary/mick_n3",
    "https://www.oed.com/dictionary/mick_n4",
    "https://www.oed.com/dictionary/mick_n5",
    "https://www.oed.com/dictionary/mick_n6"
]

# Define the order of the suffixes
suffix_order = ["n1", "n3", "n4", "n5", "n6", "adj", "adv", "pre", "con"]

# Extract the suffix from each URL
def extract_suffix(url):
    return url.split('_')[-1]

# Custom sort function that considers the predefined order
def custom_sort_key(url):
    suffix = extract_suffix(url)
    if suffix in suffix_order:
        return suffix_order.index(suffix)
    else:
        return len(suffix_order)

# Sort URLs based on the custom sort function
sorted_urls = sorted(urls, key=custom_sort_key)

# Filter and print URLs ending with 'n' or the specific suffixes
urls_to_display = [url for url in sorted_urls if extract_suffix(url) in suffix_order or extract_suffix(url) == 'n']
for url in urls_to_display:
    print(url)

