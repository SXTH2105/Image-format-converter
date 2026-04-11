import os
import tkinter as tk
from tkinter import filedialog
try:
    from PIL import Image
except ImportError:
    print("Pillow library is not installed. Please install it using 'pip install Pillow'")
    exit(1)

def main():
    # Hide the main tkinter window
    root = tk.Tk()
    root.withdraw()

    print("Please select an image file to convert...")
    # Open file dialog
    file_path = filedialog.askopenfilename(
        title="Select an Image",
        filetypes=[
            ("Image files", "*.jpg *.jpeg *.png *.webp *.bmp *.gif *.tiff *.ico"),
            ("All files", "*.*")
        ]
    )

    if not file_path:
        print("No file selected. Exiting.")
        return

    # Analyze the image
    try:
        with Image.open(file_path) as img:
            original_format = img.format
            img_mode = img.mode
            print(f"\n--- Image Analysis ---")
            print(f"Selected image: {os.path.basename(file_path)}")
            print(f"Current format: {original_format}")
            print(f"Color mode  : {img_mode}")
            print(f"Dimensions  : {img.size[0]}x{img.size[1]}")
            print(f"----------------------\n")
            
            supported_formats = ['JPEG', 'PNG', 'WEBP', 'BMP', 'GIF', 'TIFF', 'ICO', 'SVG']
            
            # Remove the original format from the list of options to avoid converting to the exact same format
            options = [fmt for fmt in supported_formats if fmt != original_format]

            print("Available formats to convert to:")
            for i, fmt in enumerate(options, 1):
                print(f"{i}. {fmt}")
            
            choice = input(f"\nEnter the number of the format you want to convert to (1-{len(options)}): ")
            
            try:
                choice_idx = int(choice) - 1
                if choice_idx < 0 or choice_idx >= len(options):
                    print("Invalid choice. Exiting.")
                    return
                target_format = options[choice_idx]
            except ValueError:
                print("Invalid input. Exiting.")
                return

            # Prepare output directory
            script_dir = os.path.dirname(os.path.abspath(__file__))
            output_dir = os.path.join(script_dir, "Converted Img")
            os.makedirs(output_dir, exist_ok=True)

            # Prepare output filename
            # name of the image before converted + the name of format after converted
            base_name = os.path.splitext(os.path.basename(file_path))[0]
            ext_map = {'JPEG': '.jpg', 'PNG': '.png', 'WEBP': '.webp', 'BMP': '.bmp', 'GIF': '.gif', 'TIFF': '.tiff', 'ICO': '.ico', 'SVG': '.svg'}
            output_ext = ext_map[target_format]
            
            output_filename = f"{base_name}_{target_format}{output_ext}"
            output_path = os.path.join(output_dir, output_filename)

            # Convert and save
            # When converting to formats that don't support transparency (like JPEG), 
            # we need to convert RGBA/LA (with alpha channel) to RGB first.
            if target_format == 'SVG':
                import io
                import base64
                buffered = io.BytesIO()
                # Embed as Base64 encoded PNG inside the SVG
                img.save(buffered, format="PNG")
                img_str = base64.b64encode(buffered.getvalue()).decode()
                svg_content = f'<svg width="{img.width}" height="{img.height}" xmlns="http://www.w3.org/2000/svg">\n  <image href="data:image/png;base64,{img_str}" width="{img.width}" height="{img.height}"/>\n</svg>'
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(svg_content)
            elif target_format in ('JPEG', 'BMP') and img.mode in ('RGBA', 'LA', 'P'):
                # Create a white background image to replace transparency
                background = Image.new("RGB", img.size, (255, 255, 255))
                if img.mode == 'P':
                    img_rgba = img.convert('RGBA')
                    background.paste(img_rgba, mask=img_rgba.split()[3])
                else:
                    background.paste(img, mask=img.split()[3] if img.mode == 'RGBA' else img.split()[1])
                background.save(output_path, target_format)
            else:
                img.save(output_path, target_format)

            print(f"\n✅ Successfully converted to {target_format}!")
            print(f"📁 Saved at: {output_path}")

    except Exception as e:
        print(f"\n❌ Error processing image: {e}")

if __name__ == "__main__":
    main()
