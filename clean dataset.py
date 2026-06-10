import os

dataset_path = "dataset"

keep_limit = 100

for disease in os.listdir(dataset_path):

    disease_folder = os.path.join(dataset_path, disease)

    if os.path.isdir(disease_folder):

        images = os.listdir(disease_folder)

        images.sort()

        print(f"\n{disease} before: {len(images)} images")

        extra_images = images[keep_limit:]

        for img in extra_images:

            img_path = os.path.join(disease_folder, img)

            os.remove(img_path)

        print(f"{disease} after: {keep_limit} images")
