import zipfile
import os
import pandas as pd

# archive.zip file is too large too upload to gitHub, used alternative salary data
zip_file_path = '../Data/DataAnalyst.zip'  # Define the path to the zipped file
extraction_path = '../Data'  # Define the path to the unzipped file
print(extraction_path)

with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(extraction_path)  # Extract the zip file

file_path = os.path.join(extraction_path, 'DataAnalyst.csv')  # Load the CSV file into a DataFrame
data = pd.read_csv(file_path)


print(data)