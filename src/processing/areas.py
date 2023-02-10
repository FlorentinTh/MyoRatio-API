import pandas as pd

from scipy import integrate


class Areas:
    def __init__(self, data_path: str, csv_files: list[str]):
        self._data_path = data_path
        self._dataframes = []

        for csv_file in csv_files:
            try:
                dataframe = pd.read_csv(csv_file, sep='\t', encoding='utf-8', engine='c')
                dataframe.set_index(dataframe.columns[0], inplace=True)
                self._dataframes.append(dataframe)
            except pd.errors.ParserError as error:
                raise pd.errors.ParserError(error)

    @staticmethod
    def _compute_area(data: pd.DataFrame) -> pd.DataFrame:
        area_all_emg_data = pd.DataFrame()

        for i, column in enumerate(data):
            area_emg_column_data = integrate.trapz(data[column].to_numpy())
            area_all_emg_data[data[column].name] = pd.Series(area_emg_column_data)

        return area_all_emg_data

    def start_processing(self) -> dict:
        mean_normalized_envelope_all_emg_data = pd.concat(self._dataframes).groupby(level=0).mean()
        area_mean_all_emg_data = self._compute_area(mean_normalized_envelope_all_emg_data)

        areas = {}

        for i in range(len(self._dataframes)):
            iteration_area_data = self._compute_area(self._dataframes[i])
            areas[f'iteration_{i}'] = iteration_area_data.to_dict(orient='records')[0]

        areas['mean'] = area_mean_all_emg_data.to_dict(orient='records')[0]

        return areas



