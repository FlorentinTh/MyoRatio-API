from xhtml2pdf import pisa


class PDFHelper:
    @staticmethod
    def generate_pdf_from_html(html_path, output_path):
        input_file = open(html_path, 'r+b')
        output_file = open(output_path, "w+b")
        pisa.CreatePDF(input_file, dest=output_file)
        output_file.close()
