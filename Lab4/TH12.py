# THUC HANH 12 - Bai toan CNN
# Xet mot hinh anh va ap dung lop tich chap, lop kich hoat va lop gop

#import thu vien
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from itertools import product

#dat tham so
plt.rc('figure', autolayout=True)
plt.rc('image', cmap='magma')

#xac dinh hat nhan
kernel = tf.constant([[-1, -1, -1],
                      [-1,  8, -1],
                      [-1, -1, -1],
                     ])

#load tai hinh anh
image = tf.io.read_file('girl3.jpg')
image = tf.io.decode_jpeg(image, channels=1)
image = tf.image.resize(image, size=[300, 300])

#ve hinh anh
img = tf.squeeze(image).numpy()
plt.figure(figsize=(5, 5))
plt.imshow(img, cmap='gray')
plt.axis('off')
plt.title('Original Gray Scale image')  #hinh anh thang do xam tu anh goc
plt.show()

#dinh dang lai hinh anh
image = tf.image.convert_image_dtype(image, dtype=tf.float32)
image = tf.expand_dims(image, axis=0)
kernel = tf.reshape(kernel, [*kernel.shape, 1, 1])
kernel = tf.cast(kernel, dtype=tf.float32)

#lop tich chap
conv_fn = tf.nn.conv2d

image_filter = conv_fn(
    input=image,
    filters=kernel,
    strides=1,  # or (1, 1)
    padding='SAME',
)
plt.figure(figsize=(15, 5))

#ve hinh anh da duoc tich chap
plt.subplot(1, 3, 1)
plt.imshow(
    tf.squeeze(image_filter)
)
plt.axis('off')
plt.title('Convolution')

#lop kich hoat
relu_fn = tf.nn.relu
#phat hien anh
image_detect = relu_fn(image_filter)

plt.subplot(1, 3, 2)
plt.imshow(
    #dinh dang lai de ve do thi
    tf.squeeze(image_detect)
)
plt.axis('off')
plt.title('Activation')

#lop gop
pool = tf.nn.pool
image_condense = pool(input=image_detect,
                      window_shape=(2, 2),
                      pooling_type='MAX',
                      strides=(2, 2),
                      padding='SAME',
                     )

plt.subplot(1, 3, 3)
plt.imshow(tf.squeeze(image_condense))
plt.axis('off')
plt.title('Pooling')
plt.show()
