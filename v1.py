import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
from pdf2image import convert_from_path
from pdf2docx import Converter
from PIL import Image
import fitz  # PyMuPDF
import pytesseract
import os

class PDFEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Editor")
        self.root.geometry("300x400")
        
        # Create a frame for buttons
        frame = tk.Frame(root)
        frame.pack(pady=20)

        # Add buttons for each functionality
        button_config = {
            "fill": 'x',
            "padx": 5,
            "pady": 5
        }
        
        tk.Button(frame, text="Merge PDFs", command=self.merge_pdfs).pack(**button_config)
        tk.Button(frame, text="Split PDF", command=self.split_pdf).pack(**button_config)
        tk.Button(frame, text="Delete Page from PDF", command=self.delete_page_from_pdf).pack(**button_config)
        tk.Button(frame, text="PDF to JPG", command=self.pdf_to_jpg).pack(**button_config)
        tk.Button(frame, text="JPG to PDF", command=self.jpg_to_pdf).pack(**button_config)
        tk.Button(frame, text="PDF Text Editor", command=self.pdf_text_editor).pack(**button_config)
        tk.Button(frame, text="Add Images to PDF", command=self.add_images_to_pdf).pack(**button_config)
        tk.Button(frame, text="PDF to Word", command=self.pdf_to_word).pack(**button_config)
        tk.Button(frame, text="Unlock PDF", command=self.unlock_pdf).pack(**button_config)
        tk.Button(frame, text="Crop PDF", command=self.crop_pdf).pack(**button_config)
        tk.Button(frame, text="Add Watermark", command=self.add_watermark).pack(**button_config)
        tk.Button(frame, text="Compress PDF", command=self.compress_pdf).pack(**button_config)
        tk.Button(frame, text="OCR PDF", command=self.ocr_pdf).pack(**button_config)

    def open_file_dialog(self, filetypes):
        return filedialog.askopenfilename(filetypes=filetypes)

    def open_files_dialog(self, filetypes):
        return filedialog.askopenfilenames(filetypes=filetypes)

    def save_file_dialog(self, filetypes, defaultextension):
        return filedialog.asksaveasfilename(filetypes=filetypes, defaultextension=defaultextension)

    def merge_pdfs(self):
        files = self.open_files_dialog([("PDF files", "*.pdf")])
        output = self.save_file_dialog([("PDF files", "*.pdf")], defaultextension=".pdf")
        if files and output:
            merger = PdfMerger()
            for pdf in files:
                merger.append(pdf)
            merger.write(output)
            merger.close()
            messagebox.showinfo("Success", "PDFs merged successfully")

    def split_pdf(self):
        file = self.open_file_dialog([("PDF files", "*.pdf")])
        output_dir = filedialog.askdirectory()
        if file and output_dir:
            reader = PdfReader(file)
            for i in range(len(reader.pages)):
                writer = PdfWriter()
                writer.add_page(reader.pages[i])
                with open(os.path.join(output_dir, f"page_{i + 1}.pdf"), 'wb') as out_file:
                    writer.write(out_file)
            messagebox.showinfo("Success", "PDF split successfully")

    def delete_page_from_pdf(self):
        file = self.open_file_dialog([("PDF files", "*.pdf")])
        output = self.save_file_dialog([("PDF files", "*.pdf")], defaultextension=".pdf")
        pages_to_delete = simpledialog.askstring("Input", "Enter page numbers to delete (comma-separated):")
        if file and output and pages_to_delete:
            pages_to_delete = [int(x)-1 for x in pages_to_delete.split(",")]
            reader = PdfReader(file)
            writer = PdfWriter()
            for i in range(len(reader.pages)):
                if i not in pages_to_delete:
                    writer.add_page(reader.pages[i])
            with open(output, 'wb') as out_file:
                writer.write(out_file)
            messagebox.showinfo("Success", "Pages deleted successfully")

    def pdf_to_jpg(self):
        file = self.open_file_dialog([("PDF files", "*.pdf")])
        output_dir = filedialog.askdirectory()
        if file and output_dir:
            images = convert_from_path(file)
            for i, image in enumerate(images):
                image.save(os.path.join(output_dir, f"page_{i + 1}.jpg"), 'JPEG')
            messagebox.showinfo("Success", "PDF converted to JPG successfully")

    def jpg_to_pdf(self):
        files = self.open_files_dialog([("Image files", "*.jpg;*.jpeg")])
        output = self.save_file_dialog([("PDF files", "*.pdf")], defaultextension=".pdf")
        if files and output:
            images = [Image.open(img).convert('RGB') for img in files]
            images[0].save(output, save_all=True, append_images=images[1:])
            messagebox.showinfo("Success", "JPG converted to PDF successfully")

    def pdf_text_editor(self):
        file = self.open_file_dialog([("PDF files", "*.pdf")])
        output = self.save_file_dialog([("PDF files", "*.pdf")], defaultextension=".pdf")
        text = simpledialog.askstring("Input", "Enter the text to add:")
        if file and output and text:
            doc = fitz.open(file)
            page = doc[0]
            page.insert_text((50, 50), text)
            doc.save(output)
            messagebox.showinfo("Success", "Text added to PDF successfully")

    def add_images_to_pdf(self):
        file = self.open_file_dialog([("PDF files", "*.pdf")])
        image_file = self.open_file_dialog([("Image files", "*.jpg;*.jpeg;*.png")])
        output = self.save_file_dialog([("PDF files", "*.pdf")], defaultextension=".pdf")
        if file and image_file and output:
            doc = fitz.open(file)
            page = doc[0]
            rect = fitz.Rect(100, 100, 200, 200)
            page.insert_image(rect, filename=image_file)
            doc.save(output)
            messagebox.showinfo("Success", "Image added to PDF successfully")

    def pdf_to_word(self):
        file = self.open_file_dialog([("PDF files", "*.pdf")])
        output = self.save_file_dialog([("Word files", "*.docx")], defaultextension=".docx")
        if file and output:
            cv = Converter(file)
            cv.convert(output)
            cv.close()
            messagebox.showinfo("Success", "PDF converted to Word successfully")

    def unlock_pdf(self):
        file = self.open_file_dialog([("PDF files", "*.pdf")])
        output = self.save_file_dialog([("PDF files", "*.pdf")], defaultextension=".pdf")
        password = simpledialog.askstring("Input", "Enter the PDF password:")
        if file and output and password:
            reader = PdfReader(file)
            reader.decrypt(password)
            writer = PdfWriter()
            for page in reader.pages:
                writer.add_page(page)
            with open(output, 'wb') as out_file:
                writer.write(out_file)
            messagebox.showinfo("Success", "PDF unlocked successfully")

    def crop_pdf(self):
        file = self.open_file_dialog([("PDF files", "*.pdf")])
        output = self.save_file_dialog([("PDF files", "*.pdf")], defaultextension=".pdf")
        crop_rect = simpledialog.askstring("Input", "Enter crop rectangle (x0,y0,x1,y1):")
        if file and output and crop_rect:
            rect = fitz.Rect([int(x) for x in crop_rect.split(",")])
            doc = fitz.open(file)
            for page in doc:
                page.set_cropbox(rect)
            doc.save(output)
            messagebox.showinfo("Success", "PDF cropped successfully")

    def add_watermark(self):
        file = self.open_file_dialog([("PDF files", "*.pdf")])
        output = self.save_file_dialog([("PDF files", "*.pdf")], defaultextension=".pdf")
        watermark_text = simpledialog.askstring("Input", "Enter the watermark text:")
        if file and output and watermark_text:
            reader = PdfReader(file)
            writer = PdfWriter()
            for page in reader.pages:
                writer.add_page(page)
                writer.get_page(-1).insert_text((50, 50), watermark_text, fontsize=40, color=(0, 0, 0, 0.1))
            with open(output, 'wb') as out_file:
                writer.write(out_file)
            messagebox.showinfo("Success", "Watermark added to PDF successfully")

    def compress_pdf(self):
        file = self.open_file_dialog([("PDF files", "*.pdf")])
        output = self.save_file_dialog([("PDF files", "*.pdf")], defaultextension=".pdf")
        if file and output:
            doc = fitz.open(file)
            doc.save(output, deflate=True)
            messagebox.showinfo("Success", "PDF compressed successfully")

    def ocr_pdf(self):
        file = self.open_file_dialog([("PDF files", "*.pdf")])
        output = self.save_file_dialog([("PDF files", "*.pdf")], defaultextension=".pdf")
        if file and output:
            doc = fitz.open(file)
            for page in doc:
                pix = page.get_pixmap()
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                text = pytesseract.image_to_string(img)
                page.insert_text((50, 50), text)
            doc.save(output)
            messagebox.showinfo("Success", "OCR performed on PDF successfully")

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFEditor(root)
    root.mainloop()
