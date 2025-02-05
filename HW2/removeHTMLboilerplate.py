import os
from boilerpy3.extractors import ArticleExtractor

input_dir = "raw_html_files"
output_dir = "processed_html_files"
os.makedirs(output_dir, exist_ok=True)

def process_html(file_path, output_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            html_content = f.read()

        if not html_content.strip():
            print(f"Skipping empty file: {file_path}")
            return False  

        extractor = ArticleExtractor()
        extracted_content = extractor.get_content(html_content)

        if not extracted_content.strip():
            print(f"Skipping file with no extracted content: {file_path}")
            return False  

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(extracted_content)

        print(f"Processed and saved: {output_path}")
        return True  

    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False 

uri_to_hash_map = []
with open("uri_to_hash_map.txt", "r", encoding="utf-8") as f:
    for line in f:
        uri, hash_name = line.strip().split()
        uri_to_hash_map.append((hash_name, uri))

saved_files_count = 0

for hash_name, _ in uri_to_hash_map:
    input_path = os.path.join(input_dir, f"{hash_name}.html")
    output_path = os.path.join(output_dir, f"{hash_name}_processed.txt")

    if os.path.exists(input_path):
        if process_html(input_path, output_path):
            saved_files_count += 1

print(f"Total number of files successfully saved: {saved_files_count}")
