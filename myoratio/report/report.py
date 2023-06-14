import os
from enum import Enum

import pandas as pd
import xlsxwriter
from xlsxwriter.utility import xl_col_to_name

from myoratio.angles import Angles
from myoratio.api import Constants
from myoratio.api.helpers import PathHelper, StringHelper
from myoratio.areas import Areas
from myoratio.data.emg import EMG, NormalizationOptions
from myoratio.results import Ratio, Results
from myoratio.task import Analysis, Stage


class Stats(Enum):
    MEAN = "Average"
    STDEV = "Standard deviation"
    COVAR = "Coefficient of variation"


class ChartType(Enum):
    AREA = "area"
    LINE = "line"


class Report:
    def __init__(
        self, data_path: str, analysis: str, stage: str, participant: tuple[str, dict]
    ) -> None:
        self._data_path = data_path

        if analysis in [analysis.value for analysis in Analysis]:
            self._analysis = analysis
        else:
            raise ValueError(f"Expected a value from Analysis, but got {analysis}")

        if stage in [stage.value for stage in Stage]:
            self._stage = stage
        else:
            raise ValueError(f"Expected a value from Stage, but got {stage}")

        stage_folder_name = self._stage

        if self._analysis == Analysis.SIT_STAND.value:
            if self._stage == Stage.CONCENTRIC.value:
                stage_folder_name = "standing"
            else:
                stage_folder_name = "sitting"

        output_base_path = os.path.join(
            self._data_path, "Results", self._analysis, stage_folder_name
        )

        self._participant = participant

        self._workbook = xlsxwriter.Workbook(
            os.path.join(
                output_base_path,
                f"report_{self._analysis}_{stage_folder_name}_{self._participant[0]}.xlsx",
            )
        )

        self._data_worksheet = self._workbook.add_worksheet("data")
        self._report_worksheet = self._workbook.add_worksheet("report")
        self._chart_worksheet = self._workbook.add_worksheet("chart")

        bold = self._workbook.add_format({"bold": True})
        header = self._workbook.add_format({"bold": True})
        header.set_align("center")
        number = self._workbook.add_format({"num_format": "0.000000"})
        number.set_align("center")
        number_short = self._workbook.add_format({"num_format": "0.00"})
        number_short.set_align("center")
        sci_number = self._workbook.add_format({"num_format": "##0.000E+00"})
        sci_number.set_align("center")

        self._formats = {
            "bold": bold,
            "header": header,
            "number": number,
            "number_short": number_short,
            "sci_number": sci_number,
        }

    def _write_stats_table(
        self, start_at_row: int, metadata_angles: list[dict[str, dict[str, float]]]
    ) -> tuple[float, float, int]:
        headings = [
            "",
            "Start time (s)",
            "Stop time (s)",
            "Duration (s)",
            "Start angle (°)",
            "Stop angle (°)",
            "Amplitude (°)",
            "Angular velocity (°/s)",
        ]

        self._report_worksheet.write_row("A1", headings, self._formats["header"])

        start_row = start_at_row
        stop_row = start_row + len(metadata_angles)

        sum_start_times = 0
        sum_stop_times = 0

        for i, metadata_angle in enumerate(metadata_angles):
            self._report_worksheet.write(
                f"A{i + 2}", f"Iteration {i + 1}", self._formats["bold"]
            )

            start_time = metadata_angle["0"]["x"]
            sum_start_times += start_time

            self._report_worksheet.write(f"B{i + 2}", start_time, self._formats["number"])

            stop_time = metadata_angle["1"]["x"]
            sum_stop_times += stop_time

            self._report_worksheet.write(f"C{i + 2}", stop_time, self._formats["number"])
            self._report_worksheet.write_formula(
                f"D{i + 2}", f"=C{i + 2}-B{i + 2}", self._formats["number"]
            )
            self._report_worksheet.write(
                f"E{i + 2}", metadata_angle["0"]["y"], self._formats["number"]
            )
            self._report_worksheet.write(
                f"F{i + 2}", metadata_angle["1"]["y"], self._formats["number"]
            )
            self._report_worksheet.write_formula(
                f"G{i + 2}", f"=E{i + 2}-F{i + 2}", self._formats["number"]
            )
            self._report_worksheet.write_formula(
                f"H{i + 2}", f"=G{i + 2}/D{i + 2}", self._formats["number"]
            )

        mean_start_time = sum_start_times / len(metadata_angles)
        mean_stop_time = sum_stop_times / len(metadata_angles)
        total_mean_time = mean_stop_time - mean_start_time
        time_interval = total_mean_time / (NormalizationOptions.LENGTH.value - 1)

        self._report_worksheet.write(
            f"A{len(metadata_angles) + 2}", Stats.MEAN.value, self._formats["bold"]
        )
        self._report_worksheet.write(
            f"A{len(metadata_angles) + 3}", Stats.STDEV.value, self._formats["bold"]
        )
        self._report_worksheet.write(
            f"A{len(metadata_angles) + 4}", Stats.COVAR.value, self._formats["bold"]
        )

        for i in range(len(headings) - 1):
            col = xl_col_to_name(i + 1)
            mean_row = len(metadata_angles) + 1
            stddev_row = len(metadata_angles) + 2

            self._report_worksheet.write_formula(
                mean_row,
                i + 1,
                f"=AVERAGE({col}{start_row}:{col}{stop_row - 1})",
                self._formats["number"],
            )

            self._report_worksheet.write_formula(
                stddev_row,
                i + 1,
                f"=STDEV({col}{start_row}:{col}{stop_row - 1})",
                self._formats["number"],
            )

            self._report_worksheet.write_formula(
                len(metadata_angles) + 3,
                i + 1,
                f"=({col}{stddev_row + 1}/{col}{mean_row + 1})*100",
                self._formats["number"],
            )

        stop_at_row = len(metadata_angles) + 5

        return mean_start_time, time_interval, stop_at_row

    def _write_data_worksheet(
        self, emg: EMG, angles: Angles, start_time: float, interval: float
    ) -> None:
        time_heading = ["Time"]
        mean_envelopes = emg.get_mean_envelopes()
        self._data_headings = time_heading + list(mean_envelopes.iloc[0].index)
        self._data_headings.append("Angles")
        self._data_worksheet.write_row("A1", self._data_headings, self._formats["header"])

        time = start_time

        for i in range(NormalizationOptions.LENGTH.value):
            self._data_worksheet.write(f"A{i + 2}", time, self._formats["number"])
            time += interval

        for i, column in enumerate(mean_envelopes):
            self._data_worksheet.write_column(
                1, i + 1, mean_envelopes[column], self._formats["sci_number"]
            )

        mean_angles = angles.get_mean_angles_data(self._stage)
        self._data_worksheet.write_column(
            1,
            len(mean_envelopes.columns) + 1,
            mean_angles.iloc[:, 0],
            self._formats["number"],
        )

    def _write_areas_table(self, start_at_row: int, areas: Areas) -> int:
        all_areas = areas.get_areas()
        start_row = start_at_row
        stop_row = start_row + len(all_areas.columns)

        self._report_worksheet.write(f"A{start_row}", "Areas", self._formats["bold"])

        for i in range(len(all_areas.columns)):
            if i < len(all_areas.columns) - 1:
                self._report_worksheet.write(
                    f"A{start_row + i + 2}", f"Iteration {i + 1}", self._formats["bold"]
                )

        for i, row in all_areas.iterrows():
            row_index = all_areas.index.get_loc(i)
            self._report_worksheet.write(
                start_row, row_index + 1, i, self._formats["header"]
            )
            self._report_worksheet.write_column(
                start_row + 1, row_index + 1, row[:-1], self._formats["number"]
            )

        self._report_worksheet.write(
            f"A{start_row + len(all_areas.columns) + 1}",
            Stats.MEAN.value,
            self._formats["bold"],
        )
        self._report_worksheet.write(
            f"A{start_row + len(all_areas.columns) + 2}",
            Stats.STDEV.value,
            self._formats["bold"],
        )
        self._report_worksheet.write(
            f"A{start_row + len(all_areas.columns) + 3}",
            Stats.COVAR.value,
            self._formats["bold"],
        )

        for i in range(len(all_areas)):
            col = xl_col_to_name(i + 1)
            mean_row = start_row + len(all_areas.columns)
            stddev_row = start_row + len(all_areas.columns) + 1

            self._report_worksheet.write_formula(
                mean_row,
                i + 1,
                f"=AVERAGE({col}{start_row + 2}:{col}{stop_row})",
                self._formats["number"],
            )

            self._report_worksheet.write_formula(
                stddev_row,
                i + 1,
                f"=STDEV({col}{start_row + 2}:{col}{stop_row})",
                self._formats["number"],
            )

            self._report_worksheet.write_formula(
                start_row + len(all_areas.columns) + 2,
                i + 1,
                f"=({col}{stddev_row + 1}/{col}{mean_row + 1})*100",
                self._formats["number"],
            )

        stop_at_row = start_row + len(all_areas.columns) + 4
        return stop_at_row

    def _write_ratios_matrices(
        self, start_at_row: int, ratios: pd.DataFrame
    ) -> tuple[int, list[tuple]]:
        ratios = ratios.iloc[:, 1:]

        start_row = start_at_row

        ratio = Ratio(self._analysis, self._stage)
        antagonist, agonist = ratio.get_muscles()

        ratios_of_interest = []

        self._report_worksheet.write(
            f"A{start_row}", "Ratio matrices", self._formats["bold"]
        )

        for i in range(len(ratios.columns)):
            label = (
                f"Iteration {i + 1}" if i < len(ratios.columns) - 1 else "Average ratios"
            )

            self._report_worksheet.write(start_row + 1, 0, label, self._formats["bold"])

            antagonist_column = None
            agonist_column = None

            for j, row in ratios.iterrows():
                if agonist is not None and antagonist is not None:
                    if antagonist_column is None or agonist_column is None:
                        if StringHelper.include_substring(row[i]["muscle"], antagonist):
                            antagonist_column = j + 2  # type: ignore

                        if StringHelper.include_substring(row[i]["muscle"], agonist):
                            agonist_column = start_row + j + 2  # type: ignore
                else:
                    raise ValueError("antagonist and agonist cannot be None")

                self._report_worksheet.write(
                    start_row + j + 2, 1, row[i]["muscle"], self._formats["bold"]  # type: ignore
                )

                self._report_worksheet.write(
                    start_row + 1, j + 2, row[i]["muscle"], self._formats["header"]  # type: ignore
                )

                self._report_worksheet.write_row(
                    start_row + j + 2, 2, row[i]["values"], self._formats["number_short"]  # type: ignore
                )

            if antagonist_column is not None and agonist_column is not None:
                ratios_of_interest.append((antagonist_column, agonist_column))  # type: ignore
            else:
                raise ValueError("antagonist_column and agonist_column cannot be None")

            start_row += len(ratios) + 2

        return start_row, ratios_of_interest

    def _write_ratios_table(self, start_at_row: int, ratios: list[tuple]) -> None:
        start_row = start_at_row

        antagonist = None
        agonist = None

        ratio = Ratio(self._analysis, self._stage)
        antagonist, agonist = ratio.get_muscles()

        self._report_worksheet.write(
            start_row, 0, f"Antagonist / Agonist Ratios", self._formats["bold"]
        )

        self._report_worksheet.write(
            start_row, 1, f"{antagonist} / {agonist}", self._formats["bold"]
        )

        start_row += 1

        for i in range(len(ratios) - 1):
            self._report_worksheet.write(
                start_row + i, 0, f"Iteration {i + 1}", self._formats["bold"]
            )

            self._report_worksheet.write_formula(
                start_row + i,
                1,
                f"={xl_col_to_name(ratios[i][0])}{ratios[i][1] + 1}",
                self._formats["number_short"],
            )

        self._report_worksheet.write(
            start_row + len(ratios) - 1, 0, Stats.MEAN.value, self._formats["bold"]
        )

        self._report_worksheet.write_formula(
            start_row + len(ratios) - 1,
            1,
            f"=AVERAGE(B{start_row + 1}:B{start_row + len(ratios) - 1})",
            self._formats["number"],
        )

        self._report_worksheet.write(
            start_row + len(ratios), 0, Stats.STDEV.value, self._formats["bold"]
        )

        self._report_worksheet.write_formula(
            start_row + len(ratios),
            1,
            f"=STDEV(B{start_row + 1}:B{start_row + len(ratios) - 1})",
            self._formats["number"],
        )

        self._report_worksheet.write(
            start_row + len(ratios) + 1, 0, Stats.COVAR.value, self._formats["bold"]
        )

        self._report_worksheet.write_formula(
            start_row + len(ratios) + 1,
            1,
            f"=(B{start_row + len(ratios) + 1}/B{start_row + len(ratios)})*100",
            self._formats["number"],
        )

    def _insert_chart(self, chart_type: str, offset: int) -> None:
        if chart_type not in [chart_type.value for chart_type in ChartType]:
            raise ValueError(f"Expected a value from ChartType, but got {chart_type}")

        if self._data_headings is not None:
            ratio = Ratio(self._analysis, self._stage)
            antagonist, agonist = ratio.get_muscles()

            antagonist_index = None
            agonist_index = None
            time_index = 0
            angle_index = len(self._data_headings) - 1

            if antagonist is not None and agonist is not None:
                for i in range(len(self._data_headings)):
                    if StringHelper.include_substring(self._data_headings[i], antagonist):
                        antagonist_index = i
                    elif StringHelper.include_substring(self._data_headings[i], agonist):
                        agonist_index = i

                if chart_type == ChartType.AREA.value:
                    chart_options = {
                        "type": "area",
                        "subtype": None,
                        "border": {"color": "black"},
                    }
                else:
                    chart_options = {"type": "line", "border": {"color": "black"}}

                muscle_chart = self._workbook.add_chart(chart_options)
                muscle_chart.set_size({"width": 900, "height": 600})
                muscle_chart.set_legend(
                    {"position": "bottom", "border": {"color": "black"}}
                )

                if (
                    self._stage == Stage.CONCENTRIC.value
                    and self._analysis != Analysis.FLEXION.value
                ) or (
                    self._stage == Stage.ECCENTRIC.value
                    and self._analysis == Analysis.FLEXION.value
                ):
                    muscle_chart.add_series(
                        {
                            "name": f"=data!${xl_col_to_name(antagonist_index)}$1",
                            "categories": f"=data!${xl_col_to_name(time_index)}$2:${xl_col_to_name(time_index)}${NormalizationOptions.LENGTH.value + 1}",
                            "values": f"=data!${xl_col_to_name(antagonist_index)}$2:${xl_col_to_name(antagonist_index)}${NormalizationOptions.LENGTH.value + 1}",
                        }
                    )

                    muscle_chart.add_series(
                        {
                            "name": f"=data!${xl_col_to_name(agonist_index)}$1",
                            "categories": f"=data!${xl_col_to_name(time_index)}$2:${xl_col_to_name(time_index)}${NormalizationOptions.LENGTH.value + 1}",
                            "values": f"=data!${xl_col_to_name(agonist_index)}$2:${xl_col_to_name(agonist_index)}${NormalizationOptions.LENGTH.value + 1}",
                        }
                    )
                else:
                    muscle_chart.add_series(
                        {
                            "name": f"=data!${xl_col_to_name(agonist_index)}$1",
                            "categories": f"=data!${xl_col_to_name(time_index)}$2:${xl_col_to_name(time_index)}${NormalizationOptions.LENGTH.value + 1}",
                            "values": f"=data!${xl_col_to_name(agonist_index)}$2:${xl_col_to_name(agonist_index)}${NormalizationOptions.LENGTH.value + 1}",
                        }
                    )

                    muscle_chart.add_series(
                        {
                            "name": f"=data!${xl_col_to_name(antagonist_index)}$1",
                            "categories": f"=data!${xl_col_to_name(time_index)}$2:${xl_col_to_name(time_index)}${NormalizationOptions.LENGTH.value + 1}",
                            "values": f"=data!${xl_col_to_name(antagonist_index)}$2:${xl_col_to_name(antagonist_index)}${NormalizationOptions.LENGTH.value + 1}",
                        }
                    )

                angle_chart = self._workbook.add_chart({"type": "line"})

                angle_chart.add_series(
                    {
                        "name": f"=data!${xl_col_to_name(angle_index)}$1",
                        "categories": f"=data!${xl_col_to_name(time_index)}$2:${xl_col_to_name(time_index)}${NormalizationOptions.LENGTH.value + 1}",
                        "values": f"==data!${xl_col_to_name(angle_index)}$2:${xl_col_to_name(angle_index)}${NormalizationOptions.LENGTH.value + 1}",
                        "y2_axis": True,
                    }
                )

                muscle_chart.combine(angle_chart)

                muscle_chart.set_x_axis({"name": "Time (s)"})
                muscle_chart.set_y_axis({"name": "Activation"})
                angle_chart.set_y2_axis({"name": "Angle (°)"})

                y_offset = offset + 10 if offset == 0 else offset + 50

                self._chart_worksheet.insert_chart(
                    "D2", muscle_chart, {"x_offset": 25, "y_offset": y_offset}
                )

    def generate_XLSX_report(self) -> None:
        participant_metadata_folder_path = os.path.join(
            PathHelper.get_metadata_analysis_path(self._data_path, self._analysis),
            StringHelper.format_participant_name_as_folder_name(self._participant[0]),
        )

        areas = Areas(participant_metadata_folder_path, self._stage)
        angles = Angles(participant_metadata_folder_path)
        emg = EMG(participant_metadata_folder_path, self._stage)

        metadata_angles = angles.get_angles_from_metadata(self._stage)

        stats_table_start_row = Constants.XSLX_TABLE_SPACES.value

        start_time, interval, stats_table_end_row = self._write_stats_table(
            stats_table_start_row, metadata_angles
        )

        self._write_data_worksheet(emg, angles, start_time, interval)

        areas_table_start_row = stats_table_end_row + Constants.XSLX_TABLE_SPACES.value
        areas_table_end_row = self._write_areas_table(areas_table_start_row, areas)

        ratios_matrices_start_row = (
            areas_table_end_row + Constants.XSLX_TABLE_SPACES.value
        )
        results = Results()
        ratios = results.get_ratios(participant_metadata_folder_path, self._stage)
        ratios_matrices_stop_row, ratios_of_interest = self._write_ratios_matrices(
            ratios_matrices_start_row, ratios
        )

        ratios_table_start_row = (
            ratios_matrices_stop_row + Constants.XSLX_TABLE_SPACES.value
        )
        self._write_ratios_table(ratios_table_start_row, ratios_of_interest)

        self._insert_chart(ChartType.AREA.value, 0)
        self._insert_chart(ChartType.LINE.value, 600)

        self._data_worksheet.autofit()
        self._report_worksheet.autofit()

        self._workbook.close()
