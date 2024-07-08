import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import json
import threading

Image.MAX_IMAGE_PIXELS = 933120000

class HeightmapConverter:
    def __init__(self, master):
        self.master = master
        self.master.title("Heightmap Converter")

        self.image_path = None
        self.heightmap_data = None
        self.scale = 100
        self.offset = 0
        self.chunk_size = 500
        self.enable_preprocessing = tk.BooleanVar(value=True)
        self.preprocess_width_value = tk.StringVar(value="500")
        self.preprocess_height_value = tk.StringVar(value="500")
        self.preprocess_width_unit = tk.StringVar(value="px")
        self.preprocess_height_unit = tk.StringVar(value="px")

        self.logger = self.create_logger()

        self.create_widgets()

    def create_logger(self):
        logger_frame = tk.Frame(self.master)
        logger_frame.pack(fill=tk.BOTH, expand=True)

        log_label = tk.Label(logger_frame, text="Log")
        log_label.pack()

        self.log_text = tk.Text(logger_frame, state='disabled', height=10)
        self.log_text.pack(fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(logger_frame, command=self.log_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text['yscrollcommand'] = scrollbar.set

        return self.log_text

    def log(self, message):
        self.logger.config(state='normal')
        self.logger.insert(tk.END, message + "\n")
        self.logger.config(state='disabled')
        self.logger.yview(tk.END)

    def create_widgets(self):
        self.load_image_button = tk.Button(self.master, text="Load Image", command=self.load_image)
        self.load_image_button.pack()

        self.preprocessing_checkbox = tk.Checkbutton(self.master, text="Enable Preprocessing", variable=self.enable_preprocessing)
        self.preprocessing_checkbox.pack()

        self.preprocess_size_frame = tk.Frame(self.master)
        self.preprocess_size_frame.pack()

        self.preprocess_width_label = tk.Label(self.preprocess_size_frame, text="Width:")
        self.preprocess_width_label.grid(row=0, column=0)
        self.preprocess_width_entry = tk.Entry(self.preprocess_size_frame, textvariable=self.preprocess_width_value)
        self.preprocess_width_entry.grid(row=0, column=1)

        self.preprocess_width_unit_menu = ttk.Combobox(self.preprocess_size_frame, textvariable=self.preprocess_width_unit, values=["px", "%"], width=5)
        self.preprocess_width_unit_menu.grid(row=0, column=2)

        self.preprocess_height_label = tk.Label(self.preprocess_size_frame, text="Height:")
        self.preprocess_height_label.grid(row=1, column=0)
        self.preprocess_height_entry = tk.Entry(self.preprocess_size_frame, textvariable=self.preprocess_height_value)
        self.preprocess_height_entry.grid(row=1, column=1)

        self.preprocess_height_unit_menu = ttk.Combobox(self.preprocess_size_frame, textvariable=self.preprocess_height_unit, values=["px", "%"], width=5)
        self.preprocess_height_unit_menu.grid(row=1, column=2)

        self.scale_label = tk.Label(self.master, text="Height Scale:")
        self.scale_label.pack()
        self.scale_entry = tk.Entry(self.master)
        self.scale_entry.insert(0, str(self.scale))
        self.scale_entry.pack()

        self.offset_label = tk.Label(self.master, text="Height Offset:")
        self.offset_label.pack()
        self.offset_entry = tk.Entry(self.master)
        self.offset_entry.insert(0, str(self.offset))
        self.offset_entry.pack()

        self.process_image_button = tk.Button(self.master, text="Process Image", command=self.process_image_thread)
        self.process_image_button.pack()

        self.save_heightmap_button = tk.Button(self.master, text="Save Heightmap", command=self.save_heightmap_thread)
        self.save_heightmap_button.pack()

        self.preview_button = tk.Button(self.master, text="Preview Heightmap", command=self.preview_heightmap_thread)
        self.preview_button.pack()
        
        self.progress = ttk.Progressbar(self.master, orient="horizontal", mode="determinate")
        self.progress.pack(fill=tk.BOTH, expand=True, pady=10)

    def update_progress(self, value):
        self.progress['value'] = value
        self.master.update_idletasks()

    def load_image(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.png;*.jpeg")])
        if self.image_path:
            self.log(f"Loaded image: {self.image_path}")
            messagebox.showinfo("Image Loaded", f"Loaded image: {self.image_path}")

    def process_image_thread(self):
        threading.Thread(target=self.process_image).start()

    def process_image(self):
        if not self.image_path:
            self.log("Error: Please load an image first")
            messagebox.showerror("Error", "Please load an image first")
            return
        
        try:
            self.scale = float(self.scale_entry.get())
            self.offset = float(self.offset_entry.get())
        except ValueError:
            self.log("Error: Scale and Offset must be numbers")
            messagebox.showerror("Error", "Scale and Offset must be numbers")
            return

        self.update_progress(0)
        image = Image.open(self.image_path).convert('L')
        width, height = image.size

        if self.enable_preprocessing.get():
            try:
                width_value = float(self.preprocess_width_value.get())
                height_value = float(self.preprocess_height_value.get())
            except ValueError:
                self.log("Error: Preprocessing width and height must be numbers")
                messagebox.showerror("Error", "Preprocessing width and height must be numbers")
                return

            if self.preprocess_width_unit.get() == "%":
                new_width = int(width * (width_value / 100))
            else:
                new_width = int(width_value)

            if self.preprocess_height_unit.get() == "%":
                new_height = int(height * (height_value / 100))
            else:
                new_height = int(height_value)

            self.log(f"Resizing image to ({new_width}, {new_height})")
            image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)

        width, height = image.size  
        chunks_x = width // self.chunk_size + (width % self.chunk_size != 0)
        chunks_y = height // self.chunk_size + (height % self.chunk_size != 0)
        
        self.heightmap_data = np.zeros((height, width))

        for i in range(chunks_y):
            for j in range(chunks_x):
                left = j * self.chunk_size
                upper = i * self.chunk_size
                right = min((j + 1) * self.chunk_size, width)
                lower = min((i + 1) * self.chunk_size, height)

                self.log(f"Processing chunk: ({left}, {upper}) to ({right}, {lower})")
                chunk = image.crop((left, upper, right, lower))

                chunk_data = np.asarray(chunk) / 255.0 * self.scale + self.offset
                self.heightmap_data[upper:lower, left:right] = chunk_data

                progress = ((i * chunks_x + j + 1) / (chunks_x * chunks_y)) * 100
                self.update_progress(progress)

        self.update_progress(100)
        self.log("Image processed successfully")
        messagebox.showinfo("Processing Complete", "Image processed successfully")

    def save_heightmap_thread(self):
        threading.Thread(target=self.save_heightmap).start()

    def save_heightmap(self):
        if self.heightmap_data is None:
            self.log("Error: Please process an image first")
            messagebox.showerror("Error", "Please process an image first")
            return
        
        save_path = filedialog.asksaveasfilename(defaultextension=".lua", filetypes=[("Lua files", "*.lua"), ("CSV files", "*.csv"), ("JSON files", "*.json")])
        if not save_path:
            return

        self.update_progress(0)
        if save_path.endswith('.lua'):
            self.save_as_lua(save_path)
        elif save_path.endswith('.csv'):
            self.save_as_csv(save_path)
        elif save_path.endswith('.json'):
            self.save_as_json(save_path)
        self.update_progress(100)

    def save_as_lua(self, path):
        self.log("Saving heightmap as Lua")
        rows, cols = self.heightmap_data.shape
        chunk_size = 100  
        total_chunks = rows // chunk_size + (rows % chunk_size != 0)
        with open(path, "w") as file:
            file.write("return {\n")
            for i in range(total_chunks):
                start = i * chunk_size
                end = min((i + 1) * chunk_size, rows)
                for row in self.heightmap_data[start:end]:
                    file.write("{" + ",".join(map(str, row)) + "},\n")
                progress = ((i + 1) / total_chunks) * 100
                self.update_progress(progress)
            file.write("}")
        self.log(f"Heightmap saved to {path}")
        messagebox.showinfo("Save Complete", f"Heightmap saved to {path}")

    def save_as_csv(self, path):
        self.log("Saving heightmap as CSV")
        rows, cols = self.heightmap_data.shape
        chunk_size = 100  
        total_chunks = rows // chunk_size + (rows % chunk_size != 0)
        with open(path, "w") as file:
            for i in range(total_chunks):
                start = i * chunk_size
                end = min((i + 1) * chunk_size, rows)
                np.savetxt(file, self.heightmap_data[start:end], delimiter=",")
                progress = ((i + 1) / total_chunks) * 100
                self.update_progress(progress)
        self.log(f"Heightmap saved to {path}")
        messagebox.showinfo("Save Complete", f"Heightmap saved to {path}")

    def save_as_json(self, path):
        self.log("Saving heightmap as JSON")
        rows, cols = self.heightmap_data.shape
        chunk_size = 100  
        total_chunks = rows // chunk_size + (rows % chunk_size != 0)
        with open(path, "w") as file:
            for i in range(total_chunks):
                start = i * chunk_size
                end = min((i + 1) * chunk_size, rows)
                json.dump(self.heightmap_data[start:end].tolist(), file)
                progress = ((i + 1) / total_chunks) * 100
                self.update_progress(progress)
        self.log(f"Heightmap saved to {path}")
        messagebox.showinfo("Save Complete", f"Heightmap saved to {path}")

    def preview_heightmap_thread(self):
        threading.Thread(target=self.preview_heightmap).start()

    def preview_heightmap(self):
        if self.heightmap_data is None:
            self.log("Error: Please process an image first")
            messagebox.showerror("Error", "Please process an image first")
            return

        plt.imshow(self.heightmap_data, cmap='gray')
        plt.colorbar()
        plt.title("Heightmap Preview")
        plt.show()

if __name__ == "__main__":
    root = tk.Tk()
    app = HeightmapConverter(root)
    root.mainloop()
