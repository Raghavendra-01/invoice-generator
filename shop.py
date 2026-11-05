from tkinter import *
from tkinter import messagebox
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas 
from reportlab.lib.utils import ImageReader
from num2words import num2words
import os
import json
import sys

# Note: Replace these with actual image paths
LOGO_PATH = "logo.png"  # Path to your company logo
LOGO2_PATH = "logo2.png"  # Path to your ISI mark logo

# Private business details live in config.json (NOT committed to GitHub).
# Copy config.example.json to config.json and fill in your real details.
CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")
try:
    with open(CONFIG_PATH, encoding="utf-8") as f:
        CFG = json.load(f)
except FileNotFoundError:
    sys.exit("config.json not found. Copy config.example.json to config.json and fill in your details.")

BANK = CFG["bank"]

def format_indian(number):
    """Format numbers with commas as per Indian numbering system (1,00,000)"""
    number = float(number)
    num_str = "{:.2f}".format(number)
    if '.' in num_str:
        integer_part, decimal_part = num_str.split('.')
    else:
        integer_part, decimal_part = num_str, '00'
    
    # Process integer part
    if len(integer_part) > 3:
        last_three = integer_part[-3:]
        other_numbers = integer_part[:-3]
        integer_part = ','.join([
            other_numbers[max(i-2,0):i] for i in range(len(other_numbers), 0, -2)
        ][::-1]) + ',' + last_three
    return f"{integer_part}.{decimal_part}"

def generate_invoice():
    try:
        delivery_place = entry_delivery.get()
        file_name = f"{delivery_place}.pdf"
        c = canvas.Canvas(file_name, pagesize=A4)
        width, height = A4
        
        # Draw logos if they exist
        try:
            logo = ImageReader(LOGO_PATH)
            c.drawImage(logo, 30, height - 80, width=80, height=60, preserveAspectRatio=True)
        except:
            pass
            
        try:
            logo2 = ImageReader(LOGO2_PATH)
            c.drawImage(logo2, width - 130, height - 80, width=120, height=80, preserveAspectRatio=True)
        except:
            pass

        # Company Header
        c.setFont("Helvetica-Bold", 22)
        c.drawString(120, height - 50, CFG["company_name"])
        c.setFont("Helvetica-Bold", 12)
        c.drawString(120, height - 70, f"GSTIN : {CFG['gstin']}")
        c.setFont("Helvetica", 10)
        c.drawString(120, height - 85, CFG["address"])
        c.drawString(120, height - 100, CFG["tagline"])
        c.drawString(120, height - 115, f"Cell : {CFG['phone']}")
        c.setFont("Helvetica-Bold", 14)
        c.drawString(270, height - 135, "TAX INVOICE")
        c.setFont("Helvetica-Bold", 14)
        c.drawString(420, height - 135, "Original : FOR BUYER")
        
        # Buyer Info with DEL AT
        c.setFont("Helvetica", 11)
        c.drawString(30, height - 170, f"Name of the Buyer : {entry_buyer.get()}")
        c.drawString(30, height - 190, f"DEL AT : {entry_del_at.get()}")
        c.drawString(350, height - 170, f"Invoice No. : {entry_invoice.get()}")
        c.drawString(30, height - 210, f"GST No: {entry_gst.get()}")
        c.drawString(350, height - 190, f"Invoice Date : {entry_date.get()}")
        c.drawString(30, height - 230, f"State : {CFG['state']}")
        c.drawString(350, height - 210, f"Transportation Mode : {entry_transport.get()}")
        c.drawString(30, height - 250, f"Code : {CFG['state_code']}")
        c.drawString(350, height - 230, f"Vehicle Number : {entry_vehicle.get()}")
        c.drawString(30, height - 270, f"HSN Code : {CFG['hsn_code']}")
        c.drawString(350, height - 250, f"Place of Delivery : {delivery_place}")

        # Table Headers (simplified without "of Goods" in description)
        c.setFont("Helvetica-Bold", 11)
        headers = ["Sl. No.", "Description of Goods", "UOM", "Qty", "Price of Goods ", "Amount"]
        x_positions = [30, 70, 270, 330, 400, 520]
        for i, header in enumerate(headers):
            c.drawString(x_positions[i], height - 295, header)

        c.line(25, height - 300, 580, height - 300)

        # Table Content with "of Goods" below Price
        y = height - 320
        total = 0
        for i in range(len(item_desc)):
            desc = item_desc[i].get()
            qty = float(item_qty[i].get()) if item_qty[i].get() else 0
            price = float(item_price[i].get()) if item_price[i].get() else 0
            amt = qty * price
            total += amt
            c.setFont("Helvetica", 10)
            c.drawString(30, y, str(i + 1))
            c.drawString(70, y, desc)  # Description without "of Goods"
            c.drawString(270, y, "MTS")
            c.drawString(330, y, format_indian(qty))
            c.drawString(400, y, format_indian(price))  # Price value
            c.drawString(520, y, format_indian(amt))
            y -= 25

        # GST and Total with Indian formatting
        cgst = total * 0.09
        sgst = total * 0.09
        grand_total = total + cgst + sgst
        y -= 20
        c.setFont("Helvetica-Bold", 11)
        c.drawString(400, y, f"CGST (9.0%):                  {format_indian(cgst)}")
        y -= 20
        c.drawString(400, y, f"SGST (9.0%):                  {format_indian(sgst)}")
        y -= 20
        c.setFont("Helvetica-Bold", 14)
        c.drawString(400, y, f"Grand Total:   {format_indian(grand_total)}")

        # Amount in words
        y -= 30
        c.setFont("Helvetica", 11)
        amount_words = num2words(grand_total, to='currency', lang='en_IN').replace('euro', 'rupees').replace('cents', 'paise')
        c.drawString(30, y, f"In Words : {amount_words.capitalize()} Only")
        y -= 40  # Extra space before box

        # Bank Details Box (strictly contained)
        box_height = 150
        box_y_start = y - box_height
        c.rect(30, box_y_start, 220, box_height)
        
        # Bank details inside box
        c.setFont("Helvetica-Bold", 13)
        c.drawString(40, box_y_start + box_height - 20, "BANK A/C. DETAILS :")
        c.setFont("Helvetica", 11)
        c.drawString(40, box_y_start + box_height - 40, BANK["account_name"])
        c.drawString(40, box_y_start + box_height - 60, BANK["bank_name"])
        c.drawString(40, box_y_start + box_height - 80, f"A/c No: {BANK['account_no']}")
        c.drawString(40, box_y_start + box_height - 100, BANK["branch"])
        c.drawString(40, box_y_start + box_height - 120, f"IFSC : {BANK['ifsc']}")

        y -= 170
        c.setFont("Helvetica", 10)
        c.drawString(30, y, "Note : Terms and Conditions")
        c.drawString(30, y-15, "1. Certified that the Particulars given above are true and correct")
        c.drawString(30, y - 30, f"2. Subject to {CFG['jurisdiction']} Jurisdiction")
        c.drawString(30, y - 45, "3. Goods once sold cannot taken back or exchange")

        # Signature on right side
        c.setFont("Helvetica-Bold", 12)
        c.drawString(400, y + box_height - 50, f"For {CFG['company_name']}")
        c.drawString(400, y + box_height - 110, "Authorized Signature")

        c.save()
        messagebox.showinfo("Success", f"Invoice saved as '{file_name}'")

    except Exception as e:
        messagebox.showerror("Error", str(e))

def delete_item():
    if len(item_desc) > 1:
        item_desc[-1].destroy()
        item_qty[-1].destroy()
        item_price[-1].destroy()
        item_desc.pop()
        item_qty.pop()
        item_price.pop()
    else:
        messagebox.showwarning("Warning", "You must keep at least one item row")

# GUI
root = Tk()
root.title(f"Invoice Generator - {CFG['company_name']}")
root.geometry("800x700")

# Main frame
main_frame = Frame(root, padx=20, pady=20)
main_frame.pack(fill=BOTH, expand=True)

# Input fields
fields = [
    "Buyer Name", 
    "DEL AT",
    "GST No.", 
    "Invoice No.", 
    "Invoice Date", 
    "Transport Mode", 
    "Vehicle No.", 
    "Place of Delivery"
]
entries = []
for i, field in enumerate(fields):
    frame = Frame(main_frame)
    frame.pack(fill=X, pady=5)
    Label(frame, text=field, width=15, anchor='w').pack(side=LEFT)
    e = Entry(frame, width=50)
    e.pack(side=LEFT, padx=10)
    entries.append(e)

entry_buyer, entry_del_at, entry_gst, entry_invoice, entry_date, entry_transport, entry_vehicle, entry_delivery = entries

# Items table
items_frame = Frame(main_frame)
items_frame.pack(fill=BOTH, pady=10)

Label(items_frame, text="Description", width=30, anchor='w').grid(row=0, column=0, padx=5)
Label(items_frame, text="Qty", width=8, anchor='w').grid(row=0, column=1, padx=5)
Label(items_frame, text="Price", width=10, anchor='w').grid(row=0, column=2, padx=5)

item_desc, item_qty, item_price = [], [], []

def add_item_row():
    row = len(item_desc) + 1
    d = Entry(items_frame, width=30)
    d.grid(row=row, column=0, padx=5, pady=2)
    q = Entry(items_frame, width=8)
    q.grid(row=row, column=1, padx=5, pady=2)
    p = Entry(items_frame, width=10)
    p.grid(row=row, column=2, padx=5, pady=2)
    item_desc.append(d)
    item_qty.append(q)
    item_price.append(p)

add_item_row()

# Buttons
button_frame = Frame(main_frame)
button_frame.pack(fill=X, pady=20)

Button(button_frame, text="Add Item", command=add_item_row, width=15).pack(side=LEFT, padx=10)
Button(button_frame, text="Delete Item", command=delete_item, width=15).pack(side=LEFT, padx=10)
Button(button_frame, text="Generate Invoice", command=generate_invoice, width=15).pack(side=LEFT, padx=10)

root.mainloop()
