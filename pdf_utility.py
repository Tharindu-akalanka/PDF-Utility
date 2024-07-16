import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import PyPDF2
import fitz  # PyMuPDF

# Define colors for dark theme
BG_COLOR = "#1e1e1e"  # Background color
FG_COLOR = "#ffffff"  # Text color
BUTTON_BG = "#333333"  # Button background color
BUTTON_FG = "#ffffff"  # Button text color

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
        
        # Ask for start page number in a popup window
        start_page_str = simpledialog.askstring("Split PDF", f"Enter the start page (1 to {total_pages}):")
        if not start_page_str:
            return
        start_page = int(start_page_str)

        # Ask for end page number in a popup window and lift it to the top
        end_page_str = simpledialog.askstring("Split PDF", f"Enter the end page ({start_page} to {total_pages}):")
        if not end_page_str:
            return
        end_page = int(end_page_str)
        
        root.lift()

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

        # Ask for page numbers to delete in a popup window
        pages_to_delete_str = simpledialog.askstring("Delete Pages", f"Enter the page numbers to delete (1 to {total_pages}), separated by commas:")
        if not pages_to_delete_str:
            return

        pages_to_delete = [int(page.strip()) - 1 for page in pages_to_delete_str.split(",")]

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

    # Centering the window on screen
    window_width = 400
    window_height = 300
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # Set dark theme for window
    root.configure(bg=BG_COLOR)
    root.option_add("*Font", "Helvetica")
    root.option_add("*Background", BG_COLOR)
    root.option_add("*Foreground", FG_COLOR)

    # Frame for buttons
    frame = tk.Frame(root, padx=10, pady=10, bg=BG_COLOR)
    frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    # Button styles
    button_style = {"font": ("Helvetica", 12), "padx": 20, "pady": 10, "bd": 2, "bg": BUTTON_BG, "fg": BUTTON_FG}

    # Buttons
    merge_button = tk.Button(frame, text="Merge PDFs", command=merge_pdfs, **button_style)
    merge_button.pack(pady=5, fill=tk.X)

    split_button = tk.Button(frame, text="Split PDF", command=split_pdf, **button_style)
    split_button.pack(pady=5, fill=tk.X)

    delete_button = tk.Button(frame, text="Delete Pages from PDF", command=delete_pages_from_pdf, **button_style)
    delete_button.pack(pady=5, fill=tk.X)

    pdf_to_jpg_button = tk.Button(frame, text="PDF to JPG", command=pdf_to_jpg, **button_style)
    pdf_to_jpg_button.pack(pady=5, fill=tk.X)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
