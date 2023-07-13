# -*- coding: utf-8 -*-
"""Repositorio BIGGAN 256x256.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1NeB-XX5SNXyTfR7uk62gk8HJWXDylLuP

# Propuesta "*Alta Resolución Generative Adversarial Network*"
## Alumno: Patrick Xavier Marquez Choque
## Curso: Proyecto Final de Carrera II
## Periodo: 2023-I
"""

# Importar las bibliotecas necesarias
import tensorflow as tf
from tensorflow.keras import layers
import numpy as np

# Definir la arquitectura del generador
def build_generator():
    generator = tf.keras.Sequential()
    generator.add(layers.Dense(256, input_shape=(100,), activation='relu'))
    generator.add(layers.Reshape((1, 1, 256)))
    generator.add(layers.Conv2DTranspose(128, kernel_size=(4, 4), strides=(2, 2), padding='same', activation='relu'))
    generator.add(layers.Conv2DTranspose(64, kernel_size=(4, 4), strides=(2, 2), padding='same', activation='relu'))
    generator.add(layers.Conv2DTranspose(3, kernel_size=(4, 4), strides=(2, 2), padding='same', activation='sigmoid'))
    return generator

# Definir la arquitectura del discriminador
def build_discriminator():
    discriminator = tf.keras.Sequential()
    discriminator.add(layers.Conv2D(64, kernel_size=(4, 4), strides=(2, 2), padding='same', input_shape=(64, 64, 3)))
    discriminator.add(layers.LeakyReLU(alpha=0.2))
    discriminator.add(layers.Conv2D(128, kernel_size=(4, 4), strides=(2, 2), padding='same'))
    discriminator.add(layers.LeakyReLU(alpha=0.2))
    discriminator.add(layers.Conv2D(256, kernel_size=(4, 4), strides=(2, 2), padding='same'))
    discriminator.add(layers.LeakyReLU(alpha=0.2))
    discriminator.add(layers.Flatten())
    discriminator.add(layers.Dense(1, activation='sigmoid'))
    return discriminator

# Definir la función de pérdida
def adversarial_loss(y_true, y_pred):
    return tf.keras.losses.binary_crossentropy(y_true, y_pred)

# Definir los modelos del generador y del discriminador
generator = build_generator()
discriminator = build_discriminator()

# Compilar el modelo del generador
generator.compile(loss=adversarial_loss, optimizer=tf.keras.optimizers.Adam(0.0002, 0.5))

# Compilar el modelo del discriminador
discriminator.compile(loss=adversarial_loss, optimizer=tf.keras.optimizers.Adam(0.0002, 0.5))

# Crear un tensor de ruido para la entrada del generador
input_noise = tf.keras.Input(shape=(100,))

# Generar una imagen inpainted
inpainted_image = generator(input_noise)

# Congelar los pesos del discriminador durante el entrenamiento del generador
discriminator.trainable = False

# Definir el modelo GAN combinando el generador y el discriminador
#gan = tf.keras.Model(input_noise, discriminator(inpainted_image))
#gan.compile(loss=adversarial_loss, optimizer=tf.keras.optimizers.Adam(0.0002, 0.5))

# Importar las bibliotecas necesarias
import tensorflow as tf
from tensorflow.keras import layers
import numpy as np

# Cargar el conjunto de datos CelebA
(x_train, y_train), (_, _) = tf.keras.datasets.celebA.load_data()

# Preprocesar los datos
x_train = x_train.astype('float32') / 255.0

# Definir la arquitectura del generador
def build_generator():
    generator = tf.keras.Sequential()
    generator.add(layers.Dense(4 * 4 * 256, input_shape=(100,), activation='relu'))
    generator.add(layers.Reshape((4, 4, 256)))
    generator.add(layers.Conv2DTranspose(128, kernel_size=(4, 4), strides=(2, 2), padding='same', activation='relu'))
    generator.add(layers.Conv2DTranspose(64, kernel_size=(4, 4), strides=(2, 2), padding='same', activation='relu'))
    generator.add(layers.Conv2DTranspose(3, kernel_size=(4, 4), strides=(2, 2), padding='same', activation='sigmoid'))
    return generator

# Definir la arquitectura del discriminador
def build_discriminator():
    discriminator = tf.keras.Sequential()
    discriminator.add(layers.Conv2D(64, kernel_size=(4, 4), strides=(2, 2), padding='same', input_shape=(32, 32, 3)))
    discriminator.add(layers.LeakyReLU(alpha=0.2))
    discriminator.add(layers.Conv2D(128, kernel_size=(4, 4), strides=(2, 2), padding='same'))
    discriminator.add(layers.LeakyReLU(alpha=0.2))
    discriminator.add(layers.Conv2D(256, kernel_size=(4, 4), strides=(2, 2), padding='same'))
    discriminator.add(layers.LeakyReLU(alpha=0.2))
    discriminator.add(layers.Flatten())
    discriminator.add(layers.Dense(1, activation='sigmoid'))
    return discriminator

# Definir la función de pérdida
def adversarial_loss(y_true, y_pred):
    return tf.keras.losses.binary_crossentropy(y_true, y_pred)

# Definir los modelos del generador y del discriminador
generator = build_generator()
discriminator = build_discriminator()

# Compilar el modelo del generador
generator.compile(loss=adversarial_loss, optimizer=tf.keras.optimizers.Adam(0.0002, 0.5))

# Compilar el modelo del discriminador
discriminator.compile(loss=adversarial_loss, optimizer=tf.keras.optimizers.Adam(0.0002, 0.5))

# Crear un tensor de ruido para la entrada del generador
input_noise = tf.keras.Input(shape=(100,))

# Generar una imagen inpainted
inpainted_image = generator(input_noise)

# Congelar los pesos del discriminador durante el entrenamiento del generador
discriminator.trainable = False

# Definir el modelo GAN combinando el generador y el discriminador
gan = tf.keras.Model(input_noise, discriminator(inpainted_image))
gan.compile(loss=adversarial_loss, optimizer=tf.keras.optimizers.Adam(0.0002, 0.5))

# Entrenar la GAN
epochs = 100
batch_size = 128
steps_per_epoch = x_train.shape[0] // batch_size

for epoch in range(epochs):
    for step in range(steps_per_epoch):
        # Seleccionar un lote aleatorio de imágenes
        real_images = x_train[np.random.randint(0, x_train.shape[0], size=batch_size)]

        # Generar ruido de entrada para el generador
        noise = np.random.normal(0, 1, size=(batch_size, 100))

        # Generar imágenes inpainted utilizando el generador
        generated_images = generator.predict(noise)

        # Crear un lote combinado de imágenes reales y generadas
        combined_images = np.concatenate([generated_images, real_images])

        # Etiquetas para las imágenes combinadas
        labels = np.concatenate([np.zeros((batch_size, 1)), np.ones((batch_size, 1))])

        # Entrenar el discriminador
        d_loss = discriminator.train_on_batch(combined_images, labels)

        # Generar ruido de entrada para el generador
        noise = np.random.normal(0, 1, size=(batch_size, 100))

        # Etiquetas para las imágenes generadas
        misleading_targets = np.ones((batch_size, 1))

        # Entrenar el modelo GAN
        g_loss = gan.train_on_batch(noise, misleading_targets)

    # Imprimir el progreso del entrenamiento
    if (epoch + 1) % 100 == 0:
        print(f"Epoch {epoch+1}/{epochs} - Discriminator Loss: {d_loss} - Generator Loss: {g_loss}")

# Generar imágenes inpainted utilizando el generador
num_images = 10
noise = np.random.normal(0, 1, size=(num_images, 100))
generated_images = generator.predict(noise)

# Visualizar las imágenes generadas
import matplotlib.pyplot as plt

fig, axs = plt.subplots(1, num_images, figsize=(20, 4))
fig.suptitle('Generated Images')

for i in range(num_images):
    axs[i].imshow(generated_images[i])
    axs[i].axis('off')

plt.show()

def calculate_psnr(image1, image2):
    mse = np.mean((image1 - image2) ** 2)
    max_value = np.max(image1)
    psnr = 20 * np.log10(max_value / np.sqrt(mse))
    return psnr

psnr_values = []
for i in range(num_images):
    psnr = calculate_psnr(original_images[i], generated_images[i])
    psnr_values.append(psnr)
    print(f"PSNR for image {i+1}: {psnr} dB")

average_psnr = np.mean(psnr_values)
print(f"Average PSNR: {average_psnr} dB")

import numpy as np
from skimage.metrics import peak_signal_noise_ratio

def calculate_psnr(original_images, generated_images):
    psnr_values = []
    for i in range(len(original_images)):
        psnr = peak_signal_noise_ratio(original_images[i], generated_images[i], data_range=1.0)
        psnr_values.append(psnr)
        print(f"PSNR for image {i+1}: {psnr} dB")

    average_psnr = np.mean(psnr_values)
    print(f"Average PSNR: {average_psnr} dB")

original_images = load_celebA()

# Calcula el PSNR
calculate_psnr(original_images, generated_images)