import os

import pandas as pd
from matplotlib import pyplot as plt

from .path_helper import PathHelper


class PlotHelper:
    def __init__(self, csv_path: tuple[str, str], data: pd.DataFrame):
        self._csv_path = csv_path
        self._data = data

    def build_plot(self, legend: str, x_label: str, y_label: str) -> None:
        plt.figure(facecolor="#ededed")
        axes = plt.gca()
        axes.set_facecolor("#ededed")
        plt.setp(axes.spines.values(), color="#d5d5d5")
        plt.plot(self._data, "#16A085", label=legend)
        plt.xlabel(
            x_label,
            fontdict={"family": "sans-serif", "weight": "bold", "color": "#16A085"},
        )
        plt.legend(
            facecolor="#ededed",
            edgecolor="#575757",
            loc=4,
            labelcolor="#575757",
            prop={"size": 12, "family": "sans-serif"},
        )
        plt.ylabel(
            y_label,
            fontdict={"family": "sans-serif", "weight": "bold", "color": "#16A085"},
        )
        plt.grid(color="#d5d5d5")
        axes.tick_params(axis="x", colors="#575757", labelsize=12)
        axes.tick_params(axis="y", colors="#575757", labelsize=12)
        axes.tick_params(color="#d5d5d5", which="both")

    def save_plot(self, base_path: str, prefix: str = "") -> None:
        if bool(prefix and prefix.isspace()) is True:
            filename = os.path.splitext(self._csv_path[1])[0] + ".png"
        else:
            filename = f"{prefix}_" + os.path.splitext(self._csv_path[1])[0] + ".png"

        split_path = self._csv_path[0].split(os.sep)
        analysis = split_path[len(split_path) - 2]
        participant = split_path[len(split_path) - 1]

        plot_path = os.path.join(
            PathHelper.get_analysis_folder_path(base_path, analysis),
            participant,
            filename,
        )

        plt.savefig(plot_path)
        plt.close()
