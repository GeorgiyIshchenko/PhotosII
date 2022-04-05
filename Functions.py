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


def deleting_old_dataset(deleteingdataset):  # removes old dataset
    if deleteingdataset == 'train_dataset':
        try:
            path = os.path.join(os.path.dirname((__file__)), r'ls /home')
            shutil.rmtree(path)
        except:
            print("directory is already empty")
        finally:
            os.mkdir(r'ls /home')
            os.mkdir(r'ls /home/Class1')
            os.mkdir(r'ls /home/Class2')
    if deleteingdataset == 'prediction_dataset':
        try:
            path = os.path.join(os.path.dirname((__file__)), r'Onprediction')
            shutil.rmtree(path)
        except:
            print("directory is already empty")
        finally:
            os.mkdir(r'Onprediction')
            os.mkdir(r'Onprediction/Unsorted')


def model_preparation():
    try:
        model = tf.keras.models.load_model('Models')
        return model
    except:
        print("Model not found")
        return None


def model_save(model):
    path = os.path.join(os.path.dirname((__file__)), r'Models')
    shutil.rmtree(path)
    os.mkdir(r'Models')
    model.save("Models")


def download_photo(URL, name, tag, downloadtype):  # download one image using it's URL, name, tag
    if downloadtype == 'train_dataset':
        name = name + ".jpg"
        if (tag == "match"):
            name = r"ls /home/Class1/" + name
            req.urlretrieve(URL, name)
        if (tag == "notmatch"):
            name = r"ls /home/Class2/" + name
            req.urlretrieve(URL, name)
    if downloadtype == 'prediction_dataset':
        name = r"Onprediction/Unsorted/" + name + ".jpg"
        req.urlretrieve(URL, name)


def downlodad_photos_from_json(json_string, downloadtype):  # this function adds new dataset
    output = json.loads(json_string)
    photo_list = list()
    for obj in output:
        photo = Dict2Photo(obj)
        photo_list.append(photo)
    for i in range(len(photo_list)):
        download_photo(URL=photo_list[i].image,
                       name=str(i), tag=photo_list[i].tag, downloadtype=downloadtype)


def set_dataset(json_string):  # this function removes old dataset and adds new
    deleting_old_dataset(deleteingdataset='train_dataset')
    downlodad_photos_from_json(json_string, downloadtype='train_dataset')


def do_photo_array(json_string):  # do a photo array by json data
    output = json.loads(json_string)
    photo_class_list = list()
    list_of_images = list()
    for obj in output:
        photo = Dict2Photo(obj)
        photo_class_list.append(photo)
    for i in range(len(photo_class_list)):
        img = req.urlopen(photo_class_list[i].image).read()
        list_of_images.append(img)
    return list_of_images


def Education(json_string):
    BATCH_SIZE = 32
    IMG_SIZE = (160, 160)

    train_dataset = dataset_by_filenames(json_string)

    #class_names = train_dataset.class_names

    AUTOTUNE = tf.data.AUTOTUNE

    train_dataset = train_dataset.prefetch(buffer_size=AUTOTUNE)

    data_augmentation = tf.keras.Sequential([
        tf.keras.layers.RandomFlip('horizontal'),
        tf.keras.layers.RandomRotation(0.2),
    ])

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

    initial_epochs = 10

    history = model.fit(train_dataset,
                        epochs=initial_epochs)

    base_model.trainable = True

    fine_tune_at = 100

    for layer in base_model.layers[:fine_tune_at]:
        layer.trainable = False

    model.summary()

    fine_tune_epochs = 10

    total_epochs = initial_epochs + fine_tune_epochs

    history_fine = model.fit(train_dataset, epochs=total_epochs, initial_epoch=history.epoch[-1])

    queue.enqueue(model_save, model)


def _parce_function(filename, label):
    path = "Media/"
    filename = path + filename
    image_string = tf.io.read_file(filename)
    image_decoded = tf.image.decode_jpeg(image_string, channels=3)
    image = tf.cast(image_decoded, tf.float32)
    image = tf.image.resize(image, [160, 160], preserve_aspect_ratio=False)
    return image, label


def dataset_by_filenames(json_string):
    output = json.loads(json_string)
    photo_list = list()

    filenames = list()
    labels = list()

    for obj in output:
        photo = Dict2Photo(obj)
        photo_list.append(photo)

    for photo in photo_list:
        filenames.append(photo.image)
        if photo.tag == "match":
            labels.append(1)
        elif photo.tag == "notmatch":
            labels.append(0)
        else:
            labels.append(-1)

    total_amount = len(labels)



    filenames = tf.constant(filenames)
    labels = tf.constant(labels)



    dataset = tf.data.Dataset.from_tensor_slices((filenames, labels))

    dataset = dataset.map(_parce_function)
    dataset = dataset.batch(total_amount)



    return dataset


def join_prediction_dataset():
    prediction_dir = os.path.join('Onprediction')
    BATCH_SIZE = 32
    IMG_SIZE = (160, 160)
    prediction_dataset = tf.keras.utils.image_dataset_from_directory(prediction_dir,
                                                                     shuffle=True,
                                                                     batch_size=BATCH_SIZE,
                                                                     image_size=IMG_SIZE)
    return prediction_dataset


def do_prediction_dataset(json_string):
    deleting_old_dataset(deleteingdataset='prediction_dataset')
    downlodad_photos_from_json(json_string, downloadtype='prediction_dataset')
    return join_prediction_dataset()


def Prediction(json_string):
    model = model_preparation()
    prediction_dataset = dataset_by_filenames(json_string)
    AUTOTUNE = tf.data.AUTOTUNE

    prediction_dataset = prediction_dataset.prefetch(buffer_size=AUTOTUNE)

    image_batch, label_batch = prediction_dataset.as_numpy_iterator().next()
    predictions = model.predict_on_batch(image_batch).flatten()

    predictions = tf.nn.sigmoid(predictions)
    predictions = tf.where(predictions < 0.5, 0, 1)

    # print('predictions:\n', predictions.numpy())
    return predictions.numpy()
