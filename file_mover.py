import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import shutil
import os
import time
import threading
from datetime import datetime

class FileMoverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Mover_Rev1.0.0")
        self.root.geometry("600x400")
        
        # Variables
        self.source_path = tk.StringVar()
        self.dest_path = tk.StringVar()
        self.wait_time = tk.StringVar(value="60")  # Default 60 seconds
        self.is_running = False
        self.status_text = tk.StringVar(value="Ready")
        
        # Create GUI elements
        self.create_widgets()
        
    def create_widgets(self):
        # Source path
        ttk.Label(self.root, text="Source Path:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(self.root, textvariable=self.source_path, width=50).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(self.root, text="Browse", command=self.browse_source).grid(row=0, column=2, padx=5, pady=5)
        
        # Destination path
        ttk.Label(self.root, text="Destination Path:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(self.root, textvariable=self.dest_path, width=50).grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(self.root, text="Browse", command=self.browse_dest).grid(row=1, column=2, padx=5, pady=5)
        
        # Wait time
        ttk.Label(self.root, text="Wait Time (seconds):").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(self.root, textvariable=self.wait_time, width=10).grid(row=2, column=1, padx=5, pady=5, sticky="w")
        
        # Status display
        ttk.Label(self.root, text="Status:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        ttk.Label(self.root, textvariable=self.status_text).grid(row=3, column=1, padx=5, pady=5, sticky="w")
        
        # Start/Stop button
        self.start_button = ttk.Button(self.root, text="Start", command=self.toggle_moving)
        self.start_button.grid(row=4, column=1, padx=5, pady=20)
        
        # Log display
        self.log_text = tk.Text(self.root, height=10, width=60)
        self.log_text.grid(row=5, column=0, columnspan=3, padx=5, pady=5)
        
    def browse_source(self):
        path = filedialog.askdirectory()
        if path:
            self.source_path.set(path)
            
    def browse_dest(self):
        path = filedialog.askdirectory()
        if path:
            self.dest_path.set(path)
            
    def log_message(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        
    def toggle_moving(self):
        if not self.is_running:
            if not self.validate_paths():
                return
            self.is_running = True
            self.start_button.config(text="Stop")
            self.moving_thread = threading.Thread(target=self.move_files_loop)
            self.moving_thread.daemon = True
            self.moving_thread.start()
        else:
            self.is_running = False
            self.start_button.config(text="Start")
            self.status_text.set("Stopped")
            
    def validate_paths(self):
        if not self.source_path.get() or not self.dest_path.get():
            messagebox.showerror("Error", "Please select both source and destination paths")
            return False
        if not os.path.exists(self.source_path.get()):
            messagebox.showerror("Error", "Source path does not exist")
            return False
        if not os.path.exists(self.dest_path.get()):
            messagebox.showerror("Error", "Destination path does not exist")
            return False
        try:
            wait_time = int(self.wait_time.get())
            if wait_time < 1:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Wait time must be a positive integer")
            return False
        return True
        
    def move_files_loop(self):
        while self.is_running:
            try:
                files = os.listdir(self.source_path.get())
                files = [f for f in files if os.path.isfile(os.path.join(self.source_path.get(), f))]
                
                if not files:
                    self.status_text.set("No files to move")
                    self.log_message("No files found in source directory")
                else:
                    moved_count = 0
                    for file in files[:10]:  # Move maximum 10 files per cycle
                        if not self.is_running:
                            break
                            
                        source_file = os.path.join(self.source_path.get(), file)
                        dest_file = os.path.join(self.dest_path.get(), file)
                        
                        try:
                            shutil.move(source_file, dest_file)
                            self.log_message(f"Moved: {file}")
                            moved_count += 1
                        except Exception as e:
                            self.log_message(f"Error moving {file}: {str(e)}")
                            
                    self.status_text.set(f"Moved {moved_count} files")
                    
                # Wait for the specified time
                wait_time = int(self.wait_time.get())
                for _ in range(wait_time):
                    if not self.is_running:
                        break
                    time.sleep(1)
                    
            except Exception as e:
                self.log_message(f"Error: {str(e)}")
                self.status_text.set("Error occurred")
                time.sleep(5)

if __name__ == "__main__":
    root = tk.Tk()
    app = FileMoverApp(root)
    root.mainloop() 