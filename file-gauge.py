import customtkinter as ctk
from tkinter import filedialog
from pathlib import Path
import shutil


FILE_CATEGORIES = {
    "Images": {
        ".jpg", ".jpeg", ".png", ".gif",
        ".webp", ".bmp", ".svg", ".ico"
    },

    "Videos": {
        ".mp4", ".mkv", ".avi",
        ".mov", ".webm", ".flv"
    },

    "Music": {
        ".mp3", ".wav", ".flac",
        ".aac", ".ogg", ".m4a"
    },

    "Documents": {
        ".pdf", ".doc", ".docx",
        ".txt", ".rtf", ".odt"
    },

    "Spreadsheets": {
        ".xls", ".xlsx", ".csv"
    },

    "Presentations": {
        ".ppt", ".pptx", ".odp"
    },

    "Archives": {
        ".zip", ".rar", ".7z",
        ".tar", ".gz"
    },

    "Programs": {
        ".exe", ".msi", ".apk"
    },

    "Code": {
        ".py", ".js", ".ts",
        ".html", ".css", ".cpp",
        ".c", ".java", ".rs",
        ".go", ".json"
    }
}


class FileOrganizerApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("File Organizer")
        self.geometry("800x550")
        self.minsize(700, 500)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.create_ui()

    def create_ui(self):

        title = ctk.CTkLabel(
            self,
            text="File Organizer",
            font=ctk.CTkFont(
                size=32,
                weight="bold"
            )
        )

        title.pack(pady=(35, 5))

        subtitle = ctk.CTkLabel(
            self,
            text="Automatically organize your files into categories",
            font=ctk.CTkFont(size=14)
        )

        subtitle.pack(pady=(0, 30))

        # Folder frame
        folder_frame = ctk.CTkFrame(self)

        folder_frame.pack(
            padx=40,
            fill="x"
        )

        folder_label = ctk.CTkLabel(
            folder_frame,
            text="Folder to organize",
            font=ctk.CTkFont(
                size=16,
                weight="bold"
            )
        )

        folder_label.pack(
            anchor="w",
            padx=20,
            pady=(15, 8)
        )

        self.folder_entry = ctk.CTkEntry(
            folder_frame,
            placeholder_text="Choose a folder..."
        )

        self.folder_entry.pack(
            side="left",
            padx=(20, 10),
            pady=(0, 20),
            fill="x",
            expand=True
        )

        browse_button = ctk.CTkButton(
            folder_frame,
            text="Browse",
            width=100,
            command=self.choose_folder
        )

        browse_button.pack(
            side="right",
            padx=(0, 20),
            pady=(0, 20)
        )

        # Organize button
        organize_button = ctk.CTkButton(
            self,
            text="ORGANIZE FILES",
            height=50,
            font=ctk.CTkFont(
                size=16,
                weight="bold"
            ),
            command=self.organize
        )

        organize_button.pack(
            padx=40,
            pady=30,
            fill="x"
        )

        # Status
        self.status = ctk.CTkLabel(
            self,
            text="Ready"
        )

        self.status.pack(pady=10)

        # Log
        self.log = ctk.CTkTextbox(
            self,
            height=180
        )

        self.log.pack(
            padx=40,
            pady=(5, 30),
            fill="both",
            expand=True
        )

    def choose_folder(self):

        folder = filedialog.askdirectory()

        if folder:

            self.folder_entry.delete(
                0,
                "end"
            )

            self.folder_entry.insert(
                0,
                folder
            )

            self.status.configure(
                text=f"Selected: {folder}"
            )

    def get_category(self, extension):

        extension = extension.lower()

        for category, extensions in FILE_CATEGORIES.items():

            if extension in extensions:
                return category

        return "Other"

    def organize(self):

        folder = self.folder_entry.get()

        if not folder:

            self.status.configure(
                text="Please select a folder first."
            )

            return

        folder_path = Path(folder)

        if not folder_path.exists():

            self.status.configure(
                text="Folder does not exist."
            )

            return

        files = [
            file
            for file in folder_path.iterdir()
            if file.is_file()
        ]

        if not files:

            self.status.configure(
                text="No files found."
            )

            return

        moved = 0

        self.log.delete(
            "1.0",
            "end"
        )

        for file in files:

            category = self.get_category(
                file.suffix
            )

            category_folder = (
                folder_path / category
            )

            category_folder.mkdir(
                exist_ok=True
            )

            destination = (
                category_folder / file.name
            )

            # Prevent overwriting
            if destination.exists():

                counter = 1

                while True:

                    new_name = (
                        f"{file.stem}_{counter}"
                        f"{file.suffix}"
                    )

                    destination = (
                        category_folder / new_name
                    )

                    if not destination.exists():
                        break

                    counter += 1

            try:

                shutil.move(
                    str(file),
                    str(destination)
                )

                self.log.insert(
                    "end",
                    f"✓ {file.name} → {category}/\n"
                )

                moved += 1

            except Exception as error:

                self.log.insert(
                    "end",
                    f"✗ {file.name}: {error}\n"
                )

        self.status.configure(
            text=f"Done! Organized {moved} files."
        )


if __name__ == "__main__":

    app = FileOrganizerApp()

    app.mainloop()