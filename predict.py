import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np

# Load trained model
model = tf.keras.models.load_model("skin_disease_model.h5")

# Class names
class_names = ['akiec', 'bcc', 'bkl', 'df', 'mel', 'nv', 'vasc']

# Image path
img_path = "test3.jpg"   # change your image name here

# Load image
img = image.load_img(img_path, target_size=(128, 128))

# Convert image to array
img_array = image.img_to_array(img)

# Expand dimensions
img_array = np.expand_dims(img_array, axis=0)

# Normalize
img_array = img_array / 255.0

# Prediction
prediction = model.predict(img_array)

# Get highest probability
confidence = np.max(prediction) * 100

# Get predicted class index
predicted_class = np.argmax(prediction)

# Final result
print("Prediction:", class_names[predicted_class])

print("Confidence: {:.2f}%".format(confidence))
