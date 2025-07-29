# Adobe Hackathon - Task 1A: PDF Structure Extraction

## 📌 Objective

This project extracts the **title** and **hierarchical heading structure** (H1, H2, H3) from PDF documents and outputs it as a structured JSON file, as specified in the Adobe Generative AI Hackathon Round 1A problem statement.

## 🧠 What It Does

* Identifies the **main title** using the largest font on the first page.
* Detects **headings (H1, H2, H3)** based on font size hierarchy.
* Applies filters to ensure heading quality (e.g., avoids bullets/lists/long lines).
* Outputs results in a clean JSON format with heading levels and page numbers.

---

## 📁 Project Structure

```
🔹 Dockerfile            # For containerized execution
🔹 requirements.txt      # Python dependency (PyMuPDF)
🔹 solution.py           # Main logic for PDF parsing and heading extraction
```

---

## 🔧 Dependencies & Setup

### Python Dependencies

Only one library is required:

```
PyMuPDF==1.23.9
```

Install via pip:

```bash
pip install -r requirements.txt
```

> Python 3.10 or above is recommended.

### Folder Structure (as per problem statement)

```
root/
├── input/         # Directory containing PDF files
├── output/        # Directory where JSON outputs will be saved
├── Dockerfile
├── requirements.txt
└── solution.py
```

---

## 🐳 Running with Docker

### 🧪 Step-by-Step

1. **Build the Docker image:**

   ```bash
   docker build -t adobe-task1a .
   ```

2. **Prepare folders:**

   * Place input PDFs in a local `input/` folder.
   * Create an empty `output/` folder.

3. **Run the container:**

   ```bash
   docker run -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output adobe-task1a
   ```

4. **View results:**

   * Output JSONs will be saved inside `output/` directory.

---

## 📂 Output Format

Each processed PDF generates a JSON like:

```json
{
  "title": "Document Title",
  "outline": [
    { "level": "H1", "text": "Introduction", "page": 1 },
    { "level": "H2", "text": "Background", "page": 2 },
    { "level": "H3", "text": "Details", "page": 4 }
  ]
}
```

---

## 🧠 Logic Summary

| Feature        | How It's Determined                                                |
| -------------- | ------------------------------------------------------------------ |
| Title          | Largest font span on the first page                                |
| Heading Fonts  | Next top 3 common sizes smaller than title font                    |
| Valid Headings | Based on length, punctuation, stopword ratio, and formatting rules |

---

## 📦 Example Usage

Place a PDF like `sample.pdf` in `input/`, then run:

```bash
docker run -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output adobe-task1a
```

Result will be in `output/sample.json`.

---

## 🛠️ Tech Stack

* Python 3.10
* [PyMuPDF (`fitz`)](https://pymupdf.readthedocs.io/)
* Docker (for containerization)

---

## 📬 Contact

Built by [DarkMatter1217](https://github.com/DarkMatter1217) for the Adobe Generative AI Hackathon — Task 1A.
