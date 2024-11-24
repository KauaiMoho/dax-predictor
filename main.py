import numpy as np
from bs4 import BeautifulSoup as bs
import pandas as pd

dax_raw = pd.read_csv('dax_2019-2024.csv')
print(dax_raw)