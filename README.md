# 🛒 Grocery Shop Management System

A desktop GUI application built with **Python (Tkinter)** and **MySQL** to streamline inventory tracking, stock management, and customer billing for a grocery store. *(Originally developed as a Class 12 Computer Science project).*

## ✨ Features
* **Database Integration:** Connects Python directly to a MySQL database for persistent storage of inventory and sales records.
* **Inventory Management (CRUD):** Add new grocery items, update stock quantities/prices, search products, and delete outdated records.
* **Automated Billing System:** Calculate item totals, generate customer bills, and automatically deduct purchased quantities from stock.
* **User-Friendly GUI:** Clean, form-based desktop interface built with Tkinter for fast data entry.

## 🛠️ Tech Stack
* **Language:** Python 3
* **GUI Framework:** Tkinter
* **Database:** MySQL
* **Connector:** `mysql-connector-python`

## ⚙️ Prerequisites & Setup
1. **Install the MySQL Connector:**
   ```bash
   pip install mysql-connector-python
   ```
2. **Database Configuration:**
   * Ensure MySQL Server is running on your machine.
   * Create the required database and tables (update the host, user, and password fields inside `Grocery Shop Management.py` to match your local MySQL credentials).

## 🚀 How to Run
1. Clone the repository:
   ```bash
   git clone https://github.com
   ```
2. Navigate to the project directory and run the application:
   ```bash
   python "Grocery Shop Management.py"
   ```
