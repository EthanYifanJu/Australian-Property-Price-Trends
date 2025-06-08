import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import json
import os

class DataProcessor:
    def __init__(self):
        self.measure = ""
        self.property_type = ""
        self.region = ""
        self.startPeriod = ""
        self.endPeriod = ""
        self.file_path = ""
        self.structures = ""

    def fetch_data(self, measure, property_type, region, startPeriod, endPeriod):
        # dataflowIdentifier String(path)
        # The dataflow identifier in {agencyId},{dataflowId},{version} format.
        dataFlowIdentifier = "ABS,RPPI"

        # dataKey String(path)
        '''
        The key to query data returned.
        Use "all" if you would like to return all data for the dataset.
        To filter data returned provide a data key, containing one or more coded values for each dimension, 
        separated by a dot (dimensions must be in the order they are defined in the data structure).

        Wildcarding is supported by omitting values for the dimension.
        The OR operator is supported using the + character. 
        You can combine wildcarding and the OR operator.
        '''

        '''
        Measure
        1: Index Nnumbers
        2: Percentage Change from Previous Period
        3: Percentage Change from Corresponding Quarter of the Previous Year
        '''
        self.measure = measure

        '''
        Property type
        1: Attached dwellings
        2: Established houses
        3: Residential property
        '''
        self.property_type = property_type

        '''
        Region
        3GBRI: Greater Brisbane
        2GMEL: Greater Melbourne
        6GHOB: Greater Hobart
        5GPER: Greater Perth
        4GADE: Greater Adelaide
        7GDAR: Greater Darwin
        1GSYD: Greater Sydney
        8ACTE: Australian Capital Territory
        100: Weighted average of eight capital cities

        BELOW ENTRIES ARE NOT USED. ONLY INDECATING WHICH STATE THE CAPITAL CITY BELONGS TO.
        3: Queensland
        AUS: Australia
        2: Victoria
        6: Tasmania
        5: Western Australia
        4: South Australia
        7: Northern Territory
        1: New South Wales
        8: Australian Capital Territory
        '''
        self.region = region

        '''
        Frequency
        Q: Quarterly
        '''
        frequency = "Q"

        dataKey = self.measure + "." + self.property_type + "." + self.region + "." + frequency

        '''
        startPeriod & endPeriod
        string(query)

        The start period and end period (used to filter on time). This is inclusive. The value can be in the following formats:

        year: yyyy
        year-quarter: yyyy-Q1 - yyyy-Q4
        '''
        self.startPeriod = startPeriod
        self.endPeriod = endPeriod

        file_name = f"{self.measure}.{self.property_type}.{self.region}.{self.startPeriod}.{self.endPeriod}.json"
        self.file_path = f"./src/data/{file_name}"


        if os.path.exists(self.file_path):
            print(f"File already exists: {self.file_path}. Skipping download.")
            return

        url = "https://data.api.abs.gov.au/rest/data/" + dataFlowIdentifier + "/" + dataKey + "?format=jsondata"
        if self.startPeriod:
            url += "&startPeriod=" + self.startPeriod
        if self.endPeriod:
            url += "&endPeriod=" + self.endPeriod
        # print(url)
        response = requests.get(url)
        data = response.json()

        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)

        print(f"Data saved to data folder")

    def process_data(self):
        with open(self.file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Extract structures
        self.structures = data['data']['structures'][0]
        series_dimensions = self.structures['dimensions']['series']
        observation_dimensions = self.structures['dimensions']['observation']

        # Create mappings for dimension indices to their labels
        dimension_maps = {}
        for dim in series_dimensions:
            dim_id = dim['id']
            values = dim['values']
            dimension_maps[dim_id] = {str(id): value['name'] for id, value in enumerate(values)}

        # Map observation indices to time periods
        time_periods = [value['id'] for value in observation_dimensions[0]['values']]

        # Process series data
        records = []
        series_data = data['data']['dataSets'][0]['series']
        for series_key, series_value in series_data.items():
            # Split the series key to get dimension indices
            indices = series_key.split(':')
            series_info = {}
            for i, dim in enumerate(series_dimensions):
                dim_id = dim['id']
                index = indices[i]
                series_info[dim_id] = dimension_maps[dim_id][index]
            
            # Extract observations
            observations = series_value['observations']
            for obs_index, obs_value in observations.items():
                record = series_info.copy()
                record['TIME_PERIOD'] = time_periods[int(obs_index)]
                record['OBS_VALUE'] = obs_value[0]
                records.append(record)
        return records

    def visualise_data(self, records):
        # Create a DataFrame
        df = pd.DataFrame(records)
        # Create a new column combining 'REGION' and 'PROPERTY_TYPE'
        df['REGION_PROPERTY'] = df['REGION'] + ' - ' + df['PROPERTY_TYPE']

        fig = px.line(df, x='TIME_PERIOD', y='OBS_VALUE', color='REGION_PROPERTY',
                      title=df['MEASURE'].iloc[0],
                      labels={"OBS_VALUE": self.structures['attributes']['series'][0]['values'][0]['name']})
        fig.update_layout(autosize=True)
        return fig.to_html(full_html=False)
    
        # hue_order = sorted(df['REGION_PROPERTY'].unique())
        # # Plot
        # plt.figure(figsize=(10, 6))
        # sns.lineplot(data=df, x='TIME_PERIOD', y='OBS_VALUE', hue='REGION_PROPERTY', hue_order=hue_order)
        # plt.title(df['MEASURE'][0])
        # plt.xlabel('Time Period')
        # plt.ylabel(self.structures['attributes']['series'][0]['values'][0]['name'])
        # plt.legend(title='Region-Property type')
        # plt.tight_layout()
        # plt.show()

# dp = DataProcessor()
# dp.fetch_data(measure="1", property_type="1", region="1GSYD", startPeriod="2015-Q1", endPeriod="2020-Q4")
# records = dp.process_data()
# dp.visualise_data(records)