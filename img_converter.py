import os
import customtkinter as ctk
from tkinter import filedialog, messagebox
try:
    from PIL import Image
except ImportError:
    import sys
    print("Pillow library is not installed. Please install it using 'pip install Pillow'")
    sys.exit(1)

# Set UI Theme
ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class ImageConverterApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Image Format Converter")
        self.geometry("600x680")
        self.resizable(False, False)

        # State Variables
        self.selected_file_path = None
        self.img_info = None
        self.supported_formats = ['JPEG', 'PNG', 'WEBP', 'BMP', 'GIF', 'TIFF', 'ICO', 'SVG']
        self.target_format = ctk.StringVar(value="Select Format")
        self.output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Converted Img")

        self.setup_ui()

    def setup_ui(self):
        # Header title
        self.lbl_title = ctk.CTkLabel(self, text="Image Format Converter", font=ctk.CTkFont(size=24, weight="bold"))
        self.lbl_title.pack(pady=(20, 10))

        # --- File Selection Section ---
        self.frame_file = ctk.CTkFrame(self)
        self.frame_file.pack(pady=10, padx=20, fill="x")

        self.lbl_file_path = ctk.CTkLabel(self.frame_file, text="No file selected", text_color="gray", wraplength=400)
        self.lbl_file_path.pack(side="left", padx=10, pady=15, expand=True, fill="x")

        self.btn_browse = ctk.CTkButton(self.frame_file, text="Browse Image", command=self.browse_file, width=120)
        self.btn_browse.pack(side="right", padx=10, pady=15)

        # --- Output Selection Section ---
        self.frame_output = ctk.CTkFrame(self)
        self.frame_output.pack(pady=5, padx=20, fill="x")

        self.lbl_output_path = ctk.CTkLabel(self.frame_output, text=f"Save to: {self.output_dir}", text_color="gray", wraplength=400)
        self.lbl_output_path.pack(side="left", padx=10, pady=15, expand=True, fill="x")

        self.btn_browse_output = ctk.CTkButton(self.frame_output, text="Browse Folder", command=self.browse_output, width=120)
        self.btn_browse_output.pack(side="right", padx=10, pady=15)

        # --- Image Details Section ---
        self.frame_details = ctk.CTkFrame(self)
        self.frame_details.pack(pady=10, padx=20, fill="x")

        self.lbl_details_title = ctk.CTkLabel(self.frame_details, text="Image Details", font=ctk.CTkFont(size=16, weight="bold"))
        self.lbl_details_title.pack(pady=(10, 5))

        self.lbl_format = ctk.CTkLabel(self.frame_details, text="Original Format: -")
        self.lbl_format.pack(pady=2)

        self.lbl_mode = ctk.CTkLabel(self.frame_details, text="Color Mode: -")
        self.lbl_mode.pack(pady=2)

        self.lbl_size = ctk.CTkLabel(self.frame_details, text="Dimensions:")
        self.lbl_size.pack(pady=(2, 5))

        # Resolution fields
        self.frame_res = ctk.CTkFrame(self.frame_details, fg_color="transparent")
        self.frame_res.pack(pady=(0, 10))

        self.entry_width = ctk.CTkEntry(self.frame_res, placeholder_text="Width", width=80)
        self.entry_width.pack(side="left", padx=(0, 5))
        self.lbl_x = ctk.CTkLabel(self.frame_res, text="x")
        self.lbl_x.pack(side="left")
        self.entry_height = ctk.CTkEntry(self.frame_res, placeholder_text="Height", width=80)
        self.entry_height.pack(side="left", padx=(5, 0))

        # --- Conversion Settings ---
        self.frame_settings = ctk.CTkFrame(self)
        self.frame_settings.pack(pady=10, padx=20, fill="x")

        self.lbl_target = ctk.CTkLabel(self.frame_settings, text="Target Format:")
        self.lbl_target.pack(side="left", padx=10, pady=15)

        self.opt_target = ctk.CTkOptionMenu(self.frame_settings, variable=self.target_format, values=["Select Image First"], state="disabled")
        self.opt_target.pack(side="left", padx=10, pady=15, expand=True, fill="x")

        # --- Action & Status Section ---
        self.btn_convert = ctk.CTkButton(self, text="Convert Image", command=self.convert_image, font=ctk.CTkFont(size=16, weight="bold"), height=40, state="disabled")
        self.btn_convert.pack(pady=20, padx=20, fill="x")

        self.lbl_status = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=12))
        self.lbl_status.pack(pady=(0, 10))

    def browse_file(self):
        file_path = filedialog.askopenfilename(
            title="Select an Image",
            filetypes=[
                ("Image files", "*.jpg *.jpeg *.png *.webp *.bmp *.gif *.tiff *.ico"),
                ("All files", "*.*")
            ]
        )
        if file_path:
            self.selected_file_path = file_path
            self.lbl_file_path.configure(text=os.path.basename(file_path), text_color="white")
            self.analyze_image()

    def browse_output(self):
        folder_path = filedialog.askdirectory(title="Select Output Folder")
        if folder_path:
            self.output_dir = folder_path
            self.lbl_output_path.configure(text=f"Save to: {self.output_dir}", text_color="white")

    def analyze_image(self):
        if not self.selected_file_path:
            return

        try:
            with Image.open(self.selected_file_path) as img:
                original_format = img.format
                img_mode = img.mode
                width, height = img.size

                self.img_info = {
                    'format': original_format,
                    'mode': img_mode,
                    'size': (width, height)
                }

                self.lbl_format.configure(text=f"Original Format: {original_format}")
                self.lbl_mode.configure(text=f"Color Mode: {img_mode}")
                self.lbl_size.configure(text=f"Original Dimensions: {width}x{height}")

                # Update resolution entries
                self.entry_width.delete(0, 'end')
                self.entry_width.insert(0, str(width))
                self.entry_height.delete(0, 'end')
                self.entry_height.insert(0, str(height))

                # Update target formats dropdown
                options = [fmt for fmt in self.supported_formats if fmt != original_format]
                self.opt_target.configure(values=options, state="normal")
                self.target_format.set(options[0])
                
                self.btn_convert.configure(state="normal")
                self.lbl_status.configure(text="", text_color="white")

        except Exception as e:
            self.lbl_status.configure(text=f"Error analyzing image: {str(e)}", text_color="red")
            self.opt_target.configure(state="disabled")
            self.btn_convert.configure(state="disabled")

    def convert_image(self):
        if not self.selected_file_path:
            return

        target_fmt = self.target_format.get()
        if target_fmt in ("Select Image First", "Select Format"):
            return

        # Validate resolution inputs
        try:
            target_width = int(self.entry_width.get())
            target_height = int(self.entry_height.get())
            if target_width <= 0 or target_height <= 0:
                raise ValueError()
        except ValueError:
            self.lbl_status.configure(text="❌ Error: Dimensions must be valid positive integers.", text_color="#EF4444")
            return

        self.btn_convert.configure(state="disabled", text="Converting...")
        self.update()

        try:
            # Prepare output directory
            os.makedirs(self.output_dir, exist_ok=True)

            # Prepare output filename
            base_name = os.path.splitext(os.path.basename(self.selected_file_path))[0]
            ext_map = {'JPEG': '.jpg', 'PNG': '.png', 'WEBP': '.webp', 'BMP': '.bmp', 'GIF': '.gif', 'TIFF': '.tiff', 'ICO': '.ico', 'SVG': '.svg'}
            output_ext = ext_map[target_fmt]
            
            output_filename = f"{base_name}_{target_width}x{target_height}_{target_fmt}{output_ext}"
            output_path = os.path.join(self.output_dir, output_filename)

            with Image.open(self.selected_file_path) as img:
                # Resize if the requested dimensions differ from the original
                if (target_width, target_height) != img.size:
                    img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)

                # Convert and save
                if target_fmt == 'SVG':
                    import io
                    import base64
                    buffered = io.BytesIO()
                    # Embed as Base64 encoded PNG inside the SVG
                    img.save(buffered, format="PNG")
                    img_str = base64.b64encode(buffered.getvalue()).decode()
                    svg_content = f'<svg width="{img.width}" height="{img.height}" xmlns="http://www.w3.org/2000/svg">\n  <image href="data:image/png;base64,{img_str}" width="{img.width}" height="{img.height}"/>\n</svg>'
                    with open(output_path, "w", encoding="utf-8") as f:
                        f.write(svg_content)
                elif target_fmt in ('JPEG', 'BMP') and img.mode in ('RGBA', 'LA', 'P'):
                    # Create a white background image to replace transparency
                    background = Image.new("RGB", img.size, (255, 255, 255))
                    if img.mode == 'P':
                        img_rgba = img.convert('RGBA')
                        background.paste(img_rgba, mask=img_rgba.split()[3])
                    else:
                        background.paste(img, mask=img.split()[3] if img.mode == 'RGBA' else img.split()[1])
                    background.save(output_path, target_fmt)
                else:
                    img.save(output_path, target_fmt)

            self.lbl_status.configure(text=f"✅ Successfully converted & saved to:\n{output_path}", text_color="#10B981")

        except Exception as e:
            self.lbl_status.configure(text=f"❌ Error during conversion: {str(e)}", text_color="#EF4444")
        
        finally:
            self.btn_convert.configure(state="normal", text="Convert Image")


if __name__ == "__main__":
    app = ImageConverterApp()
    app.mainloop()

