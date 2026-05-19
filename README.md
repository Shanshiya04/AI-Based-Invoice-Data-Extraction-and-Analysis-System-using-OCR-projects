# AI-Based-Invoice-Data-Extraction-and-Analysis-System-using-OCR
AI-based system for extracting and analyzing invoice data from images and PDFs using OCR with an explainable approach.
# 📄 AI-Based Invoice Data Extraction using OCR

## 🚀 Overview

This project presents an **AI-based system for extracting structured data from invoices** using Optical Character Recognition (OCR). The system processes multiple invoice files (images and PDFs), extracts key information such as vendor name, date, total amount, and line items, and presents the results in an interactive dashboard.

The solution combines **deep learning-based OCR (PaddleOCR)** with **rule-based data extraction**, making it both efficient and explainable.

---

## 🧠 Key Idea

The system follows an **Explainable AI approach**, where:

* OCR (deep learning) extracts raw text
* Rule-based logic processes and structures the data
* Results are displayed and exported for analysis

This ensures:
✔ Transparency
✔ Reliability
✔ Easy debugging

---

## ✨ Features

* 📤 Upload multiple invoices (Images & PDFs)
* 🧾 Extract key fields:

  * Vendor Name
  * Invoice Date
  * Total Amount
  * Line Items
* 📊 Dashboard with summary metrics
* 📥 Export results to Excel
* ⚡ Fast and interactive Streamlit UI
* 🔍 Handles both structured and unstructured invoices

---

## 🛠️ Technologies Used

* **Python**
* **Streamlit** – UI Dashboard
* **PaddleOCR** – AI-based text extraction
* **OpenCV** – Image processing
* **Pandas** – Data handling
* **pdf2image** – PDF to image conversion
* **Regex (re)** – Data extraction logic

---

## 🧠 System Architecture

1. **Input Layer**

   * Upload invoices (Image/PDF)

2. **OCR Layer**

   * PaddleOCR extracts text using deep learning

3. **Processing Layer**

   * Text cleaned and grouped
   * Regex used to extract fields

4. **Output Layer**

   * Structured data displayed in UI
   * Export to Excel

---

## 📁 Project Structure

```text
invoice-ocr-project/
│
├── app1.py             # Main Streamlit application
├── requirements.txt    # Dependencies
├── README.md           # Project documentation
└── sample_invoices/    # Optional test files
```

---

## ⚙️ Installation

### 1. Clone repository

```bash
git clone https://github.com/your-username/invoice-ocr-project.git
cd invoice-ocr-project
```

### 2. Create virtual environment

```bash
python -m venv venv310
venv310\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Run the Application

```bash
streamlit run app2.py
```

---

## 📊 Output

The system provides:

* Extracted invoice details
* Summary dashboard (files, invoices, items)
* Downloadable Excel report

---

## 🎯 Use Cases

* Automated invoice processing
* Expense tracking systems
* Financial data analysis
* Business intelligence dashboards

---

## 🔮 Future Enhancements

* Integration with transformer-based models (Donut, LayoutLM)
* Improved item detection using ML
* Database integration
* Cloud deployment

---

## 🎓 Conclusion

This project demonstrates how **AI (OCR) combined with explainable logic** can effectively convert unstructured invoice data into structured insights. The system is scalable, user-friendly, and suitable for real-world applications.

---

## 👨‍💻 Author

* Shanshiya E

---

## 📜 License

This project is licensed under the MIT License.
