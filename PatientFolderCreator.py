import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path

class PatientFolderCreatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Patient Folder Creator")
        self.root.resizable(False, False)
        self.root.geometry("700x500")

        #create notebook
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        #create two frames
        self.paste_frame = ttk.Frame(self.notebook)
        self.manual_frame = ttk.Frame(self.notebook)

        self.notebook.add(self.paste_frame, text="Paste from HopeRx")
        self.notebook.add(self.manual_frame, text="Manual Input")

        #Setup both tabs
        self.setup_paste_tab()
        self.setup_manual_tab()

    def setup_paste_tab(self):
        #Title
        title = ttk.LabelFrame(self.paste_frame, text="Paste all data from HopeRx:")
        title.pack(pady=10)

        #text widget for pasting
        self.paste_text = tk.Text(self.paste_frame, height=12, width=60, font=('Consolas', 10))
        self.paste_text.pack(padx=20, pady=10)
        self.paste_text.bind('<KeyRelease>', self.update_paste_preview)

        #preview section
        preview_label = tk.Label(self.paste_frame, text="Folder Preview:", font=('Arial', 10, 'bold'))
        preview_label.pack(pady=(10, 5))

        self.paste_preview = tk.Label(self.paste_frame, text="",
                                      font=('Consolas', 9),
                                      wraplength=600,
                                      fg='#2196F3',
                                      justify='left')
        self.paste_preview.pack(pady=5)

        #Generate button
        generate_btn = tk.Button(self.paste_frame, text="Generate Folder",
                                 command=self.generate_from_paste,
                                 bg='#4CAF50', fg='white',
                                 font=('Arial', 12, 'bold'),
                                 padx=30, pady=10)
        generate_btn.pack(pady=5)

    def setup_manual_tab(self):
        #Create form
        form_frame = tk.Frame(self.manual_frame)
        form_frame.pack(padx=20, pady=40)

        #Due Date
        tk.Label(form_frame, text="Due Date (mm/dd/yyyy):",
                 font=('Arial', 10)).grid(row=0, column=0, sticky='w', pady=10)
        self.due_date_entry = ttk.Entry(form_frame, font=('Arial', 10), width=30)
        self.due_date_entry.grid(row=0, column=1, padx=10, pady=10)
        self.due_date_entry.bind('<KeyRelease>', self.update_manual_preview)

        #Patient Name
        tk.Label(form_frame, text="Patient Name:",
                 font=('Arial', 10)).grid(row=1, column=0, sticky='w', pady=10)
        self.patient_name_entry = ttk.Entry(form_frame, font=('Arial', 10), width=30)
        self.patient_name_entry.grid(row=1, column=1, padx=10, pady=10)
        self.patient_name_entry.bind('<KeyRelease>', self.update_manual_preview)

        #Unique ID
        tk.Label(form_frame, text="Unique ID:",
                 font=('Arial', 10)).grid(row=2, column=0, sticky='w', pady=10)
        self.unique_id_entry = ttk.Entry(form_frame, font=('Arial', 10), width=30)
        self.unique_id_entry.grid(row=2, column=1, padx=10, pady=10)
        self.unique_id_entry.bind('<KeyRelease>', self.update_manual_preview)

        #Center Name
        tk.Label(form_frame, text="Center Name:",
                 font=('Arial', 10)).grid(row=3, column=0, sticky='w', pady=10)
        self.center_name_entry = ttk.Entry(form_frame, font=('Arial', 10), width=30)
        self.center_name_entry.grid(row=3, column=1, padx=10, pady=10)
        self.center_name_entry.bind('<KeyRelease>', self.update_manual_preview)

        #preview section
        preview_label = tk.Label(form_frame, text="Folder Preview:",
                                 font=('Arial', 10, 'bold'))
        preview_label.grid(row=4, column=0, columnspan=2, pady=(10,5))

        self.manual_preview = tk.Label(form_frame, text="",
                                       font=('Consolas', 9),
                                       wraplength=600,
                                       fg='#2196F3',
                                       justify='left')
        self.manual_preview.grid(row=5, column=0, columnspan=2, pady=5)

        generate_btn = tk.Button(form_frame, text="Generate Folder",
                                 command=self.generate_from_manual,
                                 bg='#4CAF50', fg='white',
                                 font=('Arial', 12, 'bold'),
                                 padx=30, pady=10)
        generate_btn.grid(row=6, column=0, columnspan=2, pady=20)

    def parse_pasted_data(self, text):
        """Parse pasted data in window and extract patient information"""
        #Strip empty lines
        lines = [line.strip() for line in text.strip().split('\n') if line.strip()]

        if len(lines) < 2:
            return None

        due_date = None
        center_name = None
        patient_line = None

        #find first date(due date)
        for line in lines:
            if '/' in line and not due_date:
                due_date = line.replace("/",".")
                break

        #last line is patient line
        if len(lines) > 0:
            patient_line = lines[-1].upper()

        #second to last is center
        if len(lines) > 1:
            potential_center = lines[-2]
            #Check if it's alphabetic
            if potential_center.replace(' ','').isalpha() or potential_center[0].isupper():
                center_name = potential_center
            else:
                # search backwards for alphabetic line
                for line in reversed(lines[:1]):
                    if line. replace(' ','').isalpha():
                        center_name = line
                        break

        if not center_name:
            center_name = "UNKNOWN"

        #parse patient line
        if patient_line:
            patient_parts = patient_line.strip().split()
            if len(patient_parts) >= 2:
                unique_id = patient_parts[-1]
                patient_name = " ".join(patient_parts[:-1])
            else:
                patient_name = patient_line.strip()
                unique_id = "UNKNOWN"

        else:
            patient_name = "UNKNOWN"
            unique_id = "UNKNOWN"

        return {
            'due_date': due_date,
            'patient_name': patient_name,
            'unique_id': unique_id,
            'center_name': center_name,
        }

    def update_paste_preview(self, event=None):
        """Update Preview based on pasted text"""
        text = self.paste_text.get("1.0", tk.END).strip()

        if not text:
            self.paste_preview.config(text="Preview will appear here...")
            return

        data = self.parse_pasted_data(text)

        if not data or not data['due_date']:
            self.paste_preview.config(text="Unable to parse pasted data. Check format.")
            return

        folder_name = f"{data['due_date']} {data['patient_name']} {data['unique_id']} {data['center_name']}"

        self.paste_preview.config(text=folder_name)

    def update_manual_preview(self, event=None):
        """Update Preview based on manual input"""

        due_date = self.due_date_entry.get().strip().replace('/','.')
        patient_name = self.patient_name_entry.get().strip().upper()
        unique_id = self.unique_id_entry.get().strip().upper()
        center_name = self.center_name_entry.get().strip().title()

        if not any([due_date, patient_name, unique_id, center_name]):
            self.manual_preview.config(text="Preview will appear here...")
            return

        # Use placeholders for empty fields
        due_date = due_date if due_date else "[Due Date]"
        patient_name = patient_name if patient_name else "[Patient Name]"
        unique_id = unique_id if unique_id else "[ID]"
        center_name = center_name if center_name else "[Center]"

        folder_name = f"{due_date} {patient_name} {unique_id} {center_name}"

        self.manual_preview.config(text=folder_name)

    def create_folder_structure(self, folder_name, unique_id):
        """Create folder structure"""

        desktop = Path.home() / "Desktop"
        main_folder_path = desktop / folder_name

        # create main folder and subfolders
        try:
            #create main folder
            main_folder_path.mkdir(exist_ok=True)

            #create subfolders
            subfolders = ["3D Viewer", "Design Screenshots", f"{unique_id} STL"]
            for subfolder in subfolders:
                subfolder_path = main_folder_path / subfolder
                subfolder_path.mkdir(exist_ok=True)

            return True, str(main_folder_path)
        except Exception as e:
            return False, str(e)

    def generate_from_paste(self):
        """Generate folder from pasted data"""
        #get folder name from preview
        text = self.paste_text.get("1.0", tk.END).strip()

        if not text:
            messagebox.showerror("Error", "Please paste data into the text box.")
            return

        #get folder name from preview

        folder_name = self.paste_preview.cget("text")

        if not folder_name or folder_name in ["Preview will appear here...", "Unable to parse data. Check format."]:
            messagebox.showerror("Error", "Could not generate folder from pasted data. Check format.")
            return

        #create folders
        data = self.parse_pasted_data(text)
        success, result = self.create_folder_structure(folder_name, data["unique_id"])

        if success:
            messagebox.showinfo("Success", f"Folder created successfully.\n\nLocation:\n {result}")
            self.paste_text.delete("1.0", tk.END)
            self.paste_preview.config(text="")
        else:
            messagebox.showerror("Error", f"Failed to create folder:\n{result}")

    def generate_from_manual(self):
        """Generate folder from manual input"""
        #get folder name from preview
        folder_name = self.manual_preview.cget("text")

        if not folder_name or folder_name == "Preview will appear here..." or "[" in folder_name:
            messagebox.showerror("Error", "Please fill in all fields!")
            return

        unique_id = self.unique_id_entry.get().strip().upper()
        success, result = self.create_folder_structure(folder_name, unique_id)

        if success:
            messagebox.showinfo("Success", f"Folder created successfully.\n\nLocation:\n {result}")
            #clear entries
            self.due_date_entry.delete(0, tk.END)
            self.patient_name_entry.delete(0, tk.END)
            self.unique_id_entry.delete(0, tk.END)
            self.center_name_entry.delete(0, tk.END)
            self.manual_preview.config(text="")
        else:
            messagebox.showerror("Error", f"Failed to create folder:\n{result}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PatientFolderCreatorGUI(root)
    root.mainloop()
