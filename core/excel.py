
import pandas as pd

def export_excel(dataframes):
    file="reporte_red_alimentos.xlsx"
    with pd.ExcelWriter(file) as writer:
        for name,df in dataframes.items():
            df.to_excel(writer,sheet_name=name,index=False)
    return file
