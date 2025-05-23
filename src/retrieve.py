import requests
import pandas as pd
import matplotlib.pyplot as plt

url = "https://data.api.abs.gov.au/rest/data/ABS,RPPI/ALL?&format=jsondata"
response = requests.get(url)
data = response.json()

# Extract the data records
records = data['data']
# Convert the list of records into a DataFrame
df = pd.DataFrame(records)
print(df)