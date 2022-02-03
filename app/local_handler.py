import pandas as pd
import os
from pathlib import Path

app_dir = Path(__file__).parent
root_dir = Path(app_dir).parent
files_dir = Path(os.path.join(app_dir, "files"))

files = [os.path.join(files_dir, file) for file in os.listdir(files_dir) if file.endswith(".csv")]

writer = pd.ExcelWriter(path="team6.xlsx", engine="xlsxwriter")
for file in files:
    df = pd.read_csv(file)
    sheet_name = file.split("_")[0].split("/")[-1]
    df.to_excel(writer, sheet_name=sheet_name)

writer.save()