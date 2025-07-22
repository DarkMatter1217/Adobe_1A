import fitz
import os
import re
import json

def clean_text(text):
    return re.sub(r'\s+', ' ', text).strip()

def get_font_styles(doc, threshold=10):
    styles = {}
    for page in doc:
        blocks = page.get_text("dict", flags=fitz.TEXT_PRESERVE_WHITESPACE)["blocks"]
        for block in blocks:
            if block['type'] == 0:
                for line in block['lines']:
                    for span in line['spans']:
                        if span['size'] > threshold:
                            key = int(span['size'])
                            styles[key] = styles.get(key, 0) + 1
    return sorted(styles.items(), key=lambda item: item[1], reverse=True)

def is_valid_heading(text, title_text):
    stripped = text.strip()
    if stripped.lower() == title_text.lower():
        return False
    if not stripped or len(stripped.split()) > 10 or len(stripped.split()) < 2:
        return False
    if re.match(r"^((\d{1,2}[\.\)])|([a-zA-Z][\.\)])|(•)|(\*)|(-))\s", stripped):
        return False
    if stripped.endswith(('.', '!', '?')):
        return False
    stopwords = {'a', 'an', 'the', 'is', 'in', 'on', 'for', 'of', 'to', 'and', 'with', 'that', 'it'}
    word_count = len(stripped.split())
    stopword_count = sum(1 for word in stripped.lower().split() if word in stopwords)
    if stopword_count / word_count > 0.4:
        return False
    if stripped.isupper() and word_count <= 2:
        return False
    return True

def extract_structure(doc):
    title = ""
    max_font_size = 0
    title_line_y0 = 0
    first_page = doc[0]
    blocks = first_page.get_text("dict")["blocks"]
    for block in blocks:
        if block['type'] == 0:
            for line in block['lines']:
                for span in line['spans']:
                    if span['size'] > max_font_size:
                        max_font_size = span['size']
                        title_line_y0 = line['bbox'][1]
    if max_font_size > 0:
        title_words = []
        for block in blocks:
            if block['type'] == 0:
                for line in block['lines']:
                    if abs(line['bbox'][1] - title_line_y0) < 2:
                        for span in line['spans']:
                            title_words.append(span['text'])
        title = clean_text(" ".join(title_words))
    sorted_styles = get_font_styles(doc)
    heading_sizes = []
    for size, freq in sorted_styles:
        if size < max_font_size and size > 11:
            if size not in heading_sizes: heading_sizes.append(size)
        if len(heading_sizes) == 3: break
    headings = []
    seen = set()
    for page_num, page in enumerate(doc):
        page_blocks = page.get_text("dict")["blocks"]
        for block in page_blocks:
            if block['type'] == 0:
                for line in block['lines']:
                    line_spans = [span['text'] for span in line['spans'] if span['text'].strip()]
                    full_line_text = clean_text(" ".join(line_spans))
                    if not full_line_text: continue
                    first_span = line['spans'][0]
                    span_size = int(first_span['size'])
                    if span_size in heading_sizes and is_valid_heading(full_line_text, title):
                        key = (full_line_text.lower(), page_num)
                        if key not in seen:
                            level = heading_sizes.index(span_size) + 1
                            headings.append({
                                "level": f"H{level}",
                                "text": full_line_text,
                                "page": page_num + 1
                            })
                            seen.add(key)
    return {"title": title, "outline": headings}

def main():
    input_dir = "/app/input"
    output_dir = "/app/output"
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(input_dir, filename)
            json_path = os.path.join(output_dir, os.path.splitext(filename)[0] + ".json")
            try:
                doc = fitz.open(pdf_path)
                structure = extract_structure(doc)
                with open(json_path, 'w', encoding='utf-8') as f:
                    json.dump(structure, f, indent=2, ensure_ascii=False)
                print(f"Processed: {filename}")
            except Exception as e:
                print(f"Failed to process {filename}: {e}")

if __name__ == "__main__":
    main()














