import tkinter as tk
from tkinter import filedialog, messagebox
import PyPDF2
import fitz  # PyMuPDF

def merge_pdfs():
    file_paths = filedialog.askopenfilenames(title="Select PDFs", filetypes=[("PDF files", "*.pdf")])
    if not file_paths:
        return

    try:
        pdf_writer = PyPDF2.PdfWriter()

        for file_path in file_paths:
            pdf_reader = PyPDF2.PdfReader(file_path)
            for page_num in range(len(pdf_reader.pages)):
                pdf_writer.add_page(pdf_reader.pages[page_num])

        output_path = filedialog.asksaveasfilename(title="Save Merged PDF", defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if output_path:
            with open(output_path, "wb") as out_file:
                pdf_writer.write(out_file)
            messagebox.showinfo("Success", "PDFs merged successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def split_pdf():
    file_path = filedialog.askopenfilename(title="Select a PDF", filetypes=[("PDF files", "*.pdf")])
    if not file_path:
        return

    try:
        pdf_reader = PyPDF2.PdfReader(file_path)
        total_pages = len(pdf_reader.pages)
        
        start_page = int(input("Enter the start page for the first split (1 to {}): ".format(total_pages)))
        end_page = int(input("Enter the end page for the first split ({} to {}): ".format(start_page, total_pages)))
        
        pdf_writer1 = PyPDF2.PdfWriter()
        pdf_writer2 = PyPDF2.PdfWriter()

        for page_num in range(start_page - 1, end_page):
            pdf_writer1.add_page(pdf_reader.pages[page_num])
        
        for page_num in range(end_page, total_pages):
            pdf_writer2.add_page(pdf_reader.pages[page_num])

        output_path1 = filedialog.asksaveasfilename(title="Save First Part", defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        output_path2 = filedialog.asksaveasfilename(title="Save Second Part", defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])

        if output_path1:
            with open(output_path1, "wb") as out_file:
                pdf_writer1.write(out_file)
        
        if output_path2:
            with open(output_path2, "wb") as out_file:
                pdf_writer2.write(out_file)

        messagebox.showinfo("Success", "PDF split successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def delete_pages_from_pdf():
    file_path = filedialog.askopenfilename(title="Select a PDF", filetypes=[("PDF files", "*.pdf")])
    if not file_path:
        return

    try:
        pdf_reader = PyPDF2.PdfReader(file_path)
        total_pages = len(pdf_reader.pages)

        pages_to_delete = input(f"Enter the page numbers to delete (1 to {total_pages}), separated by commas: ")
        pages_to_delete = [int(page.strip()) - 1 for page in pages_to_delete.split(",")]

        pdf_writer = PyPDF2.PdfWriter()
        for page_num in range(total_pages):
            if page_num not in pages_to_delete:
                pdf_writer.add_page(pdf_reader.pages[page_num])

        output_path = filedialog.asksaveasfilename(title="Save PDF", defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if output_path:
            with open(output_path, "wb") as out_file:
                pdf_writer.write(out_file)
            messagebox.showinfo("Success", "Pages deleted successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def pdf_to_jpg():
    file_path = filedialog.askopenfilename(title="Select a PDF", filetypes=[("PDF files", "*.pdf")])
    if not file_path:
        return

    try:
        pdf_document = fitz.open(file_path)
        output_dir = filedialog.askdirectory(title="Select Output Directory")
        if not output_dir:
            return

        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            pix = page.get_pixmap()
            output_path = f"{output_dir}/page_{page_num + 1}.jpg"
            pix.save(output_path)
        
        messagebox.showinfo("Success", "PDF pages have been converted to JPGs successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")


def create_gui():
    root = tk.Tk()
    root.title("PDF Utility")

    frame = tk.Frame(root, padx=10, pady=10)
    frame.pack(padx=10, pady=10)

    merge_button = tk.Button(frame, text="Merge PDFs", command=merge_pdfs)
    merge_button.pack(pady=5)

    split_button = tk.Button(frame, text="Split PDF", command=split_pdf)
    split_button.pack(pady=5)

    delete_button = tk.Button(frame, text="Delete Pages from PDF", command=delete_pages_from_pdf)
    delete_button.pack(pady=5)

    pdf_to_jpg_button = tk.Button(frame, text="PDF to JPG", command=pdf_to_jpg)
    pdf_to_jpg_button.pack(pady=5)

   

    root.mainloop()

if __name__ == "__main__":
    create_gui()
