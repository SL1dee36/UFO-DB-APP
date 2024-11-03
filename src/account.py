import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

class UserProfileApp(ctk.CTkToplevel):
    def __init__(self, master): 
        super().__init__(master)
        self.title("User Profile")
        self.geometry("700x700")

        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        self.profile_frame = ctk.CTkFrame(self)
        self.profile_frame.pack(fill='both', expand=True, padx=20, pady=10)

        self.profile_frame.rowconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)
        self.profile_frame.columnconfigure(0, weight=1)
        self.profile_frame.columnconfigure(1, weight=1)

        self.title_label = ctk.CTkLabel(self.profile_frame, text="Account", font=("Arial", 24, "bold"))
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(10, 10), sticky="n")

        self.avatar_frame = ctk.CTkFrame(self.profile_frame)
        self.avatar_frame.grid(row=1, column=0, columnspan=2, pady=10, padx=10, sticky="nsew")
        self.avatar_frame.columnconfigure(0, weight=1)

        self.avatar_display = ctk.CTkLabel(self.avatar_frame, text="No Avatar", width=150, height=150, corner_radius=10, fg_color=("gray", "gray10"))
        self.avatar_display.grid(row=0, column=0, pady=10, padx=10, sticky="n")

        self.upload_button = ctk.CTkButton(self.avatar_frame, text="Upload Avatar", command=self.upload_avatar, width=120)
        self.upload_button.grid(row=1, column=0, pady=10, sticky="n")

        self.nick_label = ctk.CTkLabel(self.profile_frame, text="Nickname:", font=("Arial", 18))
        self.nick_label.grid(row=2, column=0, columnspan=2, pady=10, padx=10, sticky="w")

        nick_frame = ctk.CTkFrame(self.profile_frame, height=50)
        nick_frame.grid(row=3, column=0, columnspan=2, pady=10, padx=10, sticky="ew")
        self.nick_entry = ctk.CTkEntry(nick_frame, font=("Arial", 16), width=300)
        self.nick_entry.pack(fill="both", expand=True)

        self.stats_label = ctk.CTkLabel(self.profile_frame, text="Statistics:", font=("Arial", 18, "bold"))
        self.stats_label.grid(row=4, column=0, columnspan=2, pady=10, padx=10, sticky="w")

        self.stats_display = ctk.CTkTextbox(self.profile_frame, wrap="word", state="disabled", width=200, font=("Arial", 14))
        self.stats_display.grid(row=5, column=0, columnspan=2, pady=10, padx=10, sticky="nsew")
        self.stats_display.insert("0.0", "No statistics available.")

        self.theme_button = ctk.CTkButton(self.profile_frame, text="Switch to Light Theme", command=self.toggle_theme, width=150)
        self.theme_button.grid(row=6, column=0, columnspan=2, pady=(20, 10), sticky="s")

        self.dark_theme = True

    def upload_avatar(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            try:
                img = Image.open(file_path)
                img = img.resize((150, 150), Image.ANTIALIAS)
                self.avatar_image = ImageTk.PhotoImage(img)
                self.avatar_display.configure(image=self.avatar_image, text="")
            except Exception as e:
                messagebox.showerror("Error", f"Could not load image: {e}")

    def toggle_theme(self):
        if self.dark_theme:
            ctk.set_appearance_mode("Light")
            self.dark_theme = False
            self.theme_button.configure(text="Switch to Dark Theme")
        else:
            ctk.set_appearance_mode("Dark")
            self.dark_theme = True
            self.theme_button.configure(text="Switch to Light Theme")

if __name__ == "__main__":
    root = ctk.CTk()
    app = UserProfileApp(root)
    root.mainloop()