import tkinter as tk
import customtkinter as ctk
from PIL import Image
from .account import UserProfileApp
from .ui import DatabaseApp 
from .dbBuilder.otherFunc import openPrivacyPolicy, openTermsofUse

class StartWindow(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.title("UFO DataBase")
        self.geometry("800x600")

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        title_label = ctk.CTkLabel(self, text="UFO DATABASE", font=("Helvetica", 40, "bold"), text_color="lightblue")
        title_label.pack(pady=(40, 20))  

        self.version_label = ctk.CTkLabel(self, text=" Версия 2.0.1 ", font=("Arial", 10), fg_color="#2b2b2b")
        self.version_label.place(relx=0.0, rely=1.0, anchor="sw", x=20, y=-20) 

        frame = ctk.CTkFrame(self, width=400, height=300, corner_radius=10)  
        frame.pack(pady=(50, 20))  

        try:
            image = ctk.CTkImage(light_image=Image.open("img/ufo.jpg"),
                                 dark_image=Image.open("img/ufo.jpg"),  
                                 size=(200, 200))
        except Exception as e:
            print(f"Error loading image: {e}")
            image = None

        if image:
            image_label = ctk.CTkLabel(frame, image=image, text="")
            image_label.pack(pady=(10, 10))

        label = ctk.CTkLabel(frame, text="\nКол-во созданых DB:\n3\n", font=("Helvetica", 18), text_color="white")
        label.pack(expand=True) 

        start_button = ctk.CTkButton(self, text="НАЧАТЬ", width=200, corner_radius=20, font=("Helvetica", 16), 
                                      hover_color="lightblue", command=self.open_database_app)
        start_button.pack(pady=(20, 0), padx=20)  

        link_frame = ctk.CTkFrame(self, corner_radius=10)
        link_frame.pack(side=tk.BOTTOM, anchor=tk.S, padx=20, pady=(10, 20))
        link_frame.configure(fg_color=frame.cget('fg_color')) 

        link1 = ctk.CTkLabel(link_frame, text="Политика конфиденциальности", text_color="white", 
                              cursor="hand2", font=("Helvetica", 10))
        link1.pack(side=tk.LEFT, padx=10)
        link1.bind("<Button-1>", lambda e: openPrivacyPolicy())  

        link2 = ctk.CTkLabel(link_frame, text="Условия использования", text_color="white", 
                              cursor="hand2", font=("Helvetica", 10))
        link2.pack(side=tk.LEFT, padx=10)
        link2.bind("<Button-1>", lambda e: openTermsofUse())  

        account_frame = ctk.CTkFrame(self, width=50, height=50, corner_radius=70, border_width=0)
        account_frame.place(relx=0.92, rely=0.05, anchor=tk.CENTER)

        account_canvas = tk.Canvas(account_frame, width=40, height=40, bg="#2b2b2b", highlightthickness=0)
        account_canvas.place(x=5, y=5)

        account_canvas.create_oval(2, 2, 38, 38, fill="gray", outline="")
        account_canvas.create_text(20, 20, text="👤", font=("Arial", 18), fill="white")

        account_canvas.bind("<Button-1>", lambda e: self.openAccount())

    def openAccount(self):
        self.profile_window = UserProfileApp(self) 
        self.profile_window.grab_set()

    def open_database_app(self):
        database_app = DatabaseApp(self)
        self.withdraw()

if __name__ == "__main__":
    start_window = StartWindow()
    start_window.mainloop()