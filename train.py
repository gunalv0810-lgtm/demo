import tensorflow as tf
from tensorflow.keras import layers, models

# Dataset path
dataset_path = "dataset"

# Load dataset
train_dataset = tf.keras.preprocessing.image_dataset_from_directory(
    dataset_path,
    image_size=(128, 128),
    batch_size=8
)

# Class names
class_names = train_dataset.class_names
print("Classes:", class_names)

# Normalize images
normalization_layer = layers.Rescaling(1./255)

train_dataset = train_dataset.map(
    lambda x, y: (normalization_layer(x), y)
)

# Build CNN Model
model = models.Sequential([

    layers.Conv2D(32, (3,3), activation='relu',
                  input_shape=(128,128,3)),

    layers.MaxPooling2D((2,2)),

    layers.Conv2D(64, (3,3), activation='relu'),

    layers.MaxPooling2D((2,2)),

    layers.Flatten(),

    layers.Dense(128, activation='relu'),

    layers.Dense(len(class_names), activation='softmax')
])

# Compile model
model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

# Train model
history = model.fit(
    train_dataset,
    epochs=5
)

# Save model
model.save("skin_disease_model.h5")

print("Model Saved Successfully!")
