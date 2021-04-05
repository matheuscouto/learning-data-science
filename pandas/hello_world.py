import pandas as pd
import numpy as np
df = pd.DataFrame(np.random.randn(5, 10))
def set_pandas_display_options() -> None:
    display = pd.options.display
    display.max_columns = 100
    display.max_rows = 100
    display.max_colwidth = 199
    display.width = None
set_pandas_display_options()
print(df)