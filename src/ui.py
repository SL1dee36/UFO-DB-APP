from customtkinter import *
from tkinter import messagebox, TclError
import time
import os
from .dbBuilder.pyufodb import Relative_DB
from .dbBuilder.otherFunc import githubLink, AuthorLink,gitlink
from .dbBuilder.dbEditor import DBEditor
from .aiBridge import create_ai_frame, AI
import shutil
from tkinter import filedialog

class DatabaseApp(CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Database Interface")
        self.geometry("900x600")
        self.saves_dir = "src/saves"
        self.gradient_colors = [(78, 84, 200), (143, 148, 251)]
        self.current_color_index = 0
        self.create_db_frame = None 

        self.load_frame()

    def animate_gradient_button(self, button, step=0):
        if step < 100:
            r1, g1, b1 = self.gradient_colors[self.current_color_index]
            r2, g2, b2 = self.gradient_colors[(self.current_color_index + 1) % len(self.gradient_colors)]

            r = int(r1 + (r2 - r1) * (step / 100))
            g = int(g1 + (g2 - g1) * (step / 100))
            b = int(b1 + (b2 - b1) * (step / 100))
            color = f"#{r:02x}{g:02x}{b:02x}"
            button.configure(fg_color=color)

            self.after_id = self.after(20, self.animate_gradient_button, button, step + 1)
        else:
            self.current_color_index = (self.current_color_index + 1) % len(self.gradient_colors)
            self.after_id = self.after(200, self.animate_gradient_button, button)

    def init_create_db_frame(self):
        CTkLabel(self.create_db_frame, text="Название базы данных:").pack(padx=5, pady=(5, 0))
        self.db_name_entry = CTkEntry(self.create_db_frame)
        self.db_name_entry.pack(padx=5, pady=5)

        CTkLabel(self.create_db_frame, text="Количество строк:").pack(padx=5, pady=(5, 0))
        self.row_scale = CTkSlider(self.create_db_frame, from_=1, to=20, number_of_steps=19,
                                    command=self.update_row_count)
        self.row_scale.set(1) 
        self.row_scale.pack(padx=5, pady=5)

        self.row_count_label = CTkLabel(self.create_db_frame, text="1")  
        self.row_count_label.pack(padx=5, pady=(0, 10))

        CTkLabel(self.create_db_frame, text="Количество столбцов:").pack(padx=5, pady=(5, 0))
        self.column_scale = CTkSlider(self.create_db_frame, from_=3, to=20, number_of_steps=19,
                                    command=self.update_column_count)
        self.column_scale.set(1)  
        self.column_scale.pack(padx=5, pady=5)

        self.column_count_label = CTkLabel(self.create_db_frame, text="3")
        self.column_count_label.pack(padx=5, pady=(0, 10))

        self.create_button = CTkButton(self.create_db_frame,text="create",command=lambda: self.create_new_db())
        self.create_button.pack()

    def update_row_count(self, value):
        self.row_count_label.configure(text=str(int(float(value))))

    def update_column_count(self, value):
        self.column_count_label.configure(text=str(int(float(value))))

    def create_new_database(self):
        self.create_db_frame.pack(padx=5, pady=5, fill=BOTH, expand=True)
        self.init_create_db_frame()
        self.after_cancel(self.after_id)

    def create_new_db(self):
        db_name = self.db_name_entry.get().strip()
        if not db_name:
            messagebox.showerror("Ошибка", "Пожалуйста, введите название базы данных.")
            return
        
        row_count = self.row_scale.get()
        column_count = int(self.column_scale.get())
        
        # Генерация имен столбцов
        column_names = self.generate_column_names(column_count)

        # Создание файла базы данных
        if not os.path.exists(self.saves_dir):
            os.makedirs(self.saves_dir)
        self.db_file = os.path.join(self.saves_dir, f"{db_name}.ufo")
        
        if os.path.exists(self.db_file):
            messagebox.showinfo("База данных", "Файл базы данных уже существует.")
        else:
            self.db = Relative_DB()
            self.db.create_table("sightings", column_names)
            self.db.save_to_file(self.db_file)
            messagebox.showinfo("База данных", "Новая база данных создана успешно.")
            self.refresh_file_list()

    def generate_column_names(self, count):
        """Генерация имен столбцов от 'a' до 'zzz'."""
        if count < 3 or count > 78:
            return []
        
        names = []
        for i in range(count):
            name = ""
            num = i
            while num >= 0:
                name = chr(num % 26 + ord('a')) + name
                num = num // 26 - 1 
            names.append(name)
        
        return names

    def clear_window(self):
        self.resizable(True, True)
        self.start_frame.pack_forget()

    def load_frame(self):
        self.resizable(False, False)
        self.start_frame = CTkFrame(self)
        self.start_frame.pack(padx=5, pady=5, fill=BOTH, expand=True)
        self.file_manager = CTkFrame(self.start_frame, width=self.winfo_width() // 1.7)
        self.file_manager.pack(padx=5, pady=5, side=LEFT, fill=Y)
        self.file_toolbar_frame = CTkFrame(self.file_manager, height=50, width=self.winfo_width() // 1.7)
        self.file_toolbar_frame.pack(padx=5, pady=5, fill=X)
        self.interface_menu = CTkFrame(self.start_frame)
        self.interface_menu.pack(padx=(0, 5), pady=5, side=LEFT, fill=BOTH, expand=True)
        self.interface_menu_frame = CTkFrame(self.interface_menu, height=50)
        self.interface_menu_frame.pack(side=TOP, padx=5, pady=5, fill=X)
        self.interface_bottom_frame = CTkFrame(self.interface_menu, height=50)
        self.interface_bottom_frame.pack(side=BOTTOM, padx=5, pady=5, fill=X)
        self.load_im()
        self.load_file_manager()

    def load_im(self):
        self.create_btn = CTkButton(self.interface_menu_frame, text="Create new Table (.ufo)", width=160, height=40,
                  command=lambda: self.create_new_database())
        self.create_btn.pack(side=LEFT, padx=5, pady=5)
        CTkButton(self.interface_menu_frame, text="Load Table (.ufo)", width=160, height=40,
                  command=self.load_file_dialog).pack(side=LEFT, padx=(0, 5), pady=5)
        
        self.create_db_frame = CTkFrame(self.interface_menu)

        self.bbar = CTkFrame(self.interface_bottom_frame, corner_radius=0)
        self.bbar.pack(side=BOTTOM)
        CTkButton(self.bbar, width=100, text="Authors", command=githubLink).pack(fill=X, expand=True, side=LEFT, padx=(9, 0))
        CTkButton(self.bbar, width=100, text="GitHub", command=AuthorLink).pack(fill=X, expand=True, side=LEFT, padx=5)
        CTkButton(self.bbar, width=100, text="V2.1.0", command=gitlink).pack(fill=X, expand=True, side=LEFT, padx=(0, 9))
        #CTkButton(self.bbar, width=100, text="AI", command=lambda: AI()).pack(fill=X, expand=True, side=LEFT, padx=(0, 9))

        self.animate_gradient_button(self.create_btn)

    def load_file_manager(self):
        CTkLabel(self.file_toolbar_frame, text="Saved Databases:", width=self.winfo_width() // 1.7).pack(padx=5, pady=(5, 0))
        self.file_list_frame = CTkScrollableFrame(self.file_manager)
        self.file_list_frame.pack(padx=5, pady=5, fill=BOTH, expand=True)

        if not os.path.exists(self.saves_dir):
            os.makedirs(self.saves_dir)

        self.refresh_file_list()

    def refresh_file_list(self):
        for widget in self.file_list_frame.winfo_children():
            widget.destroy()

        if not os.path.exists(self.saves_dir):
            os.makedirs(self.saves_dir)

        for filename in os.listdir(self.saves_dir):
            if filename.endswith(".ufo"):
                filepath = os.path.join(self.saves_dir, filename)
                timestamp = os.path.getmtime(filepath)
                formatted_time = time.strftime("%Y-%m-%d %H:%M", time.localtime(timestamp))

                file_frame = CTkFrame(self.file_list_frame, height=30)
                file_frame.pack(fill=X, padx=2, pady=2)

                file_label = CTkLabel(file_frame, text=filename[:-4], anchor="w")
                file_label.pack(side=LEFT, fill=X, expand=True, padx=5)
                CTkLabel(file_frame, text=formatted_time, width=100, anchor="e").pack(side=RIGHT, padx=5)

                file_label.bind("<Button-1>", lambda event, fp=filepath: self.open_db_editor(fp))
                file_label.bind("<Enter>", lambda event: file_label.configure(cursor="hand2"))
                file_label.bind("<Leave>", lambda event: file_label.configure(cursor=""))
                
                try:
                    delete_button = CTkButton(file_frame, text="X", width=25, height=25,
                                                command=lambda fp=filepath: self.delete_database(fp))
                except TclError:
                    delete_button = CTkButton(file_frame, text="X", width=25, height=25,
                                                command=lambda fp=filepath: self.delete_database(fp))
                delete_button.pack(side=RIGHT, padx=(0, 5))

    def delete_database(self, filepath):
        if messagebox.askyesno("Подтверждение", f"Вы уверены, что хотите удалить базу данных {os.path.basename(filepath)}?"):
            try:
                os.remove(filepath)
                messagebox.showinfo("Успешно", "База данных удалена.")
                self.refresh_file_list() 
            except OSError as e:
                messagebox.showerror("Ошибка", f"Не удалось удалить базу данных: {e}")            

    def load_file_dialog(self):
        file_path = filedialog.askopenfilename(title="Select a UFO file", filetypes=[("UFO Files", "*.ufo")])
        if file_path:
            self.copy_file_to_saves(file_path)
            self.refresh_file_list()

    def copy_file_to_saves(self, file_path):
        filename = os.path.basename(file_path)
        dest_path = os.path.join(self.saves_dir, filename)
        try:
            shutil.copy(file_path, dest_path)
            messagebox.showinfo("Файл загружен", f"Файл {filename} успешно загружен.")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось скопировать файл: {e}")

    
    def open_db_editor(self, db_file):
        DBEditor(self, db_file)