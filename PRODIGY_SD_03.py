import tkinter as tk
from tkinter import messagebox
import json
import os

class ContactManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Management System")
        
        self.contacts = self.load_contacts()

        self.name_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.email_var = tk.StringVar()
        
        self.create_widgets()
    
    def create_widgets(self):
        # Add Contact Section
        tk.Label(self.root, text="Name").grid(row=0, column=0, padx=10, pady=5)
        tk.Entry(self.root, textvariable=self.name_var).grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self.root, text="Phone").grid(row=1, column=0, padx=10, pady=5)
        tk.Entry(self.root, textvariable=self.phone_var).grid(row=1, column=1, padx=10, pady=5)

        tk.Label(self.root, text="Email").grid(row=2, column=0, padx=10, pady=5)
        tk.Entry(self.root, textvariable=self.email_var).grid(row=2, column=1, padx=10, pady=5)

        tk.Button(self.root, text="Add Contact", command=self.add_contact).grid(row=3, column=0, columnspan=2, pady=10)

        # Contacts List Section
        self.contacts_listbox = tk.Listbox(self.root, height=10, width=50)
        self.contacts_listbox.grid(row=4, column=0, columnspan=2, padx=10, pady=10)
        self.contacts_listbox.bind("<<ListboxSelect>>", self.on_select)

        tk.Button(self.root, text="Edit Contact", command=self.edit_contact).grid(row=5, column=0, pady=10)
        tk.Button(self.root, text="Delete Contact", command=self.delete_contact).grid(row=5, column=1, pady=10)

        self.update_contacts_listbox()

    def add_contact(self):
        name = self.name_var.get()
        phone = self.phone_var.get()
        email = self.email_var.get()

        if name and phone and email:
            self.contacts[name] = {"phone": phone, "email": email}
            self.save_contacts()
            self.update_contacts_listbox()
            self.clear_entries()
        else:
            messagebox.showwarning("Input Error", "All fields are required")

    def edit_contact(self):
        selected_contact = self.get_selected_contact()
        if selected_contact:
            name = self.name_var.get()
            phone = self.phone_var.get()
            email = self.email_var.get()

            if name and phone and email:
                del self.contacts[selected_contact]
                self.contacts[name] = {"phone": phone, "email": email}
                self.save_contacts()
                self.update_contacts_listbox()
                self.clear_entries()
            else:
                messagebox.showwarning("Input Error", "All fields are required")

    def delete_contact(self):
        selected_contact = self.get_selected_contact()
        if selected_contact:
            del self.contacts[selected_contact]
            self.save_contacts()
            self.update_contacts_listbox()
            self.clear_entries()

    def on_select(self, event):
        try:
            selected_contact = self.contacts_listbox.get(self.contacts_listbox.curselection())
            self.name_var.set(selected_contact)
            self.phone_var.set(self.contacts[selected_contact]["phone"])
            self.email_var.set(self.contacts[selected_contact]["email"])
        except tk.TclError:
            pass

    def update_contacts_listbox(self):
        self.contacts_listbox.delete(0, tk.END)
        for contact in self.contacts:
            self.contacts_listbox.insert(tk.END, contact)

    def clear_entries(self):
        self.name_var.set("")
        self.phone_var.set("")
        self.email_var.set("")

    def load_contacts(self):
        if os.path.exists("contacts.json"):
            with open("contacts.json", "r") as file:
                return json.load(file)
        return {}

    def save_contacts(self):
        with open("contacts.json", "w") as file:
            json.dump(self.contacts, file)

    def get_selected_contact(self):
        try:
            return self.contacts_listbox.get(self.contacts_listbox.curselection())
        except tk.TclError:
            messagebox.showwarning("Selection Error", "No contact selected")
            return None

if __name__ == "__main__":
    root = tk.Tk()
    app = ContactManager(root)
    root.mainloop()
