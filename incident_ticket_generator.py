import tkinter as tk
from tkinter import messagebox, ttk
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

# GUI components
frame = tk.Frame(root)
frame.pack(pady=10)

tk.Label(frame, text="Ticket Type:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
type_entry = tk.Entry(frame, width=30)
type_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame, text="Priority (Low, Medium, High):").grid(row=1, column=0, padx=5, pady=5, sticky="e")
priority_entry = tk.Entry(frame, width=30)
priority_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame, text="Description:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
description_entry = tk.Entry(frame, width=30)
description_entry.grid(row=2, column=1, padx=5, pady=5)

tk.Label(frame, text="Status (Open, In Progress, Resolved):").grid(row=3, column=0, padx=5, pady=5, sticky="e")
status_entry = tk.Entry(frame, width=30)
status_entry.grid(row=3, column=1, padx=5, pady=5)

def create_ticket():
    ticket_id = f"TKT{len(load_tickets()) + 1:04d}"  # Generates a unique ticket ID
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

# Tickets table
tree = ttk.Treeview(root, columns=('Ticket ID', 'Date', 'Type', 'Priority', 'Description', 'Status'), show='headings')
tree.heading('Ticket ID', text='Ticket ID')
tree.heading('Date', text='Date')
tree.heading('Type', text='Type')
tree.heading('Priority', text='Priority')
tree.heading('Description', text='Description')
tree.heading('Status', text='Status')
tree.pack(pady=10)

def load_table(data=None):
    for row in tree.get_children():
        tree.delete(row)
    tickets = data if data else load_tickets()
    for ticket in tickets:
        tree.insert("", tk.END, values=(ticket['Ticket ID'], ticket['Date'], ticket['Type'], ticket['Priority'], ticket['Description'], ticket['Status']))

load_table()

# Buttons
tk.Button(root, text="Create Ticket", command=create_ticket).pack(pady=5)

# Search feature
search_frame = tk.Frame(root)
search_frame.pack(pady=5)
tk.Label(search_frame, text="Search:").pack(side=tk.LEFT)
search_entry = tk.Entry(search_frame, width=30)
search_entry.pack(side=tk.LEFT, padx=5)
tk.Button(search_frame, text="Search", command=search_tickets_display).pack(side=tk.LEFT)

root.mainloop()
