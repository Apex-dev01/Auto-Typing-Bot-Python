# OCR Auto Typing Tool - Setup & Usage Guide

## Overview

The OCR version of the Auto Typing Tool lets you extract text from any window or screen region using Optical Character Recognition (OCR), and then automatically type that text into typing.com or any other application.

### Key Features
- **Window Region Selection**: Click and drag to select any area of your screen
- **Free OCR Engine**: Uses Tesseract OCR (open-source)
- **Real-time Text Extraction**: Instantly extracts text from selected regions
- **Adjustable Typing Speed**: Control WPM (words per minute) settings
- **Seamless Integration**: Works with typing.com, text editors, and any typing platform

---

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Step 1: Install Tesseract OCR Engine

**Windows:**
1. Download the installer from: https://github.com/UB-Mannheim/tesseract/wiki
2. Run the installer (recommended path: `C:\Program Files\Tesseract-OCR`)
3. Note the installation path

**macOS:**
```bash
brew install tesseract
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install tesseract-ocr
```

### Step 2: Install Python Dependencies

```bash
pip install -r requirements-ocr.txt
```

Or install manually:
```bash
pip install pynput pillow pytesseract opencv-python numpy
```

### Step 3 (Windows Only): Configure Tesseract Path

If Tesseract was installed in a non-standard location, you may need to add this to `ocr_typer.py`:

```python
import pytesseract
pytesseract.pytesseract.pytesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

---

## Usage

### Running the OCR Auto Typing Tool

```bash
python ocr_typer.py
```

### How to Use

1. **Launch the Application**
   - Run the command above
   - The GUI window will appear

2. **Extract Text from Screen**
   - Click the green "📸 Select Region for OCR" button
   - A semi-transparent overlay will appear
   - Click and drag to select the text area you want to extract
   - Release the mouse to perform OCR
   - Extracted text appears in the text area

3. **Adjust Typing Speed**
   - Set Min WPM (Words Per Minute) - minimum typing speed
   - Set Max WPM (Words Per Minute) - maximum typing speed
   - Default: 40-60 WPM for human-like typing
   - Click "Increase Speed" to multiply by 1.5x

4. **Control Typing**
   - **Start**: Begin typing from the current position
   - **Pause**: Temporarily stop typing
   - **Continue**: Resume typing from where it paused
   - **Stop**: Stop typing and reset to the beginning
   - **Increase Speed**: Make the typing 1.5x faster

### Common Workflows

#### For typing.com
1. Open typing.com in your browser
2. Copy the test passage or screenshot it
3. Click "Select Region for OCR" to extract text from the passage
4. Click "Start" with your cursor in the typing area
5. Watch as it automatically types the text

#### For copying from PDF or Images
1. Open the PDF or image file
2. Use "Select Region for OCR" to extract text
3. The extracted text will appear in the tool
4. Use Start/Pause/Continue to control the typing speed

---

## Troubleshooting

### Issue: "pytesseract is not installed"
**Solution**: Run `pip install pytesseract`

### Issue: Tesseract not found (Windows)
**Solution**: Ensure Tesseract-OCR is installed. If installed in a custom location, add the path to `ocr_typer.py`

### Issue: OCR Accuracy Issues
**Solutions**:
- Try taking a screenshot of better quality text
- Increase contrast in the image
- Select only the text area (avoid buttons/UI elements)
- Try alternative: EasyOCR or PaddleOCR (install from `requirements-ocr.txt`)

### Issue: Typing is too slow/fast
**Solution**: Adjust the Min WPM and Max WPM values, or click "Increase Speed"

### Issue: Application freezes while typing
**Solution**: Click "Pause" or "Stop" button. This is normal for long texts.

---

## Advanced Features

### Alternative OCR Engines

If Tesseract accuracy isn't sufficient, you can try:

**EasyOCR:**
```bash
pip install easyocr
```

**PaddleOCR:**
```bash
pip install paddleocr
```

These are more accurate but slower than Tesseract.

---

## Performance Tips

1. **Optimize OCR Speed**: Select only the text area, not extra whitespace
2. **Better Results**: Use high-contrast, clear text
3. **Improve Accuracy**: Pre-process images (increase contrast, remove noise)
4. **Faster Typing**: Increase WPM values for non-typing tests

---

## System Requirements

- **RAM**: 2GB minimum (4GB+ recommended)
- **Disk Space**: ~500MB for Tesseract + Python packages
- **OS**: Windows, macOS, or Linux
- **Python**: 3.7 or higher

---

## Legal Notice

This tool is for personal use and educational purposes. Ensure you have the right to use extracted content. Do not use this tool to:
- Bypass security measures
- Copy copyrighted content without permission
- Cheat on academic assessments

---

## Support & Contributions

For issues, suggestions, or improvements:
1. Check the troubleshooting section above
2. Review the code comments in `ocr_typer.py`
3. Open an issue on GitHub
4. Submit a pull request with improvements

---

## License

This project is licensed under the MIT License. See LICENSE file for details.
