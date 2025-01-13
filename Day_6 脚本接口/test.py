import pandas as pd
data = pd.read_excel('二大班.xlsx',sheet_name='Sheet1')
print(data[data['姓名（必填）']=='李振良'])