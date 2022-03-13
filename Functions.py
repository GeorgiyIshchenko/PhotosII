import json
from Photo import Photo_Schema, Dict2Photo
import matplotlib.pyplot as plt
import numpy as np
import os
import tensorflow as tf
import requests
import shutil
import urllib.request as req
from redis import Redis
import rq

queue = rq.Queue('list0', connection=Redis.from_url('redis://'))
args = []

# comment

def download_photo(URL, name, tag):
    name = name + ".jpg"
    if (tag == "match"):
        name = r"ls /home/Class1/" + name
        req.urlretrieve(URL, name)
    if (tag == "notmatch"):
        name = r"ls /home/Class2/" + name
        req.urlretrieve(URL, name)

def downlodad_photo_from_json(json_string):
    output = json.loads(json_string)
    photo_list = list()
    for obj in output:
        photo = Dict2Photo(obj)
        print(photo.image)
        photo_list.append(photo)
    print(*photo_list)
    for i in range (len(photo_list)):
        job = queue.enqueue(download_photo,
                           URL=photo_list[i].image,
                           name=str(i), tag=photo_list[i].tag)

def Education():
    _URL = 'https://storage.googleapis.com/mledu-datasets/cats_and_dogs_filtered.zip'
    path_to_zip = tf.keras.utils.get_file('cats_and_dogs.zip', origin=_URL, extract=True)
    PATH = os.path.join(os.path.dirname(path_to_zip), 'cats_and_dogs_filtered')
    PATH = r"ls "

    train_dir = os.path.join(PATH, 'home')
    validation_dir = os.path.join(PATH, 'Test')

    BATCH_SIZE = 32
    IMG_SIZE = (160, 160)

    train_dataset = tf.keras.utils.image_dataset_from_directory(train_dir,
                                                                shuffle=True,
                                                                batch_size=BATCH_SIZE,
                                                                image_size=IMG_SIZE)

    validation_dataset = tf.keras.utils.image_dataset_from_directory(validation_dir,
                                                                     shuffle=True,
                                                                     batch_size=BATCH_SIZE,
                                                                     image_size=IMG_SIZE)

    class_names = train_dataset.class_names

    plt.figure(figsize=(10, 10))
    for images, labels in train_dataset.take(1):
        for i in range(9):
            ax = plt.subplot(3, 3, i + 1)
            plt.imshow(images[i].numpy().astype("uint8"))
            plt.title(class_names[labels[i]])
            plt.axis("off")

    val_batches = tf.data.experimental.cardinality(validation_dataset)
    test_dataset = validation_dataset.take(val_batches // 2)
    validation_dataset = validation_dataset.skip(val_batches // 2)

    print('Number of validation batches: %d' % tf.data.experimental.cardinality(validation_dataset))
    print('Number of test batches: %d' % tf.data.experimental.cardinality(test_dataset))

    AUTOTUNE = tf.data.AUTOTUNE

    train_dataset = train_dataset.prefetch(buffer_size=AUTOTUNE)
    validation_dataset = validation_dataset.prefetch(buffer_size=AUTOTUNE)
    test_dataset = test_dataset.prefetch(buffer_size=AUTOTUNE)

    data_augmentation = tf.keras.Sequential([
        tf.keras.layers.RandomFlip('horizontal'),
        tf.keras.layers.RandomRotation(0.2),
    ])

    for image, _ in train_dataset.take(1):
        plt.figure(figsize=(10, 10))
        first_image = image[0]
        for i in range(9):
            ax = plt.subplot(3, 3, i + 1)
            augmented_image = data_augmentation(tf.expand_dims(first_image, 0))
            plt.imshow(augmented_image[0] / 255)
            plt.axis('off')

    preprocess_input = tf.keras.applications.mobilenet_v2.preprocess_input
    rescale = tf.keras.layers.Rescaling(1. / 127.5, offset=-1)

    IMG_SHAPE = IMG_SIZE + (3,)
    base_model = tf.keras.applications.MobileNetV2(input_shape=IMG_SHAPE,
                                                   include_top=False,
                                                   weights='imagenet')

    image_batch, label_batch = next(iter(train_dataset))
    feature_batch = base_model(image_batch)
    print(feature_batch.shape)

    base_model.trainable = False

    base_model.summary()

    global_average_layer = tf.keras.layers.GlobalAveragePooling2D()
    feature_batch_average = global_average_layer(feature_batch)
    print(feature_batch_average.shape)

    prediction_layer = tf.keras.layers.Dense(1)
    prediction_batch = prediction_layer(feature_batch_average)
    print(prediction_batch.shape)

    inputs = tf.keras.Input(shape=(160, 160, 3))
    x = data_augmentation(inputs)
    x = preprocess_input(x)
    x = base_model(x, training=False)
    x = global_average_layer(x)
    x = tf.keras.layers.Dropout(0.2)(x)
    outputs = prediction_layer(x)
    model = tf.keras.Model(inputs, outputs)

    base_learning_rate = 0.0001
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=base_learning_rate),
                  loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
                  metrics=['accuracy'])

    model.summary()

    initial_epochs = 30

    loss0, accuracy0 = model.evaluate(validation_dataset)

    print("initial loss: {:.2f}".format(loss0))
    print("initial accuracy: {:.2f}".format(accuracy0))

    history = model.fit(train_dataset,
                        epochs=initial_epochs,
                        validation_data=validation_dataset)

    model.save("Models")
