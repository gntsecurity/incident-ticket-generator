import tkinter as tk
from tkinter import messagebox, ttk, font
import csv
import os
from datetime import datetime

# Constants
CSV_FILE = 'tickets.csv'

# Helper functions
def load_tickets():
    tickets = []
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                tickets.append(row)
    return tickets

def save_ticket(ticket):
    tickets = load_tickets()
    tickets.append(ticket)
    with open(CSV_FILE, 'w', newline='') as file:
        fieldnames = ['Ticket ID', 'Date', 'Type', 'Priority', 'Description', 'Status']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(tickets)

def search_tickets(query):
    tickets = load_tickets()
    return [ticket for ticket in tickets if query.lower() in ticket['Type'].lower() or query.lower() in ticket['Priority'].lower() or query.lower() in ticket['Description'].lower()]

# GUI setup
root = tk.Tk()
root.title("Incident Ticket Generator")
root.geometry("800x600")
root.config(bg="#f4f4f4")

# Fonts
header_font = font.Font(family="Arial", size=14, weight="bold")
label_font = font.Font(family="Arial", size=10)

# GUI components
frame = tk.Frame(root, bg="#f4f4f4")
frame.pack(pady=10)

# Header label
header = tk.Label(root, text="Incident Ticket Generator", font=header_font, bg="#3B3B3B", fg="#FFFFFF", pady=10)
header.pack(fill=tk.X)

# Entry fields
tk.Label(frame, text="Ticket Type:", font=label_font, bg="#f4f4f4").grid(row=0, column=0, padx=10, pady=5, sticky="e")
type_entry = tk.Entry(frame, width=40)
type_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(frame, text="Priority (Low, Medium, High):", font=label_font, bg="#f4f4f4").grid(row=1, column=0, padx=10, pady=5, sticky="e")
priority_entry = tk.Entry(frame, width=40)
priority_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(frame, text="Description:", font=label_font, bg="#f4f4f4").grid(row=2, column=0, padx=10, pady=5, sticky="e")
description_entry = tk.Entry(frame, width=40)
description_entry.grid(row=2, column=1, padx=10, pady=5)

tk.Label(frame, text="Status (Open, In Progress, Resolved):", font=label_font, bg="#f4f4f4").grid(row=3, column=0, padx=10, pady=5, sticky="e")
status_entry = tk.Entry(frame, width=40)
status_entry.grid(row=3, column=1, padx=10, pady=5)

# Functions for ticket actions
def create_ticket():
    ticket_id = f"TKT{len(load_tickets()) + 1:04d}"
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ticket = {
        "Ticket ID": ticket_id,
        "Date": date,
        "Type": type_entry.get(),
        "Priority": priority_entry.get(),
        "Description": description_entry.get(),
        "Status": status_entry.get()
    }
    save_ticket(ticket)
    messagebox.showinfo("Success", f"Ticket {ticket_id} created successfully.")
    clear_entries()
    load_table()

def search_tickets_display():
    query = search_entry.get()
    results = search_tickets(query)
    load_table(results)

def clear_entries():
    type_entry.delete(0, tk.END)
    priority_entry.delete(0, tk.END)
    description_entry.delete(0, tk.END)
    status_entry.delete(0, tk.END)

# Ticket table
tree = ttk.Treeview(root, columns=('Ticket ID', 'Date', 'Type', 'Priority', 'Description', 'Status'), show='headings', height=10)
tree.heading('Ticket ID', text='Ticket ID')
tree.heading('Date', text='Date')
tree.heading('Type', text='Type')
tree.heading('Priority', text='Priority')
tree.heading('Description', text='Description')
tree.heading('Status', text='Status')
tree.pack(pady=20, padx=20, fill=tk.X)

# Styling the table
style = ttk.Style()
style.configure("Treeview.Heading", font=("Arial", 10, "bold"))
style.configure("Treeview", rowheight=25, font=("Arial", 9))

# Load data into table
def load_table(data=None):
    for row in tree.get_children():
        tree.delete(row)
    tickets = data if data else load_tickets()
    for ticket in tickets:
        tree.insert("", tk.END, values=(ticket['Ticket ID'], ticket['Date'], ticket['Type'], ticket['Priority'], ticket['Description'], ticket['Status']))

load_table()

# Buttons
button_frame = tk.Frame(root, bg="#f4f4f4")
button_frame.pack(pady=10)

create_button = tk.Button(button_frame, text="Create Ticket", command=create_ticket, font=label_font, bg="#4CAF50", fg="white", padx=10, pady=5)
create_button.grid(row=0, column=0, padx=10)

# Search feature
search_frame = tk.Frame(root, bg="#f4f4f4")
search_frame.pack(pady=10)

tk.Label(search_frame, text="Search:", font=label_font, bg="#f4f4f4").pack(side=tk.LEFT, padx=5)
search_entry = tk.Entry(search_frame, width=40)
search_entry.pack(side=tk.LEFT, padx=5)
search_button = tk.Button(search_frame, text="Search", command=search_tickets_display, font=label_font, bg="#2196F3", fg="white", padx=10, pady=5)
search_button.pack(side=tk.LEFT)

root.mainloop()
