import pandas as pd
from dash import dcc, html

def load_and_clean_data(file_path):
    df = pd.read_csv(file_path, skiprows=1)
    df.dropna(inplace=True)
    df.reset_index(inplace=True)
    df.drop("index", axis=1, inplace=True)
    return df

# For the display links.
def pre_process_planets(planet):
  # Remove leading and trailing spaces
  planet = planet.strip()
  # Replace spaces with hyphens and convert to lowercase
  planet = planet.replace(" ", "_")
  return planet