import uuid
import streamlit as st
import pytesseract
pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"
from PIL import Image
import re
import pandas as pd
from io import BytesIO
from pdf2image import convert_from_bytes

# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config(page_title="InvoiceIQ · OCR Dashboard", layout="wide", page_icon="🧾")

# -----------------------------
# PROFESSIONAL UI — Navy / Slate / Sapphire
# -----------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@300;400;500&display=swap');

:root {
    --bg:           #f0f2f7;
    --bg-deep:      #e4e8f0;
    --surface:      #ffffff;
    --surface-2:    #f7f8fc;
    --border:       #dde1ec;
    --border-soft:  #eceef5;
    --navy:         #0f1e3c;
    --navy-mid:     #1a3260;
    --sapphire:     #2563eb;
    --sapphire-lt:  #3b82f6;
    --sapphire-pale:#eff6ff;
    --teal:         #0d9488;
    --teal-pale:    #f0fdfa;
    --text:         #0f172a;
    --text-2:       #334155;
    --text-3:       #64748b;
    --success:      #059669;
    --success-pale: #ecfdf5;
    --warn:         #d97706;
    --warn-pale:    #fffbeb;
    --radius-sm:    8px;
    --radius:       12px;
    --radius-lg:    18px;
    --shadow-sm:    0 1px 3px rgba(15,30,60,0.08), 0 1px 2px rgba(15,30,60,0.04);
    --shadow:       0 4px 16px rgba(15,30,60,0.10), 0 1px 4px rgba(15,30,60,0.06);
}

*, *::before, *::after { box-sizing: border-box; }

html, body, .stApp {
    background-color: var(--bg) !important;
    font-family: 'Plus Jakarta Sans', sans-serif;
    color: var(--text);
}

#MainMenu, footer, header { visibility: hidden; }

.block-container {
    padding: 0 2.5rem 4rem !important;
    max-width: 1200px !important;
}

/* ── Top nav bar ── */
.topbar {
    background: var(--navy);
    margin: 0 -2.5rem 0;
    padding: 0 2.5rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    height: 60px;
    position: sticky;
    top: 0;
    z-index: 100;
    box-shadow: 0 2px 12px rgba(15,30,60,0.25);
}
.topbar-brand {
    display: flex;
    align-items: center;
    gap: 10px;
}
.topbar-logo {
    width: 32px;
    height: 32px;
    background: linear-gradient(135deg, var(--sapphire), #60a5fa);
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 16px;
}
.topbar-name {
    font-weight: 800;
    font-size: 16px;
    color: #fff;
    letter-spacing: -0.3px;
}
.topbar-name span { color: #60a5fa; }
.topbar-pill {
    background: rgba(96,165,250,0.15);
    border: 1px solid rgba(96,165,250,0.3);
    color: #93c5fd;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    padding: 4px 12px;
    border-radius: 100px;
    display: flex;
    align-items: center;
    gap: 6px;
}
.topbar-dot {
    display: inline-block;
    width: 7px; height: 7px;
    background: #34d399;
    border-radius: 50%;
    box-shadow: 0 0 6px #34d399;
    animation: pulse 2s infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50%       { opacity: 0.35; }
}

/* ── Page hero ── */
.page-hero {
    padding: 36px 0 28px;
    border-bottom: 1px solid var(--border);
    margin-bottom: 32px;
}
.breadcrumb {
    font-size: 12px;
    color: var(--text-3);
    margin-bottom: 14px;
    font-weight: 500;
    display: flex;
    align-items: center;
    gap: 6px;
}
.breadcrumb .active { color: var(--sapphire); }
.page-hero h1 {
    font-size: 28px;
    font-weight: 800;
    color: var(--navy);
    letter-spacing: -0.5px;
    margin: 0 0 6px;
}
.page-hero p {
    font-size: 13.5px;
    color: var(--text-3);
    margin: 0;
}

/* ── Section label ── */
.sec-title {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--text-3);
    margin: 32px 0 12px;
    display: flex;
    align-items: center;
    gap: 10px;
}
.sec-title::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border);
}

/* ── Upload panel ── */
.upload-panel {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 24px 24px 18px;
    box-shadow: var(--shadow-sm);
}
.upload-panel-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 16px;
}
.upload-panel-icon {
    width: 38px; height: 38px;
    background: var(--sapphire-pale);
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 18px;
}
.upload-panel-title { font-size: 15px; font-weight: 700; color: var(--navy); }
.upload-panel-sub   { font-size: 12px; color: var(--text-3); margin-top: 2px; }

[data-testid="stFileUploader"] {
    background: var(--surface-2) !important;
    border: 1.5px dashed var(--border) !important;
    border-radius: var(--radius) !important;
    padding: 20px !important;
    transition: border-color 0.2s, background 0.2s;
}
[data-testid="stFileUploader"]:hover {
    border-color: var(--sapphire) !important;
    background: var(--sapphire-pale) !important;
}
[data-testid="stFileUploader"] label {
    color: var(--text-3) !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 13px !important;
}

/* ── Info strip ── */
.info-strip {
    background: var(--sapphire-pale);
    border: 1px solid #bfdbfe;
    border-radius: var(--radius);
    padding: 10px 16px;
    font-size: 12.5px;
    color: #1e40af;
    font-weight: 500;
    margin-top: 12px;
    display: flex;
    align-items: center;
    gap: 8px;
}

/* ── Extract button ── */
.stButton > button {
    background: linear-gradient(135deg, var(--sapphire), #1d4ed8) !important;
    color: #fff !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 700 !important;
    font-size: 14px !important;
    border: none !important;
    border-radius: var(--radius) !important;
    padding: 12px 32px !important;
    box-shadow: 0 4px 14px rgba(37,99,235,0.35) !important;
    transition: all 0.2s ease !important;
    margin-top: 10px !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(37,99,235,0.45) !important;
}

/* ── Invoice card ── */
.inv-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    margin-bottom: 12px;
    overflow: hidden;
    box-shadow: var(--shadow-sm);
    transition: box-shadow 0.2s, border-color 0.2s;
}
.inv-card:hover {
    box-shadow: var(--shadow);
    border-color: #c7d4f0;
}
.inv-card-top {
    background: var(--navy);
    padding: 13px 20px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.inv-card-filename {
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
    font-weight: 500;
    color: #cbd5e1;
    display: flex;
    align-items: center;
    gap: 8px;
}
.inv-card-filename::before {
    content: '';
    display: inline-block;
    width: 7px; height: 7px;
    background: #34d399;
    border-radius: 50%;
}
.inv-status {
    background: rgba(52,211,153,0.12);
    border: 1px solid rgba(52,211,153,0.28);
    color: #34d399;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    padding: 3px 10px;
    border-radius: 100px;
}
.inv-card-body {
    padding: 20px 20px 4px;
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 24px;
}
.inv-field-label {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: var(--text-3);
    margin-bottom: 6px;
    display: flex;
    align-items: center;
    gap: 5px;
}
.lbl-dot {
    display: inline-block;
    width: 5px; height: 5px;
    background: var(--sapphire);
    border-radius: 50%;
    opacity: 0.5;
}
.inv-field-value {
    font-size: 15px;
    font-weight: 600;
    color: var(--navy);
}
.inv-field-value.money {
    color: var(--success);
    font-size: 17px;
    font-weight: 700;
    font-family: 'JetBrains Mono', monospace;
}
.inv-field-value.empty {
    color: var(--text-3);
    font-style: italic;
    font-weight: 400;
    font-size: 13px;
}

/* ── Items section inside card ── */
.inv-items-section {
    padding: 0 20px 20px;
    margin-top: 4px;
}
.inv-items-title {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: var(--text-3);
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    gap: 8px;
    padding-top: 14px;
    border-top: 1px solid var(--border-soft);
}
.items-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 13px;
}
.items-table thead tr {
    background: var(--surface-2);
    border-radius: var(--radius-sm);
}
.items-table thead th {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1.2px;
    text-transform: uppercase;
    color: var(--text-3);
    padding: 8px 12px;
    text-align: left;
    border-bottom: 1px solid var(--border);
}
.items-table tbody tr {
    border-bottom: 1px solid var(--border-soft);
    transition: background 0.15s;
}
.items-table tbody tr:last-child { border-bottom: none; }
.items-table tbody tr:hover { background: var(--sapphire-pale); }
.items-table tbody td {
    padding: 9px 12px;
    color: var(--text-2);
    font-weight: 500;
}
.items-table tbody td.td-price {
    font-family: 'JetBrains Mono', monospace;
    font-weight: 600;
    color: var(--success);
}
.items-table tbody td.td-qty {
    font-family: 'JetBrains Mono', monospace;
    color: var(--sapphire);
    font-weight: 600;
}
.item-plain {
    display: flex;
    align-items: flex-start;
    gap: 8px;
    padding: 7px 0;
    border-bottom: 1px solid var(--border-soft);
    font-size: 13px;
    color: var(--text-2);
    font-weight: 500;
}
.item-plain:last-child { border-bottom: none; }
.item-bullet {
    width: 6px; height: 6px;
    background: var(--sapphire);
    border-radius: 50%;
    margin-top: 5px;
    flex-shrink: 0;
    opacity: 0.5;
}
.items-empty {
    background: var(--warn-pale);
    border: 1px solid #fde68a;
    border-radius: var(--radius-sm);
    padding: 10px 14px;
    font-size: 12.5px;
    color: var(--warn);
    font-weight: 600;
}

/* ── Metric cards ── */
.metrics-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 14px;
}
.metric-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 22px 22px 20px;
    box-shadow: var(--shadow-sm);
    position: relative;
    overflow: hidden;
}
.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
}
.metric-card.c-navy::before   { background: linear-gradient(90deg, #0f1e3c, #1a3260); }
.metric-card.c-blue::before   { background: linear-gradient(90deg, #2563eb, #3b82f6); }
.metric-card.c-teal::before   { background: linear-gradient(90deg, #0d9488, #34d399); }
.metric-card.c-green::before  { background: linear-gradient(90deg, #059669, #6ee7b7); }

.metric-eyebrow {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--text-3);
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    gap: 8px;
}
.m-icon {
    width: 26px; height: 26px;
    border-radius: 7px;
    display: flex; align-items: center; justify-content: center;
    font-size: 13px;
}
.m-icon.navy  { background: #e8edf7; }
.m-icon.blue  { background: #eff6ff; }
.m-icon.teal  { background: #f0fdfa; }
.m-icon.green { background: #ecfdf5; }

.metric-number {
    font-size: 38px;
    font-weight: 800;
    letter-spacing: -2px;
    line-height: 1;
    margin-bottom: 5px;
}
.metric-number.c-navy  { color: #0f1e3c; }
.metric-number.c-blue  { color: #2563eb; }
.metric-number.c-teal  { color: #0d9488; }
.metric-number.c-green { color: #059669; }

.metric-footer {
    font-size: 12px;
    color: var(--text-3);
    font-weight: 500;
}
.metric-footer b { color: var(--text-2); font-weight: 600; }

/* ── Export ── */
.export-row {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 20px 24px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    box-shadow: var(--shadow-sm);
    margin-top: 8px;
}
.export-title { font-size: 14px; font-weight: 700; color: var(--navy); margin-bottom: 3px; }
.export-sub   { font-size: 12px; color: var(--text-3); }

.stDownloadButton > button {
    background: var(--success) !important;
    color: #fff !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 700 !important;
    font-size: 13px !important;
    border: none !important;
    border-radius: var(--radius) !important;
    padding: 11px 26px !important;
    box-shadow: 0 4px 12px rgba(5,150,105,0.3) !important;
    transition: all 0.2s ease !important;
    margin-top: 0 !important;
}
.stDownloadButton > button:hover {
    background: #047857 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 18px rgba(5,150,105,0.4) !important;
}

/* ── Empty state ── */
.empty-state {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 56px 28px;
    text-align: center;
    box-shadow: var(--shadow-sm);
    margin-top: 20px;
}
.empty-state .icon { font-size: 46px; margin-bottom: 14px; }
.empty-state h3 { font-size: 17px; font-weight: 700; color: var(--navy); margin-bottom: 8px; }
.empty-state p  { font-size: 13px; color: var(--text-3); max-width: 300px; margin: 0 auto; }

/* ── Misc overrides ── */
[data-testid="stVerticalBlock"] { gap: 0 !important; }
.stMarkdown p { color: var(--text-2) !important; }
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 4px; }
</style>
""", unsafe_allow_html=True)

# ── Nav bar ────────────────────────────────────────────────
st.markdown("""
<div class="topbar">
    <div class="topbar-brand">
        <div class="topbar-logo">🧾</div>
        <div class="topbar-name">Invoice<span>IQ</span></div>
    </div>
    <div class="topbar-pill">
        <span class="topbar-dot"></span>System Online
    </div>
</div>
""", unsafe_allow_html=True)

# ── Hero ───────────────────────────────────────────────────
st.markdown("""
<div class="page-hero">
    <div class="breadcrumb">
        <span>Dashboard</span>
        <span>›</span>
        <span class="active">OCR Extraction</span>
    </div>
    <h1>Invoice Data Extraction</h1>
    <p>Upload invoice documents to automatically extract vendor, date, total amount, and line items using PaddleOCR.</p>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# OCR
# -----------------------------
@st.cache_resource
def load_ocr():
    return pytesseract

ocr = load_ocr()

# ── Upload ─────────────────────────────────────────────────
st.markdown("""
<div class="upload-panel">
    <div class="upload-panel-header">
        <div class="upload-panel-icon">📂</div>
        <div>
            <div class="upload-panel-title">Upload Documents</div>
            <div class="upload-panel-sub">PNG · JPG · JPEG · PDF — up to 50 files per batch</div>
        </div>
    </div>
""", unsafe_allow_html=True)

uploaded_files = st.file_uploader(
    "Drag & drop files here, or click to browse",
    type=["png", "jpg", "jpeg", "pdf"],
    accept_multiple_files=True,
    key="invoice_uploader"
)

st.markdown('</div>', unsafe_allow_html=True)

if uploaded_files:
    st.markdown(f"""
    <div class="info-strip">
        ℹ️ &nbsp;<strong>{len(uploaded_files)} file(s)</strong> ready — click "Run Extraction" to begin.
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# HELPERS
# -----------------------------
def clean_text(t):
    return re.sub(r'\s+', ' ', t).strip()

def parse_amount(amount_str):
    if not amount_str:
        return 0
    num = re.sub(r'[^\d.]', '', amount_str)
    return float(num) if num else 0

def extract_fields(lines):
    vendor, date, total = "", "", ""
    for i, l in enumerate(lines):
        l_low = l.lower()
        if not vendor and len(l) > 5 and not any(x in l_low for x in ["invoice", "date", "total"]):
            vendor = l
        if re.search(r'\d{4}-\d{2}-\d{2}', l):
            date = re.search(r'\d{4}-\d{2}-\d{2}', l).group()
        elif re.search(r'\d{2}/\d{2}/\d{4}', l):
            date = re.search(r'\d{2}/\d{2}/\d{4}', l).group()
        if "total" in l_low:
            m = re.search(r'[\$₹]\s?\d+(\.\d+)?', l)
            if m:
                total = m.group().replace(" ", "")
            elif i + 1 < len(lines):
                m = re.search(r'[\$₹]\s?\d+(\.\d+)?', lines[i + 1])
                if m:
                    total = m.group().replace(" ", "")
    return vendor, date, total

def extract_items(lines):
    """
    Extract line items from plain text lines (pytesseract output).
    Returns (table_items, normal_items):
      - table_items: list of dicts with Item / Qty / Price
      - normal_items: list of plain strings
    """
    table_items = []
    normal_items = []

    for l in lines:
        # Look for currency and numbers
        if re.search(r'[\$₹]', l):
            price_match = re.search(r'(\d+(?:\.\d+)?)', l)
            qty_match = re.search(r'\b\d+\b', l)
            if price_match and qty_match:
                table_items.append({
                    "Item": l,
                    "Qty": qty_match.group(),
                    "Price": re.search(r'[\$₹]\s?\d+(?:\.\d+)?', l).group()
                })
            else:
                normal_items.append(l)
        else:
            normal_items.append(l)

    return table_items, normal_items


def build_items_html(table_items, normal_items):
    """Render items section HTML."""
    if table_items:
        rows_html = ""
        for it in table_items:
            rows_html += f"""
            <tr>
                <td>{it['Item']}</td>
                <td class="td-qty">{it['Qty']}</td>
                <td class="td-price">{it['Price']}</td>
            </tr>"""
        return f"""
        <table class="items-table">
            <thead>
                <tr>
                    <th>Item / Description</th>
                    <th>Qty</th>
                    <th>Price</th>
                </tr>
            </thead>
            <tbody>{rows_html}</tbody>
        </table>"""
    elif normal_items:
        items_html = ""
        for it in normal_items:
            items_html += f'<div class="item-plain"><span class="item-bullet"></span><span>{it}</span></div>'
        return items_html
    else:
        return '<div class="items-empty">⚠ No line items detected in this invoice</div>'

def convert_pdf(file):
    return convert_from_bytes(file.read())

def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    return output.getvalue()

# -----------------------------
# MAIN
# -----------------------------
if uploaded_files:
    if st.button("⚡  Run Extraction"):

        excel_rows = []
        total_files = len(uploaded_files)

        st.markdown('<div class="sec-title">Extraction Results</div>', unsafe_allow_html=True)

        for file in uploaded_files:
            if file.type == "application/pdf":
                images = convert_pdf(file)
            else:
                images = [Image.open(file)]

            for img in images:
                temp_path = f"temp_{uuid.uuid4().hex}.png"
                img.save(temp_path)
                text = ocr.image_to_string(Image.open(temp_path))
                lines = [clean_text(l) for l in text.splitlines() if l.strip()]

                vendor, date, total = extract_fields(lines)

                   # Adapt extract_items to work with text lines
                table_items, normal_items = extract_items(lines)

                

                num_items  = len(table_items) if table_items else len(normal_items)
                total_qty  = (sum(int(it["Qty"]) for it in table_items if it["Qty"].isdigit())
                              if table_items else num_items)

                # Flatten items for Excel
                items_str = ("; ".join(f"{it['Item']} (Qty:{it['Qty']}, {it['Price']})"
                                       for it in table_items)
                             if table_items
                             else "; ".join(normal_items))

                excel_rows.append({
                    "File":          file.name,
                    "Vendor":        vendor,
                    "Date":          date,
                    "No. of Items":  num_items,
                    "Total Quantity": total_qty,
                    "Total Price":   total,
                    "Line Items":    items_str,
                })

                v_html = (f'<div class="inv-field-value">{vendor}</div>'
                          if vendor else '<div class="inv-field-value empty">Not detected</div>')
                d_html = (f'<div class="inv-field-value">{date}</div>'
                          if date   else '<div class="inv-field-value empty">Not detected</div>')
                t_html = (f'<div class="inv-field-value money">{total}</div>'
                          if total  else '<div class="inv-field-value empty">Not detected</div>')

                items_html = build_items_html(table_items, normal_items)

                st.markdown(f"""
                <div class="inv-card">
                    <div class="inv-card-top">
                        <div class="inv-card-filename">{file.name}</div>
                        <div class="inv-status">✓ Parsed</div>
                    </div>
                    <div class="inv-card-body">
                        <div>
                            <div class="inv-field-label"><span class="lbl-dot"></span>Vendor / Issuer</div>
                            {v_html}
                        </div>
                        <div>
                            <div class="inv-field-label"><span class="lbl-dot"></span>Invoice Date</div>
                            {d_html}
                        </div>
                        <div>
                            <div class="inv-field-label"><span class="lbl-dot"></span>Total Amount</div>
                            {t_html}
                        </div>
                    </div>
                    <div class="inv-items-section">
                        <div class="inv-items-title">
                            <span class="lbl-dot" style="opacity:1"></span>
                            Line Items &nbsp;·&nbsp; {num_items} detected
                        </div>
                        {items_html}
                    </div>
                </div>
                """, unsafe_allow_html=True)

        # ── Summary ──────────────────────────────────────
        total_amount    = sum(parse_amount(row["Total Price"]) for row in excel_rows)
        detected_totals = sum(1 for row in excel_rows if row["Total Price"])
        total_items_sum = sum(row["No. of Items"] for row in excel_rows)

        st.markdown('<div class="sec-title">Summary</div>', unsafe_allow_html=True)

        st.markdown(f"""
        <div class="metrics-row">
            <div class="metric-card c-navy">
                <div class="metric-eyebrow">
                    <div class="m-icon navy">📁</div>Files Processed
                </div>
                <div class="metric-number c-navy">{total_files}</div>
                <div class="metric-footer"><b>{total_files}</b> documents uploaded</div>
            </div>
            <div class="metric-card c-blue">
                <div class="metric-eyebrow">
                    <div class="m-icon blue">🧾</div>Invoices Extracted
                </div>
                <div class="metric-number c-blue">{len(excel_rows)}</div>
                <div class="metric-footer"><b>{detected_totals}</b> with amount detected</div>
            </div>
            <div class="metric-card c-teal">
                <div class="metric-eyebrow">
                    <div class="m-icon teal">📦</div>Total Line Items
                </div>
                <div class="metric-number c-teal">{total_items_sum}</div>
                <div class="metric-footer">Across all invoices</div>
            </div>
            <div class="metric-card c-green">
                <div class="metric-eyebrow">
                    <div class="m-icon green">💳</div>Total Value
                </div>
                <div class="metric-number c-green">₹{total_amount:,.0f}</div>
                <div class="metric-footer">Cumulative across all invoices</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Export ────────────────────────────────────────
        st.markdown('<div class="sec-title">Export Report</div>', unsafe_allow_html=True)

        df = pd.DataFrame(excel_rows)

        col_left, col_right = st.columns([3, 1])
        with col_left:
            st.markdown("""
            <div class="export-row">
                <div>
                    <div class="export-title">📊 Excel Summary Report</div>
                    <div class="export-sub">All extracted fields — including line items — compiled into a structured .xlsx spreadsheet</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        with col_right:
            st.markdown("<div style='padding-top:8px'>", unsafe_allow_html=True)
            st.download_button(
                label="⬇  Download .xlsx",
                data=to_excel(df),
                file_name="invoice_summary.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            st.markdown("</div>", unsafe_allow_html=True)

else:
    st.markdown("""
    <div class="empty-state">
        <div class="icon">🧾</div>
        <h3>No Invoices Uploaded Yet</h3>
        <p>Upload one or more invoice files above, then click "Run Extraction" to begin.</p>
    </div>
    """, unsafe_allow_html=True)
