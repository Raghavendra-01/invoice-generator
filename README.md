# Invoice Generator

A lightweight desktop application that generates professional **GST tax invoices as PDF files**. Built with Python, Tkinter and ReportLab.

Fill in the buyer details, add your items, and get a print-ready A4 invoice in one click.

---

## Features

- Simple desktop GUI, no browser or server required
- Dynamic item rows: add or remove line items as needed
- Automatic **CGST (9%)** and **SGST (9%)** calculation
- Amounts formatted in the **Indian numbering system** (e.g. `1,00,000.00`)
- Grand total converted to **words in rupees and paise**
- Company logo and quality-mark logo support (optional)
- Bank details, terms and signature block included on every invoice
- Business details kept in a separate config file, so no private data lives in the code

## Tech Stack

| Component | Purpose |
|-----------|---------|
| Python 3.8+ | Language |
| Tkinter | GUI (ships with Python) |
| ReportLab | PDF generation |
| num2words | Amount in words |

## Project Structure

```
invoice-generator/
├── shop.py                 # Main application
├── config.example.json     # Template for your business details
├── config.json             # Your real details (create this, not tracked by Git)
├── requirements.txt        # Python dependencies
├── logo.png                # Optional: company logo (not tracked by Git)
├── logo2.png               # Optional: second logo / quality mark (not tracked by Git)
└── .gitignore
```

## Getting Started

### 1. Prerequisites

Install **Python 3.8 or newer** from [python.org](https://www.python.org/downloads/).

On Windows, tick **"Add Python to PATH"** on the first screen of the installer.

Verify the installation:

```bash
python --version
```

### 2. Clone the repository

```bash
git clone https://github.com/Raghavendra-01/invoice-generator.git
cd invoice-generator
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

Or install them directly:

```bash
pip install reportlab num2words
```

### 4. Configure your business details

Copy the example config and edit it with your own information:

**Windows**
```bash
copy config.example.json config.json
```

**macOS / Linux**
```bash
cp config.example.json config.json
```

Open `config.json` in any text editor and fill in your details:

```json
{
  "company_name": "YOUR COMPANY NAME",
  "gstin": "00XXXXX0000X0XX",
  "address": "Door No, Street, Area, City - PIN",
  "tagline": "Manufacturers & Suppliers : YOUR PRODUCTS",
  "phone": "00000 00000, 00000 00000",
  "state": "Your State",
  "state_code": "00",
  "hsn_code": "00000000",
  "jurisdiction": "YourCity",
  "bank": {
    "account_name": "YOUR COMPANY NAME",
    "bank_name": "YOUR BANK NAME",
    "account_no": "000000000000000",
    "branch": "BRANCH, CITY",
    "ifsc": "XXXX0000000"
  }
}
```

| Field | Description |
|-------|-------------|
| `company_name` | Name printed in the invoice header and signature block |
| `gstin` | Your 15-character GST identification number |
| `address` | Business address line |
| `tagline` | Short description of your business |
| `phone` | Contact number(s) |
| `state` / `state_code` | State name and GST state code |
| `hsn_code` | HSN code for the goods you sell |
| `jurisdiction` | City named in the "Subject to ... Jurisdiction" term |
| `bank` | Bank account details printed in the payment box |

### 5. (Optional) Add logos

Place `logo.png` (top left) and `logo2.png` (top right) in the project folder. If a logo file is missing, the invoice is generated without it.

### 6. Run the application

```bash
python shop.py
```

## Usage

1. Fill in the invoice details:
   - Buyer Name
   - DEL AT
   - GST No.
   - Invoice No.
   - Invoice Date
   - Transport Mode
   - Vehicle No.
   - Place of Delivery
2. Enter the **Description**, **Qty** and **Price** for each item. Click **Add Item** for more rows, or **Delete Item** to remove the last row.
3. Click **Generate Invoice**.
4. The PDF is saved in the project folder, named after the **Place of Delivery** (for example `Guntur.pdf`).

> **Note:** The file name comes from the Place of Delivery, so two invoices to the same place will overwrite each other. Move or rename the earlier PDF first.

## Security and Privacy

This project is designed so that sensitive information never reaches version control.

- `config.json` contains your GSTIN, phone numbers and bank details. It is listed in `.gitignore` and **must never be committed**.
- Generated `*.pdf` invoices contain customer details and are also ignored.
- Before every push, run `git status` and confirm that `config.json` is not listed.

If you accidentally commit sensitive data, changing the file is not enough, because it remains in the Git history. Remove it with [`git filter-repo`](https://github.com/newren/git-filter-repo) or recreate the repository, and treat the exposed details as compromised.

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `python is not recognized` | Reinstall Python and tick **Add Python to PATH**, then reopen the terminal |
| `config.json not found` | Create it from `config.example.json` and keep it in the same folder as `shop.py` |
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` |
| Logo not showing | Check that the file is named exactly `logo.png` or `logo2.png` and sits beside `shop.py` |
| Wrong tax rate | Update the `0.09` values for CGST and SGST in `shop.py` |

## Roadmap

- [ ] Unique invoice file names (invoice number and date)
- [ ] Per-item unit of measure and HSN code
- [ ] Configurable tax rates and IGST support
- [ ] Save and reload buyer details
- [ ] Packaged `.exe` for Windows

## Contributing

Contributions are welcome. Fork the repository, create a feature branch, and open a pull request. Please do not include any real business or customer data in commits, issues or screenshots.

## License

Add a license of your choice (for example [MIT](https://choosealicense.com/licenses/mit/)) before making this repository public.
