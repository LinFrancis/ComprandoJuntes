"""Helper de exportación Excel (mantenido por compatibilidad)."""
import io
import pandas as pd


def export_excel(dataframes: dict, filename: str = "reporte_red_alimentos.xlsx") -> io.BytesIO:
    """
    Recibe un dict {nombre: DataFrame} y retorna un BytesIO con el Excel.
    Uso: buffer = export_excel({"participantes": df1, ...})
    """
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        for name, df in dataframes.items():
            if isinstance(df, pd.DataFrame) and not df.empty:
                df.to_excel(writer, sheet_name=name[:31], index=False)
    buffer.seek(0)
    return buffer
