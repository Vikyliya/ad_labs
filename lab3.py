from spyre import server
import pandas as pd
import matplotlib.pyplot as plt
import math

class StockExample(server.App):
    title = "NOAA data vizualization"

    inputs = [
        {
            "type": "dropdown",
            "label": "NOAA data dropdown",
            "options": [
                {"label": "VCI", "value": "VCI"},
                {"label": "TCI", "value": "TCI"},
                {"label": "VHI", "value": "VHI"}],
            "key": "data_type",
            "action_id": "update_data"},
        
        {
            "type": "dropdown",
            "label": "Region dropdown",
            "options": [
                {"label": "Вінницька", "value": "1"},
                {"label": "Волинська", "value": "2"},
                {"label": "Дніпропетровська", "value": "3"},
                {"label": "Донецька", "value": "4"},
                {"label": "Житомирська", "value": "5"},
                {"label": "Закарпатська", "value": "6"},
                {"label": "Запорізька", "value": "7"},
                {"label": "Івано-Франківська", "value": "8"},
                {"label": "Київська", "value": "9"},
                {"label": "Кіровоградська", "value": "10"},
                {"label": "Луганська", "value": "11"},
                {"label": "Львівська", "value": "12"},
                {"label": "Миколаївська", "value": "13"},
                {"label": "Одеська", "value": "14"},
                {"label": "Полтавська", "value": "15"},
                {"label": "Рівенська", "value": "16"},
                {"label": "Сумська", "value": "17"},
                {"label": "Тернопільська", "value": "18"},
                {"label": "Харківська", "value": "19"},
                {"label": "Херсонська", "value": "20"},
                {"label": "Хмельницька", "value": "21"},
                {"label": "Черкаська", "value": "22"},
                {"label": "Чернівецька", "value": "23"},
                {"label": "Чернігівська", "value": "24"},
                {"label": "Крим", "value": "25"},
                {"label": "Київ", "value": "26"},
                {"label": "Севастополь", "value": "27"}],
            "key": "region",
            "action_id": "update_data"},
        
        {
            "type": "text",
            "label": "Select range:",
            "key": "range",
            "value": "9-10",
            "action_id": "update_data"},
        
        {
            "type":'slider',
            "label": 'Select year:',
            "min" : 1981,
            "max" : 2023,
            "key": 'year',
            "action_id" : "update_data"}]

    controls = [{"type": "hidden", "id": "update_data"}]

    tabs = ["Plot", "Table"]

    outputs = [ { "type": "plot",
                    "id": "plot",
                    "control_id": "update_data",
                    "tab": "Plot"},
                { "type": "table",
                    "id": "table_id",
                    "control_id": "update_data",
                    "tab": "Table",
                    "on_page_load": True}]

    def g_Table(self, params):
        data_region = params['region']
        data_range = params['range']
        data_year = params['year']

        df = pd.read_csv('combined_data.csv')
        df = df[df['area'] == int(data_region)]
        start_week, end_week = map(int, data_range.split('-'))
        df = df[(df['Week'] >= start_week) & (df['Week'] <= end_week) & (df['Year'] == int(data_year))]

        return df[['Year', 'Week', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI']]

    def Data_Region_List(self, data_region):
        region_list = {
            "1": "Вінничини",
            "2": "Волині",
            "3": "Дніпропетровщини",
            "4": "Донеччини",
            "5": "Житомирщини",
            "6": "Закарпаття",
            "7": "Запоріжжя",
            "8": "Івано-Франківщини",
            "9": "Київщини",
            "10": "Кіровоградщини",
            "11": "Луганщини",
            "12": "Львівщини",
            "13": "Миколаївщини",
            "14": "Одещини",
            "15": "Полтавщини",
            "16": "Рівенщини",
            "17": "Сумщини",
            "18": "Тернопільщини",
            "19": "Харківщини",
            "20": "Херсонщини",
            "21": "Хмельницька",
            "22": "Черкащини",
            "23": "Чернівецька",
            "24": "Чернігівщини",
            "25": "Криму"
        }
        return region_list.get(data_region, "")


    def g_Plot(self, params):
        df = self.getData(params)
        data_type = params['data_type']
        y_label = data_type
        data_year = params['year']
        data_region = params['region']
        region_name = self.Data_Region_List(data_region)
        data_range = params['range']
        start_week, end_week = map(int, data_range.split('-'))

        year_int = int(data_year)
        year_decimal = math.modf(float(data_year))[0]
        if year_decimal == 0.0:
            year_str = f"{year_int} рік"

        fig, ax = plt.subplots()
        df.plot(x='Week', y=data_type, legend=False, ax=ax)
        ax.set_ylabel(y_label)
        ax.set_xlabel("Тижні")
        ax.set_title(f"{data_type} графік для {region_name}, {year_str}, {start_week}-{end_week} тижні")

        return fig

    def getHTML(self, params):
        df = self.getData(params)
        return df.to_html()

app = StockExample()
app.launch(port=2020)