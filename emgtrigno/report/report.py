import os
from datetime import datetime
from typing import Optional

import xlsxwriter
from jinja2 import Template
from xhtml2pdf import pisa

from emgtrigno.api.helpers import FileHelper, JSONHelper, PathHelper
from emgtrigno.task import Analysis


class Report:
    def __init__(
        self, report_template_path: Optional[str], data_path: str, analysis: str
    ) -> None:
        self._report_template_path = report_template_path
        self._data_path = data_path

        if analysis in [analysis.value for analysis in Analysis]:
            self._analysis = analysis
        else:
            raise ValueError(f"Expected a value from ResponseStatus, but got {analysis}")

    def _get_participants_metadata(self) -> list:
        return JSONHelper.read_participants_metadata(
            FileHelper.get_metadata_analysis_path(self._data_path, self._analysis)
        )

    def _create_HTML_report_file(self, content: dict) -> str:
        if self._report_template_path is not None:
            with open(self._report_template_path, mode="r", encoding="utf-8") as file:
                template_string = file.read()
        else:
            raise ValueError(f"Template path must be provided")

        file.close()

        template = Template(template_string, autoescape=True)
        html_content = template.render(content)

        html_output_path = os.path.join(
            FileHelper.get_metadata_analysis_path(self._data_path, self._analysis),
            f"{self._analysis}_report.html",
        )

        with open(html_output_path, mode="w", encoding="utf-8") as results:
            results.write(html_content)

        results.close()

        return html_output_path

    def generate_PDF_report(self) -> None:
        participants = self._get_participants_metadata()

        ##
        ## TODO: complete pdf report according to provided template
        ##

        content = {
            "analysis": self._analysis,
            "participants": participants,
            "date_time": datetime.now().strftime("%Y-%m-%d %H:%M"),
        }

        html_file_path = self._create_HTML_report_file(content)

        output_path = os.path.join(
            FileHelper.get_analysis_base_folder_path(self._data_path),
            f"{self._analysis}_report.pdf",
        )

        input_file = open(html_file_path, "r+b")
        output_file = open(output_path, "w+b")

        pisa.CreatePDF(input_file, dest=output_file)

        output_file.close()
        input_file.close()

    def generate_XLSX_report(self) -> None:
        participants = self._get_participants_metadata()

        output_path = os.path.join(
            FileHelper.get_analysis_base_folder_path(self._data_path),
            f"{self._analysis}_report.xlsx",
        )

        workbook = xlsxwriter.Workbook(output_path)

        for participant in participants:
            worksheet = workbook.add_worksheet(participant[0])

            ##
            ## TODO: complete xlsx report according to provided template
            ##

        workbook.close()
