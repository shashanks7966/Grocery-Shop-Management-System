import sqlite3 as sql
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog  # Packages
import matplotlib.pyplot as plt

# 1. DATABASE CONNECTION & INITIALIZATION
try:
    conn = sql.connect("grocery_shop.db")
    cursor = conn.cursor()
    print("Database connected successfully.")
    
    # AUTOMATIC TABLE SETUP (Ensures app works out of the box on any PC)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customer_details (
            phone_no INTEGER PRIMARY KEY,
            cust_name TEXT NOT NULL,
            cost REAL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS product_details (
            product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT NOT NULL,
            product_quantity_remaining REAL NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS worker_details (
            worker_id INTEGER PRIMARY KEY AUTOINCREMENT,
            worker_name TEXT NOT NULL,
            salary REAL
        )
    ''')
    conn.commit()
    print("Database tables verified/created successfully.")
    
except Exception as e:
    print(f"Error connecting to database: {e}")

# 2. LOGIN LOGIC
def validate_login():
    username = entry_user.get()
    password = entry_pass.get()
    
    if username == 'tapas' and password == 'tapas123':
        login_window.withdraw()
        main_menu()
    else:
        messagebox.showerror("Login Failed", "Invalid Username or Password")

#3.CATALOG UPDATING
def add_product():
    sub = tk.Toplevel()
    sub.title("Add Product to Catalog")
    sub.geometry("300x250")
    
    tk.Label(sub, text="Product Name:").pack(pady=5)
    en = tk.Entry(sub); en.pack()
    tk.Label(sub, text="Quantity Remaining:").pack(pady=5)
    eq = tk.Entry(sub); eq.pack()

    def save_prod():
        try:
            # Basic validation
            if not en.get() or not eq.get():
                messagebox.showerror("Error", "All fields are required!")
                return
                
            query = "INSERT INTO product_details (product_name, product_quantity_remaining) VALUES (?, ?)"
            cursor.execute(query, (en.get(), float(eq.get())))
            conn.commit()
            
            messagebox.showinfo("Success", f"'{en.get()}' added to catalog successfully!")
            sub.destroy()
        except ValueError:
            messagebox.showerror("Error", "Quantity must be a valid number!")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    tk.Button(sub, text="Add Product", command=save_prod, bg="blue", fg="white").pack(pady=20)


# 4. FUNCTIONALITY FOR BUTTONS
def add_customer():
    sub = tk.Toplevel()
    sub.title("Add Customer")
    sub.geometry("300x250")
    
    tk.Label(sub, text="Name:").pack()
    en = tk.Entry(sub); en.pack()
    tk.Label(sub, text="Phone:").pack()
    ep = tk.Entry(sub); ep.pack()
    tk.Label(sub, text="Bill Amount:").pack()
    ec = tk.Entry(sub); ec.pack()

    def save():
        try:
            query = "INSERT INTO customer_details (phone_no, cust_name, cost) VALUES (?, ?, ?)"
            cursor.execute(query, (int(ep.get()), en.get(), float(ec.get())))
            conn.commit()
            messagebox.showinfo("Success", "Customer Added Successfully!")
            sub.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    tk.Button(sub, text="Submit", command=save, bg="green", fg="white").pack(pady=10)

def view_all(table_name):
    view_win = tk.Toplevel()
    view_win.title(f"Viewing {table_name}")
    
    txt = tk.Text(view_win, height=15, width=50)
    txt.pack()
    
    try:
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        
        if not rows:
            txt.insert(tk.END, "No records found in this table.")
        for r in rows:
            txt.insert(tk.END, f"{r}\n")
    except Exception as e:
        messagebox.showerror("Error", f"Could not fetch data: {str(e)}")

def show_pie_chart():
    try:
        cursor.execute('SELECT product_name, product_quantity_remaining FROM product_details')
        records = cursor.fetchall()
        
        if not records:
            messagebox.showwarning("No Data", "No product data found in database.\nAdd records directly to 'grocery_shop.db' to see a chart.")
            return

        items = [r[0] for r in records]
        quantities = [r[1] for r in records]
        
        plt.figure(figsize=(7,7))
        plt.pie(quantities, labels=items, autopct='%1.1f%%', startangle=140)
        plt.title('Stock Availability 2026')
        plt.show()
    except Exception as e:
        messagebox.showerror("Error", str(e))

# 5. MAIN MENU WINDOW
def main_menu():
    menu = tk.Toplevel()
    menu.title("Grocery Management System - Dashboard")
    menu.geometry("400x550")
    
    try:
        menu.iconbitmap('Grocery Shop.ico')
    except:
        pass # Safely ignore if the .ico asset is missing
    
    tk.Label(menu, text="Select an Operation", font=("Arial", 14, "bold")).pack(pady=10)

    buttons = [
        ("Add Customer Details", add_customer),
        ("Add Product to Catalog", add_product),
        ("See All Customers", lambda: view_all("customer_details")),
        ("See All Products", lambda: view_all("product_details")),
        ("See All Workers", lambda: view_all("worker_details")),
        ("Stock Pie Chart", show_pie_chart),
        ("Logout", lambda: [menu.destroy(), login_window.deiconify()])
    ]

    for text, func in buttons:
        tk.Button(menu, text=text, command=func, width=25, pady=5).pack(pady=5)

# 5. INITIAL LOGIN WINDOW
login_window = tk.Tk()
login_window.title("Grocery Shop Login")
login_window.geometry("300x350")

try:
    login_window.iconbitmap('Grocery Shop.ico')
    photo = tk.PhotoImage(file="Grocery Shop.png").subsample(2)
    tk.Label(login_window, image=photo).pack(pady=10)
except:
    tk.Label(login_window, text="GROCERY SHOP", font=("Helvetica", 18)).pack(pady=20)

tk.Label(login_window, text="Username:").pack()
entry_user = tk.Entry(login_window)
entry_user.pack()

tk.Label(login_window, text="Password:").pack()
entry_pass = tk.Entry(login_window, show="*")
entry_pass.pack()

tk.Button(login_window, text="Login", command=validate_login, width=15, bg="green", fg="white").pack(pady=20)
tk.Button(login_window, text="Exit", command=login_window.destroy, width=15).pack()

login_window.mainloop()
