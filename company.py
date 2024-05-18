import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import mysql.connector
import requests
import datetime
import pyttsx3 as pt
from io import BytesIO

speech = pt.init()
def speak(text):
    speech.say(text)
    speech.runAndWait()
def greet():
    current_hour = datetime.datetime.now().hour
    if 0 <= current_hour < 12:
        speak("Good morning !")
    elif 12 <= current_hour < 18:
        speak("Good afternoon !")
    else:
        speak("Good evening !")


# Database setup
def create_database():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='NC5ZQY@123',
        database='TechSolutions_Inc'
    )
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            position VARCHAR(255) NOT NULL,
            department VARCHAR(255) NOT NULL,
            salary FLOAT NOT NULL,
            phone_number VARCHAR(20),
            gender VARCHAR(10),
            photo VARCHAR(255) DEFAULT 'https://thumbs.dreamstime.com/b/3d-human-ok-16682223.jpg'
        )
    ''')
    
    conn.commit()
    conn.close()

create_database()

# GUI Application
def add_employee():
    name = name_entry.get()
    position = position_entry.get()
    department = department_entry.get()
    salary = salary_entry.get()
    phone_number = phone_entry.get()
    gender = gender_var.get()
    photo = photo_entry.get()
    
    if not name or not position or not department or not salary or not phone_number or not gender:
        messagebox.showerror("Error", "All fields except photo are required")
        return

    try:
        salary = float(salary)
    except ValueError:
        messagebox.showerror("Error", "Salary must be a number")
        return

    if not photo:
        photo = 'https://thumbs.dreamstime.com/b/3d-human-ok-16682223.jpg'

    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='NC5ZQY@123',
        database='TechSolutions_Inc'
    )
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO employees (name, position, department, salary, phone_number, gender, photo)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    ''', (name, position, department, salary, phone_number, gender, photo))
    
    conn.commit()
    conn.close()
    #messagebox.showinfo("Success", "Employee added successfully")
    speak("Employee added successfully")
    clear_entries()
    view_employees()

def clear_entries():
    name_entry.delete(0, tk.END)
    position_entry.delete(0, tk.END)
    department_entry.delete(0, tk.END)
    salary_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    gender_var.set("")
    photo_entry.delete(0, tk.END)
    photo_label.config(image=None)  # Clear the photo label

def view_employees(order_by=None):
    
    for row in employee_tree.get_children():
        employee_tree.delete(row)
    
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='NC5ZQY@123',
        database='TechSolutions_Inc'
    )
    cursor = conn.cursor()
    query = 'SELECT * FROM employees'
    if order_by:
        query += f' ORDER BY {order_by}'
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()
    
    for row in rows:
        employee_tree.insert("", tk.END, values=row)

def delete_employee():
    selected_item = employee_tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "Please select an employee to delete")
        return
    
    employee_id = employee_tree.item(selected_item[0])['values'][0]
    
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='NC5ZQY@123',
        database='TechSolutions_Inc'
    )
    cursor = conn.cursor()
    cursor.execute('DELETE FROM employees WHERE id=%s', (employee_id,))
    conn.commit()
    conn.close()
    #messagebox.showinfo("Success", "Employee deleted successfully")
    speak("Employee deleted successfully")
    view_employees()

def update_employee():
    selected_item = employee_tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "Please select an employee to update")
        return

    name = name_entry.get()
    position = position_entry.get()
    department = department_entry.get()
    salary = salary_entry.get()
    phone_number = phone_entry.get()
    gender = gender_var.get()
    photo = photo_entry.get()

    if not name or not position or not department or not salary or not phone_number or not gender:
        messagebox.showerror("Error", "All fields except photo are required")
        return

    try:
        salary = float(salary)
    except ValueError:
        messagebox.showerror("Error", "Salary must be a number")
        return

    if not photo:
        photo = 'https://thumbs.dreamstime.com/b/3d-human-ok-16682223.jpg'

    employee_id = employee_tree.item(selected_item[0])['values'][0]

    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='NC5ZQY@123',
        database='TechSolutions_Inc'
    )
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE employees
        SET name=%s, position=%s, department=%s, salary=%s, phone_number=%s, gender=%s, photo=%s
        WHERE id=%s
    ''', (name, position, department, salary, phone_number, gender, photo, employee_id))

    conn.commit()
    conn.close()
    #messagebox.showinfo("Success", "Employee updated successfully")
    speak("Employee updated successfully")
    view_employees()

def search_employees():
    search_query = search_entry.get()
    if not search_query:
        view_employees()
        return
    
    for row in employee_tree.get_children():
        employee_tree.delete(row)
    
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='NC5ZQY@123',
        database='TechSolutions_Inc'
    )
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM employees WHERE name LIKE %s', (f'%{search_query}%',))
    rows = cursor.fetchall()
    conn.close()
    
    for row in rows:
        employee_tree.insert("", tk.END, values=row)

def add_button_hover_effects(button):
    def on_enter(event):
        button['bg'] = '#006dbf'
    def on_leave(event):
        button['bg'] = button_bg

    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)

app = tk.Tk()
app.title("TechSolutions Inc. - Employee Management System")

# Set window size
app.geometry("1000x600")

# Styling
style = ttk.Style()
style.configure("TLabel", font=("Helvetica", 14))
style.configure("TButton", font=("Helvetica", 14))
style.configure("TEntry", font=("Helvetica", 14))
style.configure("Treeview.Heading", font=("Helvetica", 14, "bold"))
style.configure("Treeview", font=("Helvetica", 12))

# Colors
bg_color = "#fff7fc"
header_bg = "#8ee5ee"
header_fg = "#000000"
button_bg = "#00bfff"
button_fg = "#000000"

app.configure(bg=bg_color)

# Company Header
header_frame = tk.Frame(app, bg=header_bg, pady=10)
header_frame.pack(fill=tk.X)

company_name = tk.Label(header_frame, text="TechSolutions Inc.", font=("Helvetica", 20, "bold"), bg=header_bg, fg=header_fg)
company_name.pack()

tagline = tk.Label(header_frame, text="Innovating Tomorrow's Solutions Today", font=("Helvetica", 14), bg=header_bg, fg=header_fg)
tagline.pack()

# Input Form in a labeled frame
input_frame = ttk.LabelFrame(app, text="Employee Details", padding=(20, 10))
input_frame.pack(side=tk.LEFT, fill=tk.Y, padx=20, pady=20)

tk.Label(input_frame, text="Name", bg=bg_color).grid(row=0, column=0, padx=10, pady=5, sticky="e")
tk.Label(input_frame, text="Position", bg=bg_color).grid(row=1, column=0, padx=10, pady=5, sticky="e")
tk.Label(input_frame, text="Department", bg=bg_color).grid(row=2, column=0, padx=10, pady=5, sticky="e")
tk.Label(input_frame, text="Salary", bg=bg_color).grid(row=3, column=0, padx=10, pady=5, sticky="e")
tk.Label(input_frame, text="Phone Number", bg=bg_color).grid(row=4, column=0, padx=10, pady=5, sticky="e")
tk.Label(input_frame, text="Gender", bg=bg_color).grid(row=5, column=0, padx=10, pady=5, sticky="e")
tk.Label(input_frame, text="Photo URL", bg=bg_color).grid(row=6, column=0, padx=10, pady=5, sticky="e")

name_entry = ttk.Entry(input_frame)
position_entry = ttk.Entry(input_frame)
department_entry = ttk.Entry(input_frame)
salary_entry = ttk.Entry(input_frame)
phone_entry = ttk.Entry(input_frame)
gender_var = tk.StringVar()
gender_frame = tk.Frame(input_frame, bg=bg_color)
gender_male = tk.Radiobutton(gender_frame, text="Male", variable=gender_var, value="Male", bg=bg_color)
gender_female = tk.Radiobutton(gender_frame, text="Female", variable=gender_var, value="Female", bg=bg_color)
gender_other = tk.Radiobutton(gender_frame, text="Other", variable=gender_var, value="Other", bg=bg_color)
photo_entry = ttk.Entry(input_frame)

name_entry.grid(row=0, column=1, padx=10, pady=5)
position_entry.grid(row=1, column=1, padx=10, pady=5)
department_entry.grid(row=2, column=1, padx=10, pady=5)
salary_entry.grid(row=3, column=1, padx=10, pady=5)
phone_entry.grid(row=4, column=1, padx=10, pady=5)
gender_frame.grid(row=5, column=1, padx=10, pady=5, sticky="w")
gender_male.pack(side=tk.LEFT)
gender_female.pack(side=tk.LEFT, padx=(10, 0))
gender_other.pack(side=tk.LEFT, padx=(10, 0))
photo_entry.grid(row=6, column=1, padx=10, pady=5)

add_button = tk.Button(input_frame, text="Add Employee", command=add_employee, bg=button_bg, fg=button_fg)
add_button.grid(row=7, column=0, columnspan=2, padx=10, pady=10, sticky="we")
add_button_hover_effects(add_button)

update_button = tk.Button(input_frame, text="Update Employee", command=update_employee, bg=button_bg, fg=button_fg)
update_button.grid(row=8, column=0, columnspan=2, padx=10, pady=10, sticky="we")
add_button_hover_effects(update_button)

delete_button = tk.Button(input_frame, text="Delete Employee", command=delete_employee, bg=button_bg, fg=button_fg)
delete_button.grid(row=9, column=0, columnspan=2, padx=10, pady=10, sticky="we")
add_button_hover_effects(delete_button)

view_button = tk.Button(input_frame, text="View Employees", command=view_employees, bg=button_bg, fg=button_fg)
view_button.grid(row=10, column=0, columnspan=2, padx=10, pady=10, sticky="we")
add_button_hover_effects(view_button)

# Clear Button
clear_button = tk.Button(input_frame, text="Clear", command=clear_entries, bg=button_bg, fg=button_fg)
clear_button.grid(row=11, column=0, columnspan=2, padx=10, pady=10, sticky="we")
add_button_hover_effects(clear_button)

# Search and Sort Frame
search_sort_frame = tk.Frame(app, padx=10, pady=10, bg=bg_color)
search_sort_frame.pack(fill=tk.X)

tk.Label(search_sort_frame, text="Search by Name", bg=bg_color).pack(side=tk.LEFT, padx=10)
search_entry = ttk.Entry(search_sort_frame)
search_entry.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
search_button = ttk.Button(search_sort_frame, text="Search", command=search_employees)
search_button.pack(side=tk.LEFT, padx=10)
add_button_hover_effects(search_button)

# Sort dropdown
sort_by_var = tk.StringVar()
sort_by_dropdown = ttk.Combobox(search_sort_frame, textvariable=sort_by_var, values=["Name", "Salary"], state="readonly")
sort_by_dropdown.set("Sort By")
sort_by_dropdown.pack(side=tk.LEFT, padx=10)

def sort_employees():
    order_by = sort_by_var.get().lower()
    if order_by == "name":
        view_employees(order_by="name")
    elif order_by == "salary":
        view_employees(order_by="salary")

sort_button = ttk.Button(search_sort_frame, text="Sort", command=sort_employees)
sort_button.pack(side=tk.LEFT, padx=10)
add_button_hover_effects(sort_button)

# Employee List
list_frame = tk.Frame(app, padx=10, pady=10, bg=bg_color)
list_frame.pack(fill=tk.BOTH, expand=True)

columns = ("ID", "Name", "Position", "Department", "Salary", "Phone", "Gender", "Photo")
employee_tree = ttk.Treeview(list_frame, columns=columns, show="headings")

for col in columns:
    employee_tree.heading(col, text=col)
    employee_tree.column(col, minwidth=0, width=100)

employee_tree.pack(fill=tk.BOTH, expand=True)

# Image Display
photo_label = tk.Label(list_frame, bg=bg_color)
photo_label.pack(pady=10)

# Function to display image and populate entry fields when an employee is selected
def show_employee_image(event):
    selected_item = employee_tree.selection()
    if not selected_item:
        return
    
    employee_data = employee_tree.item(selected_item[0])['values']
    name_entry.delete(0, tk.END)
    name_entry.insert(0, employee_data[1])
    position_entry.delete(0, tk.END)
    position_entry.insert(0, employee_data[2])
    department_entry.delete(0, tk.END)
    department_entry.insert(0, employee_data[3])
    salary_entry.delete(0, tk.END)
    salary_entry.insert(0, str(employee_data[4]))
    phone_entry.delete(0, tk.END)
    phone_entry.insert(0, employee_data[5])
    gender_var.set(employee_data[6])
    photo_entry.delete(0, tk.END)
    photo_entry.insert(0, employee_data[7])

    employee_photo_url = employee_data[7]

    try:
        response = requests.get(employee_photo_url)
        response.raise_for_status()
        image_data = Image.open(BytesIO(response.content))
        image_data.thumbnail((200, 200))
        photo = ImageTk.PhotoImage(image_data)
        photo_label.config(image=photo)
        photo_label.image = photo
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Failed to load image: {e}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Bind the show_employee_image function to the Treeview selection event
employee_tree.bind("<<TreeviewSelect>>", show_employee_image)

# Initialize with employee data
view_employees()


app.mainloop()


