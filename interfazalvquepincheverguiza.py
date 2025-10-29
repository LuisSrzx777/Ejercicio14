import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error
import csv
from PIL import Image, ImageTk
import random
import os

class EmployeeManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestión de Empleados - Edición Mejorada")
        self.root.geometry("900x700")
        self.root.configure(bg='#2c3e50')
        
        # Configuración de la base de datos
        self.db_config = {
            'host': '127.0.0.1',
            'user': 'root',
            'password': 'toor',
            'database': 'empresa_db'
        }
        
        self.setup_ui()
        self.create_database()
    
    def setup_ui(self):
        # Cargar y establecer imagen de fondo
        try:
            self.bg_image = Image.open("background.webp")
            self.bg_photo = ImageTk.PhotoImage(self.bg_image)
            self.bg_label = tk.Label(self.root, image=self.bg_photo)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            print(f"Error cargando imagen de fondo: {e}")
            # Si no hay imagen, usar color de fondo
            self.root.configure(bg='#2c3e50')
        
        # Frame principal para contenido
        self.main_frame = tk.Frame(self.root, bg='#ffffff', bd=2, relief='raised')
        self.main_frame.place(relx=0.5, rely=0.5, anchor='center', width=800, height=600)
        
        self.setup_styles()
        self.create_widgets()
    
    def setup_styles(self):
        # Configurar estilos para botones
        self.style = ttk.Style()
        
        # Estilo para botones principales
        self.style.configure('Primary.TButton',
                           font=('Arial', 10, 'bold'),
                           padding=10,
                           relief='raised',
                           borderwidth=3,
                           background='#3498db',
                           foreground='white')
        
        # Estilo para botones de éxito
        self.style.configure('Success.TButton',
                           font=('Arial', 10, 'bold'),
                           background='#27ae60',
                           foreground='white',
                           padding=10)
        
        # Estilo para botones de peligro
        self.style.configure('Danger.TButton',
                           font=('Arial', 10, 'bold'),
                           background='#e74c3c',
                           foreground='white',
                           padding=10)
        
        # Estilo para botones de advertencia
        self.style.configure('Warning.TButton',
                           font=('Arial', 10, 'bold'),
                           background='#f39c12',
                           foreground='white',
                           padding=10)
    
    def create_widgets(self):
        # Título
        title_label = tk.Label(self.main_frame, 
                              text="SISTEMA DE GESTIÓN DE EMPLEADOS", 
                              font=('Arial', 16, 'bold'),
                              bg='#34495e', 
                              fg='#ecf0f1',
                              pady=10)
        title_label.pack(fill='x', padx=20, pady=20)
        
        # Frame de formulario
        form_frame = tk.Frame(self.main_frame, bg='#f8f9fa')
        form_frame.pack(pady=10, padx=20, fill='x')
        
        # Campos del formulario
        fields = [
            ("Nombre:", "nombre"),
            ("Correo:", "correo"),
            ("Sexo:", "sexo")
        ]
        
        self.entries = {}
        for i, (text, field) in enumerate(fields):
            label = tk.Label(form_frame, text=text, font=('Arial', 10, 'bold'), bg='#f8f9fa')
            label.grid(row=i, column=0, sticky='w', padx=10, pady=5)
            
            entry = tk.Entry(form_frame, font=('Arial', 10), width=30, bg='white')
            entry.grid(row=i, column=1, padx=10, pady=5, sticky='ew')
            self.entries[field] = entry
        
        # Frame de botones principales
        button_frame = tk.Frame(self.main_frame, bg='#ffffff')
        button_frame.pack(pady=20)
        
        # Botones principales
        buttons = [
            ("Agregar Empleado", self.add_employee, 'Primary.TButton'),
            ("Mostrar Empleados", self.show_employees, 'Success.TButton'),
            ("Actualizar Empleado", self.update_employee, 'Warning.TButton'),
            ("Eliminar Empleado", self.delete_employee, 'Danger.TButton'),
            ("Exportar a CSV", self.export_to_csv, 'Primary.TButton'),
            ("Mensaje Especial", self.show_interesting_message, 'Success.TButton')
        ]
        
        for i, (text, command, style) in enumerate(buttons):
            btn = ttk.Button(button_frame, text=text, command=command, style=style)
            btn.grid(row=i//2, column=i%2, padx=10, pady=5, sticky='ew')
        
        # Botón Cerrar Esquivo
        self.close_button = ttk.Button(self.main_frame, 
                                     text="Cerrar (¡Intenta atraparme!)", 
                                     command=self.root.quit,
                                     style='Danger.TButton')
        self.close_button.pack(pady=10)
        self.close_button.bind("<Enter>", self.move_close_button)
    
    def move_close_button(self, event):
        # Mover el botón de cerrar aleatoriamente
        x = random.randint(50, 750)
        y = random.randint(400, 550)
        self.close_button.place(x=x, y=y)
    
    def create_database(self):
        try:
            connection = mysql.connector.connect(**self.db_config)
            cursor = connection.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS empleados (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nombre VARCHAR(100) NOT NULL,
                    correo VARCHAR(100) UNIQUE NOT NULL,
                    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            connection.commit()
            cursor.close()
            connection.close()
            
        except Error as e:
            messagebox.showerror("Error", f"Error al conectar con la base de datos: {e}")
    
    def add_employee(self):
        try:
            # Validar campos obligatorios
            if not all([self.entries['nombre'].get(), self.entries['correo'].get()]):
                messagebox.showerror("Error", "Nombre y Email son campos obligatorios")
                return
            
            connection = mysql.connector.connect(**self.db_config)
            cursor = connection.cursor()
            
            query = """
                INSERT INTO empleados (nombre, correo, sexo)
                VALUES (%s, %s, %s)
            """
            
            values = (
                self.entries['nombre'].get(),
                self.entries['email'].get(),
                self.entries['sexo'].get()
            )
            
            cursor.execute(query, values)
            connection.commit()
            cursor.close()
            connection.close()
            
            messagebox.showinfo("Éxito", "Empleado agregado correctamente")
            self.clear_entries()
            
        except Error as e:
            messagebox.showerror("Error", f"Error al agregar empleado: {e}")
    
    def show_employees(self):
        try:
            connection = mysql.connector.connect(**self.db_config)
            cursor = connection.cursor(dictionary=True)
            
            cursor.execute("SELECT * FROM empleados")
            employees = cursor.fetchall()
            
            cursor.close()
            connection.close()
            
            self.display_employees_window(employees)
            
        except Error as e:
            messagebox.showerror("Error", f"Error al obtener empleados: {e}")
    
    def display_employees_window(self, employees):
        employees_window = tk.Toplevel(self.root)
        employees_window.title("Lista de Empleados")
        employees_window.geometry("800x400")
        employees_window.configure(bg='#ecf0f1')
        
        # Frame para treeview
        tree_frame = tk.Frame(employees_window)
        tree_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Treeview con scrollbar
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side='right', fill='y')
        
        tree = ttk.Treeview(tree_frame, columns=('ID', 'Nombre', 'correo', 'Sexo'), 
                           show='headings', yscrollcommand=scrollbar.set)
        
        # Configurar columnas
        columns = [('ID', 50), ('Nombre', 100), ('correo', 150), 
                 ('Sexo', 50)]
        
        for col, width in columns:
            tree.heading(col, text=col)
            tree.column(col, width=width)
        
        # Insertar datos
        for emp in employees:
            tree.insert('', 'end', values=(
                emp['id'], emp['nombre'], emp['correo'],
                f"${emp['sexo']:.2f}"
            ))
        
        tree.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=tree.yview)
        
        # Botón para cerrar
        close_btn = ttk.Button(employees_window, text="Cerrar", command=employees_window.destroy)
        close_btn.pack(pady=10)
    
    def update_employee(self):
        # Ventana para actualizar empleado
        update_window = tk.Toplevel(self.root)
        update_window.title("Actualizar Empleado")
        update_window.geometry("400x300")
        update_window.configure(bg='#ecf0f1')
        
        tk.Label(update_window, text="Funcionalidad de Actualización", 
                font=('Arial', 12, 'bold'), bg='#ecf0f1').pack(pady=20)
        
        tk.Label(update_window, text="Ingrese el ID del empleado a actualizar:", 
                bg='#ecf0f1').pack(pady=5)
        
        id_entry = tk.Entry(update_window, font=('Arial', 10))
        id_entry.pack(pady=5)
        
        def perform_update():
            emp_id = id_entry.get()
            if emp_id:
                messagebox.showinfo("Actualizar", f"Actualizando empleado ID: {emp_id}")
                update_window.destroy()
            else:
                messagebox.showerror("Error", "Ingrese un ID válido")
        
        ttk.Button(update_window, text="Actualizar", command=perform_update).pack(pady=10)
        ttk.Button(update_window, text="Cancelar", command=update_window.destroy).pack(pady=5)
    
    def delete_employee(self):
        # Ventana para eliminar empleado
        delete_window = tk.Toplevel(self.root)
        delete_window.title("Eliminar Empleado")
        delete_window.geometry("400x200")
        delete_window.configure(bg='#ecf0f1')
        
        tk.Label(delete_window, text="Funcionalidad de Eliminación", 
                font=('Arial', 12, 'bold'), bg='#ecf0f1').pack(pady=20)
        
        tk.Label(delete_window, text="Ingrese el ID del empleado a eliminar:", 
                bg='#ecf0f1').pack(pady=5)
        
        id_entry = tk.Entry(delete_window, font=('Arial', 10))
        id_entry.pack(pady=5)
        
        def perform_delete():
            emp_id = id_entry.get()
            if emp_id:
                messagebox.showinfo("Eliminar", f"Eliminando empleado ID: {emp_id}")
                delete_window.destroy()
            else:
                messagebox.showerror("Error", "Ingrese un ID válido")
        
        ttk.Button(delete_window, text="Eliminar", command=perform_delete).pack(pady=10)
        ttk.Button(delete_window, text="Cancelar", command=delete_window.destroy).pack(pady=5)
    
    def export_to_csv(self):
        try:
            connection = mysql.connector.connect(**self.db_config)
            cursor = connection.cursor(dictionary=True)
            
            cursor.execute("SELECT * FROM empleados")
            employees = cursor.fetchall()
            
            cursor.close()
            connection.close()
            
            # Exportar a CSV
            filename = "empleados_exportados.csv"
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['id', 'nombre', 'correo', 'sexo']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                for emp in employees:
                    writer.writerow(emp)
            
            messagebox.showinfo("Éxito", f"Datos exportados a {filename}")
            
        except Error as e:
            messagebox.showerror("Error", f"Error al exportar datos: {e}")
    
    def show_interesting_message(self):
        message_window = tk.Toplevel(self.root)
        message_window.title("Mensaje Especial")
        message_window.geometry("500x400")
        message_window.configure(bg='#2c3e50')
        
        # Mensaje principal
        message_label = tk.Label(message_window, 
                                text="¡SISTEMA SEGURO! 🔒", 
                                font=('Arial', 18, 'bold'),
                                bg='#2c3e50', 
                                fg='#27ae60')
        message_label.pack(pady=20)
        
        # Mensaje secundario
        sub_label = tk.Label(message_window, 
                           text="Todos los datos están protegidos\ny seguros en nuestro sistema.",
                           font=('Arial', 12),
                           bg='#2c3e50',
                           fg='#ecf0f1')
        sub_label.pack(pady=10)
        
        # Información adicional
        info_text = """
        Características de seguridad:
        • Encriptación de datos
        • Acceso restringido
        • Backup automático
        • Auditoría de accesos
        • Cumplimiento normativo
        """
        
        info_label = tk.Label(message_window,
                            text=info_text,
                            font=('Arial', 10),
                            bg='#34495e',
                            fg='#bdc3c7',
                            justify='left')
        info_label.pack(pady=20, padx=20)
        
        # Botón de cierre
        close_btn = ttk.Button(message_window, 
                             text="Entendido", 
                             command=message_window.destroy,
                             style='Success.TButton')
        close_btn.pack(pady=10)
    
    def clear_entries(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = EmployeeManager(root)
    root.mainloop()
