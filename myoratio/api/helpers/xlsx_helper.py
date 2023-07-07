import xlsxwriter


class XLSXHelper:
    @staticmethod
    def get_cell_formats(workbook: xlsxwriter.Workbook) -> dict:
        center = workbook.add_format(None)
        center.set_align("center")
        bold = workbook.add_format({"bold": True})
        header = workbook.add_format({"bold": True})
        header.set_align("center")
        number = workbook.add_format({"num_format": "0.000000"})
        number.set_align("center")
        number_short = workbook.add_format({"num_format": "0.00"})
        number_short.set_align("center")
        sci_number = workbook.add_format({"num_format": "##0.000E+00"})
        sci_number.set_align("center")

        return {
            "center": center,
            "bold": bold,
            "header": header,
            "number": number,
            "number_short": number_short,
            "sci_number": sci_number,
        }
