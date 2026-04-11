# 🖼️ Image Format Converter

A Python desktop application that converts images between popular formats using a GUI file picker — powered by Pillow. It analyzes your image, shows its details, and saves the converted output to a dedicated folder.

---

## 📋 Overview

This tool lets you select any image file through a graphical dialog, view its current format, color mode, and dimensions, then convert it to any supported format with a simple numbered menu. The converted image is saved automatically to a `Converted Img/` folder — no manual path typing required.

---

## ✨ Features

- 🖱️ **GUI file picker** — select your image visually via Tkinter
- 🔍 **Image analysis** — displays format, color mode, and dimensions before converting
- 🎨 **8 supported output formats** — JPEG, PNG, WEBP, BMP, GIF, TIFF, ICO, and SVG
- 🚫 **Skips same-format conversion** — only shows formats different from the original
- 🪟 **Transparency handling** — automatically flattens RGBA/alpha channels to a white background when converting to formats that don't support transparency (e.g. JPEG, BMP)
- 🧾 **SVG export** — embeds the image as a Base64-encoded PNG inside an SVG wrapper
- 💾 **Auto-saves** to a `Converted Img/` folder with a descriptive filename

---

## 🎨 Supported Formats

| Format | Extension |
|--------|-----------|
| JPEG | `.jpg` |
| PNG | `.png` |
| WEBP | `.webp` |
| BMP | `.bmp` |
| GIF | `.gif` |
| TIFF | `.tiff` |
| ICO | `.ico` |
| SVG | `.svg` |

---

## 🛠️ Tech Stack

- **Python 3**
- **Pillow (PIL)** — for image reading, analysis, and conversion
- **Tkinter** — for the GUI file picker dialog
- **os / io / base64** — standard library utilities

---

## 🚀 Getting Started

### Prerequisites

Install the required library:

```bash
pip install Pillow
```

### Installation

1. Clone the repository:

```bash
git clone https://github.com/SXTH2105/Image-format-converter.git
cd Image-format-converter
```

2. Run the script:

```bash
python img_converter.py
```

---

## 📖 How It Works

1. A file dialog opens — select your image (`.jpg`, `.jpeg`, `.png`, `.webp`, `.bmp`, `.gif`, `.tiff`, `.ico`).
2. The app displays the image's filename, current format, color mode, and dimensions.
3. A numbered list shows all available output formats (excluding the current one).
4. Enter your choice and the conversion begins.
5. The converted file is saved to the `Converted Img/` folder, named as `originalname_FORMAT.ext`.

---

## 🗂️ Output Example

```
Converted Img/
├── photo_PNG.png
├── banner_WEBP.webp
└── icon_ICO.ico
```

---

## 📁 Project Structure

```
Image-format-converter/
│
├── img_converter.py    # Main application file
└── Converted Img/      # Output folder (auto-created)
```

---

## ⚠️ Notes

- The `Converted Img/` folder is created automatically if it doesn't exist.
- Converting transparent images (RGBA/LA) to JPEG or BMP will replace the transparent areas with a **white background**.
- SVG output embeds the image as a Base64-encoded PNG — it is not a true vector conversion.

---

## 🔮 Future Improvements

- Support batch conversion of multiple images at once
- Add image resize or quality options before converting
- Preview the image before and after conversion
- Add a full GUI interface to replace the CLI menu
- Support drag-and-drop file input

---

## 👤 Author

**Seth**
- GitHub: [@SXTH2105](https://github.com/SXTH2105)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
