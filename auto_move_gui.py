import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import shutil
import time
import threading
import os

class AutoMoveApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Auto Move Files")
        self.root.geometry("600x400")
        
        # Variables
        self.source_path = tk.StringVar()
        self.dest_path = tk.StringVar()
        self.wait_time = tk.StringVar(value="60")  # Default 60 seconds
        self.is_running = False
        
        # Create GUI elements
        self.create_widgets()
        
    def create_widgets(self):
        # Source Path
        ttk.Label(self.root, text="Source Path:").pack(pady=5)
        source_frame = ttk.Frame(self.root)
        source_frame.pack(fill=tk.X, padx=10)
        
        ttk.Entry(source_frame, textvariable=self.source_path, width=50).pack(side=tk.LEFT, padx=5)
        ttk.Button(source_frame, text="Browse", command=self.browse_source).pack(side=tk.LEFT)
        
        # Destination Path
        ttk.Label(self.root, text="Destination Path:").pack(pady=5)
        dest_frame = ttk.Frame(self.root)
        dest_frame.pack(fill=tk.X, padx=10)
        
        ttk.Entry(dest_frame, textvariable=self.dest_path, width=50).pack(side=tk.LEFT, padx=5)
        ttk.Button(dest_frame, text="Browse", command=self.browse_dest).pack(side=tk.LEFT)
        
        # Wait Time
        ttk.Label(self.root, text="Wait Time (seconds):").pack(pady=5)
        ttk.Entry(self.root, textvariable=self.wait_time, width=10).pack()
        
        # Control Buttons
        control_frame = ttk.Frame(self.root)
        control_frame.pack(pady=20)
        
        self.start_button = ttk.Button(control_frame, text="Start", command=self.start_auto_move)
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = ttk.Button(control_frame, text="Stop", command=self.stop_auto_move, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        # Status Label
        self.status_label = ttk.Label(self.root, text="Status: Not Running")
        self.status_label.pack(pady=10)
        
    def browse_source(self):
        path = filedialog.askdirectory()
        if path:
            self.source_path.set(path)
            
    def browse_dest(self):
        path = filedialog.askdirectory()
        if path:
            self.dest_path.set(path)
            
    def start_auto_move(self):
        if not self.source_path.get() or not self.dest_path.get():
            messagebox.showerror("Error", "Please select both source and destination paths")
            return
            
        try:
            wait_time = int(self.wait_time.get())
            if wait_time <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid wait time (positive number)")
            return
            
        self.is_running = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.status_label.config(text="Status: Running")
        
        # Start the auto-move thread
        self.auto_move_thread = threading.Thread(target=self.auto_move_loop)
        self.auto_move_thread.daemon = True
        self.auto_move_thread.start()
        
    def stop_auto_move(self):
        self.is_running = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.status_label.config(text="Status: Stopped")
        
    def auto_move_loop(self):
        while self.is_running:
            try:
                # Get all files from source directory
                files = [f for f in os.listdir(self.source_path.get()) 
                        if os.path.isfile(os.path.join(self.source_path.get(), f))]
                
                # Move each file
                for file in files:
                    if not self.is_running:
                        break
                        
                    source_file = os.path.join(self.source_path.get(), file)
                    dest_file = os.path.join(self.dest_path.get(), file)
                    
                    try:
                        shutil.move(source_file, dest_file)
                        print(f"Moved: {file}")
                    except Exception as e:
                        print(f"Error moving {file}: {str(e)}")
                
                # Wait for the specified time
                for _ in range(int(self.wait_time.get())):
                    if not self.is_running:
                        break
                    time.sleep(1)
                    
            except Exception as e:
                print(f"Error in auto-move loop: {str(e)}")
                self.stop_auto_move()
                break

if __name__ == "__main__":
    root = tk.Tk()
    app = AutoMoveApp(root)
    root.mainloop() 