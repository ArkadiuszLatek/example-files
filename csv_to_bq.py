#!/usr/bin/env python
# coding: utf-8

import json
import pandas as pd
from pandas.io.json import json_normalize
import numpy as np
import pandas_gbq
from google.cloud import bigquery

credentials = 'key.json'
project_id = 'test_project'
client = bigquery.Client(credentials=credentials, project=project_id)

pandas_gbq.context.credentials = credentials
pandas_gbq.context.project = project_id

df = pd.read_csv('testfile.csv')
df.columns = ['key', 'value']
schema = [
    {
        "mode": "NULLABLE",
        "name": "key",
        "type": "STRING"
    },
    {
        "mode": "NULLABLE",
        "name": "value",
        "type": "STRING"
    }
]
df.to_gbq('ALatek.list', project_id='test_project', if_exists='append', table_schema=schema)
print('data from file ' + str('testfile.csv') + ' appended')


print('test')