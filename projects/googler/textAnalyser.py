import spacy
import numpy as np
import pandas as pd 
import os
import datetime as datetime
import fnmatch
import json



pathData = './'
df = pd.read_json(os.path.join(pathData,'results.json'))
df.head()

