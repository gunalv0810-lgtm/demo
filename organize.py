import os
import pandas as pd
import shutil

print("STARTED")

print("Current folder:")
print(os.getcwd())

df = pd.read_csv("C:/Users/acer/Downloads/AIML project/HAM10000_metadata.csv")

print(df.head())

os.makedirs("dataset", exist_ok=True)

count = 0

for _, row in df.iterrows():

    image_name = row["image_id"] + ".jpg"
    label = row["dx"]

    source = os.path.join("images", image_name)

    target_folder = os.path.join("dataset", label)
    os.makedirs(target_folder, exist_ok=True)

    target = os.path.join(target_folder, image_name)

    if os.path.isfile(source):
        shutil.copy2(source, target)
        count += 1

print("Copied:", count)
print("DONE")
