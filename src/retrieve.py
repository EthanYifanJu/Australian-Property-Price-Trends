import requests
import pandas as pd
import matplotlib.pyplot as plt

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
measure = "2"

'''
Property type
1: Attached dwellings
2: Established houses
3: Residential property
'''
property_type = "1"

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
region = "3GBRI"

'''
Frequency
Q: Quarterly
'''
frequency = "Q"

dataKey = measure + "." + property_type + "." + region + "." + frequency

'''
startPeriod & endPeriod
string(query)

The start period and end period (used to filter on time). This is inclusive. The value can be in the following formats:

year: yyyy
year-quarter: yyyy-Q1 - yyyy-Q4
'''
startPeriod = "2015-Q3"
endPeriod = "2015-Q4"
url = "https://data.api.abs.gov.au/rest/data/" + dataFlowIdentifier + "/" + dataKey + "?format=jsondata"
if startPeriod != "":
    url += "&startPeriod=" + startPeriod
if endPeriod != "":
    url += "&endPeriod=" + endPeriod
print(url)
response = requests.get(url)
data = response.json()

# Extract the data records
records = data['data']
# Convert the list of records into a DataFrame
df = pd.DataFrame(records)
print(df)