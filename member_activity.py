import pandas as pd
import glob
import pandas as pd


csv_file = glob.glob('*.csv')[0]
data = pd.read_csv(csv_file, index_col=0)
print(data)