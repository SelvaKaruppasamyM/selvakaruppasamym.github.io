import os
import re
import sys
from pypdf import PdfReader

def get_latest_resume():
    resumes_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'resumes')
    if not os.path.exists(resumes_dir):
        print(f"Error: Resumes directory not found at {resumes_dir}")
        sys.exit(1)
        
    pdf_files = [f for f in os.listdir(resumes_dir) if f.lower().endswith('.pdf')]
    if not pdf_files:
        print("No PDF files found in the resumes folder.")
        sys.exit(1)
        
    # Get the file with the latest modification time
    latest_file = max(
        pdf_files,
        key=lambda f: os.path.getmtime(os.path.join(resumes_dir, f))
    )
    return os.path.join(resumes_dir, latest_file), latest_file

def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text

def update_download_link(latest_filename):
    portfolio_dir = os.path.dirname(os.path.dirname(__file__))
    html_path = os.path.join(portfolio_dir, 'index.html')
    
    if not os.path.exists(html_path):
        print(f"Error: index.html not found at {html_path}")
        sys.exit(1)
        
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
        
    # Match the download-btn anchor tag and replace the href
    # e.g., <a href="Selva_Karuppasamy_M_Resume.pdf" class="download-btn" download>
    pattern = r'(<a\s+[^>]*href=")([^"]*)("\s+class="download-btn"[^>]*download[^>]*>)'
    
    new_href = f"resumes/{latest_filename}"
    
    def replace_href(match):
        old_href = match.group(2)
        if old_href != new_href:
            print(f"Updating resume download link from '{old_href}' to '{new_href}'")
        return f"{match.group(1)}{new_href}{match.group(3)}"
        
    new_content, count = re.subn(pattern, replace_href, html_content, flags=re.IGNORECASE)
    
    if count > 0:
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("Successfully updated index.html download link.")
    else:
        print("Warning: Could not find matching download button link to update in index.html.")

def main():
    pdf_path, filename = get_latest_resume()
    print(f"Latest resume found: {filename}")
    
    # Update download link
    update_download_link(filename)
    
    # Extract text to assist with content verification
    text = extract_text_from_pdf(pdf_path)
    print("\n--- EXTRACTED RESUME TEXT ---")
    print(text.strip())
    print("-----------------------------\n")

if __name__ == '__main__':
    main()
