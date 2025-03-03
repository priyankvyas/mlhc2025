import pandas as pd
import parser

from format.column_to_format import column_to_format

# Parse the format file
formats = parser.parse_sas_formats("./data/ed22for.txt")

# Remove a redundant key from the dictionary
del(formats['LABELS'])

# Read the NHAMCS 2022 ED dataset into a Pandas DataFrame
df = pd.read_sas("./data/ed2022_sas.sas7bdat")

# For each column, find the matching format and convert the byte values to strings so that the keys match
for col, fmt in column_to_format.items():
    if fmt in formats:  # Check if format exists
        if df[col].dtype == object:
            df[col] = df[col].apply(lambda x: "'" + x.decode("utf-8") + "'" if isinstance(x, bytes) else x)
        df[col] = df[col].map(lambda x: formats[fmt].get(x, x))  # Default to original if not found

df.to_csv("./data/formatted_ed2022.csv", index=False)
