# THUC HANH 13 - Bai toan CNN
# Xay dung CNN tu dau bang NumPy (khong dung TensorFlow)

#Import thu vien, ham
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

#tao ham cho phep tich chap 2D
def convolution_2d(image, filter, pad, step):
    k_size = filter.shape[0]

    #tinh toan kich thuoc khong gian chieu rong & chieu cao
    width_out  = int((image.shape[0] - k_size + 2 * pad) / step + 1)
    height_out = int((image.shape[1] - k_size + 2 * pad) / step + 1)

    #dau ra co gia tri bang khong cho hinh anh tich chap
    output_image = np.zeros((width_out - 2 * pad, height_out - 2 * pad))

    #trien khai phep toan tich chap 2D, duyet cac hinh anh dau vao
    for i in range(image.shape[0] - k_size + 1):
        for j in range(image.shape[1] - k_size + 1):
            #trich xuat (cung kich thuoc voi bo loc) tu hinh anh dau vao
            patch_from_image = image[i:i+k_size, j:j+k_size]
            #phep toan tich chap
            output_image[i, j] = np.sum(patch_from_image * filter)

    #tra ve ket qua
    return output_image

#tao chuc nang cho lop CNN
def cnn_layer(image_volume, filter, pad=1, step=1):
    #khoi luong ban do dac diem thu duoc o lop truoc
    #ap dung khoi luong hinh anh dau vao khung dem voi gia tri bang 0 cho tat ca cac kenh

    image = np.zeros((image_volume.shape[0] + 2 * pad,
                      image_volume.shape[1] + 2 * pad,
                      image_volume.shape[2]))
    for p in range(image_volume.shape[2]):

        #neu Pad=0 thi hinh anh ket qua se giong voi hinh anh dau vao
        image[:, :, p] = np.pad(image_volume[:, :, p], (pad, pad), mode='constant', constant_values=0)

    #su dung cac phuong trinh tinh kich thuoc khong gian cua size hinh anh dau ra
    # Width_Out  = (Width_In  - K_size + 2*Pad) / Step + 1
    # Height_Out = (Height_In - K_size + 2*Pad) / Step + 1
    # Depth_Out  = K_number
    # kich thuoc cua bo loc
    k_size = filter.shape[1]

    depth_out = filter.shape[0]
    #tinh kich thuoc khong gian - chieu rong va chieu cao
    width_out  = int((image_volume.shape[0] - k_size + 2 * pad) / step + 1)
    height_out = int((image_volume.shape[1] - k_size + 2 * pad) / step + 1)

    #tao mang co gia tri bang 0 cho ban do dac trung dau ra
    feature_maps = np.zeros((width_out, height_out, depth_out))

    #trien khai tich chap hinh anh bang bo loc
    n_filters = filter.shape[0]

    for i in range(n_filters):
        #khoi tao hinh anh tich chap
        convolved_image = np.zeros((width_out, height_out))

        for j in range(image.shape[-1]):
            #tich chap moi kenh (do sau) cua hinh anh voi moi kenh (do sau) cua bo loc hien tai
            #ket qua duoc tom tat
            convolved_image += convolution_2d(image[:, :, j], filter[i, :, :, j], pad, step)

        feature_maps[:, :, i] = convolved_image
    return feature_maps

#tao ham thay the gia tri pixel lon hon 255 x 255
def image_pixels_255(maps):
    #chuan bi mang de xuat ket qua
    r = np.zeros(maps.shape)
    #thay the tat ca cac phan tu lon hon 255 x 255
    for c in range(r.shape[2]):
        for i in range(r.shape[0]):
            for j in range(r.shape[1]):
                #kiem tra xem phan tu co nho hon 255 ho n 255
                if maps[i, j, c] <= 255:
                    r[i, j, c] = maps[i, j, c]
                else:
                    r[i, j, c] = 255
    return r

#tao ham cho lop ReLU
def relu_layer(maps):
    r = np.zeros_like(maps)
    #su dung dieu kien dat 'np.where' rang moi phan tu trong 'maps' phai lon hon phan tu thich hop trong 'r'
    result = np.where(maps > r, maps, r)
    return result

#tao ham cho lop Pool
def pooling_layer(maps, size=2, step=2):
    width_out  = int((maps.shape[0] - size) / step + 1)
    height_out = int((maps.shape[1] - size) / step + 1)
    pooling_image = np.zeros((width_out, height_out, maps.shape[2]))

    for c in range(maps.shape[2]):
        ii = 0
        for i in range(0, maps.shape[0] - size + 1, step):
            jj = 0
            for j in range(0, maps.shape[1] - size + 1, step):
                #trich xuat ban va (cung kich thuoc voi bo loc) tu hinh anh dau vao
                patch_from_image = maps[i:i+size, j:j+size, c]
                #hoat dong nhom max Pool - chon phan tu toi da tu ban va hien tai
                pooling_image[ii, jj, c] = np.max(patch_from_image)
                #tang chi muc cho mang tham do
                jj += 1
            #tang chi muc cho mang tham do
            ii += 1

    return pooling_image

#hinh anh dau vao thang do xam va dua du lieu vao mang
input_image = Image.open("girl3.jpg")
image_np    = np.array(input_image)
print(image_np.shape)                                            # (270, 480, 3)
print(np.array_equal(image_np[:, :, 0], image_np[:, :, 1]))     # True
print(np.array_equal(image_np[:, :, 1], image_np[:, :, 2]))     # True

filter_1 = np.random.random_integers(low=-1, high=1, size=(4, 3, 3, image_np.shape[-1]))
print(filter_1.shape)                                            # (4, 3, 3, 3)
filter_1 = np.zeros((4, 3, 3, 3))

#bo loc thu nhat
filter_1[0, :, :, 0] = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]])
filter_1[0, :, :, 1] = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]])
filter_1[0, :, :, 2] = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]])
#bo loc thu hai
filter_1[1, :, :, 0] = np.array([[ 1, 1, 1], [ 0, 0, 0], [-1,-1,-1]])
filter_1[1, :, :, 1] = np.array([[ 1, 1, 1], [ 0, 0, 0], [-1,-1,-1]])
filter_1[1, :, :, 2] = np.array([[ 1, 1, 1], [ 0, 0, 0], [-1,-1,-1]])
#bo loc thu ba
filter_1[2, :, :, 0] = np.array([[ 1,-1, 0], [-1, 0, 1], [-1, 0, 1]])
filter_1[2, :, :, 1] = np.array([[ 1,-1, 0], [-1, 0, 1], [-1, 0, 1]])
filter_1[2, :, :, 2] = np.array([[ 1,-1, 0], [-1, 0, 1], [-1, 0, 1]])
#bo loc thu tu
filter_1[3, :, :, 0] = np.array([[ 0,-1, 1], [ 1, 0,-1], [-1, 1, 0]])
filter_1[3, :, :, 1] = np.array([[ 0,-1, 1], [ 1, 0,-1], [-1, 1, 0]])
filter_1[3, :, :, 2] = np.array([[ 0,-1, 1], [ 1, 0,-1], [-1, 1, 0]])
print(filter_1.shape)                                            # (4, 3, 3, 3)

#CNN Layer 1
cnn_1 = cnn_layer(image_np, filter_1, pad=1, step=1)
cnn_1 = image_pixels_255(cnn_1)
print(cnn_1.shape)                                               # (270, 480, 4)

# ReLU Layer 1
#dau vao ban do dac diem ket qua tu lop CNN truoc do
relu_1 = relu_layer(cnn_1)
print(relu_1.shape)                                              # (270, 480, 4)

# Pooling Layer 1
#dau vao ban do dac diem ket qua tu lop ReLU truoc do
pooling_1 = pooling_layer(relu_1, size=2, step=2)
print(pooling_1.shape)                                           # (135, 240, 4)

filter_2 = np.random.random_integers(low=-1, high=1, size=(4, 3, 3, cnn_1.shape[-1]))
print(filter_2.shape)                                            # (4, 3, 3, 4)

# CNN Layer 2
#dau vao ban do dac diem ket qua tu lop Pool truoc do
cnn_2 = cnn_layer(pooling_1, filter_2, pad=1, step=1)
cnn_2 = image_pixels_255(cnn_2)
print(cnn_2.shape)                                               # (135, 240, 4)

# ReLU Layer 2
#dau vao ban do dac diem ket qua tu lop CNN truoc do
relu_2 = relu_layer(cnn_2)
print(relu_2.shape)                                              # (135, 240, 4)

# Pooling Layer 2
#dau vao ban do dac diem ket qua tu lop ReLU truoc do
pooling_2 = pooling_layer(relu_2, size=2, step=2)
print(pooling_2.shape)                                           # (67, 120, 4)

filter_3 = np.random.random_integers(low=-1, high=1, size=(4, 3, 3, cnn_2.shape[-1]))
print(filter_3.shape)                                            # (4, 3, 3, 4)

#CNN Layer 3
#dau vao dua ban do dac diem ket qua tu lop Pool truoc do
cnn_3 = cnn_layer(pooling_2, filter_3, pad=1, step=1)
cnn_3 = image_pixels_255(cnn_3)
print(cnn_3.shape)                                               # (67, 120, 4)

#ReLU Layer 3
#dau vao dua vao ban do dac diem ket qua tu lop CNN truoc do
relu_3 = relu_layer(cnn_3)
print(relu_3.shape)                                              # (67, 120, 4)

#Pooling Layer 3
#dau vao la ban do dac diem thu duoc tu lop ReLU truoc do
pooling_3 = pooling_layer(relu_3, size=2, step=2)
print(pooling_3.shape)                                           # (33, 60, 4)

n_rows = cnn_1.shape[-1]
figure_1, ax = plt.subplots(nrows=n_rows, ncols=9, edgecolor='Black')

# dieu chinh bieu do phu cho lop CNN 1
ax[0, 0].imshow(cnn_1[:, :, 0], cmap=plt.get_cmap('gray'))
ax[0, 0].set_axis_off()
ax[0, 0].set_title('CNN #1')
for i in range(1, n_rows):
    ax[i, 0].imshow(cnn_1[:, :, i], cmap=plt.get_cmap('gray'))
    ax[i, 0].set_axis_off()

#dieu chinh bieu do phu cho lop ReLU 1
ax[0, 1].imshow(relu_1[:, :, 0], cmap=plt.get_cmap('gray'))
ax[0, 1].set_axis_off()
ax[0, 1].set_title('ReLU #1')
for i in range(1, n_rows):
    ax[i, 1].imshow(relu_1[:, :, i], cmap=plt.get_cmap('gray'))
    ax[i, 1].set_axis_off()

#dieu chinh o phu cho lop Pool 1
ax[0, 2].imshow(pooling_1[:, :, 0], cmap=plt.get_cmap('gray'))
ax[0, 2].set_axis_off()
ax[0, 2].set_title('Pooling #1')
for i in range(1, n_rows):
    ax[i, 2].imshow(pooling_1[:, :, i], cmap=plt.get_cmap('gray'))
    ax[i, 2].set_axis_off()

#dieu chinh bieu do phu cho lop CNN 2
ax[0, 3].imshow(cnn_2[:, :, 0], cmap=plt.get_cmap('gray'))
ax[0, 3].set_axis_off()
ax[0, 3].set_title('CNN #2')
for i in range(1, n_rows):
    ax[i, 3].imshow(cnn_2[:, :, i], cmap=plt.get_cmap('gray'))
    ax[i, 3].set_axis_off()

#dieu chinh bieu do phu cho lop ReLU 2
ax[0, 4].imshow(relu_2[:, :, 0], cmap=plt.get_cmap('gray'))
ax[0, 4].set_axis_off()
ax[0, 4].set_title('ReLU #2')
for i in range(1, n_rows):
    ax[i, 4].imshow(relu_2[:, :, i], cmap=plt.get_cmap('gray'))
    ax[i, 4].set_axis_off()

#dieu chinh o phu cho lop Pool 2
ax[0, 5].imshow(pooling_2[:, :, 0], cmap=plt.get_cmap('gray'))
ax[0, 5].set_axis_off()
ax[0, 5].set_title('Pooling #2')
for i in range(1, n_rows):
    ax[i, 5].imshow(pooling_2[:, :, i], cmap=plt.get_cmap('gray'))
    ax[i, 5].set_axis_off()

#dieu chinh bieu do phu cho lop CNN 3
ax[0, 6].imshow(cnn_3[:, :, 0], cmap=plt.get_cmap('gray'))
ax[0, 6].set_axis_off()
ax[0, 6].set_title('CNN #3')
for i in range(1, n_rows):
    ax[i, 6].imshow(cnn_3[:, :, i], cmap=plt.get_cmap('gray'))
    ax[i, 6].set_axis_off()

#dieu chinh bieu do phu cho lop ReLU 3
ax[0, 7].imshow(relu_3[:, :, 0], cmap=plt.get_cmap('gray'))
ax[0, 7].set_axis_off()
ax[0, 7].set_title('ReLU #3')
for i in range(1, n_rows):
    ax[i, 7].imshow(relu_3[:, :, i], cmap=plt.get_cmap('gray'))
    ax[i, 7].set_axis_off()

#dieu chinh o phu cho lop Pool 3
ax[0, 8].imshow(pooling_3[:, :, 0], cmap=plt.get_cmap('gray'))
ax[0, 8].set_axis_off()
ax[0, 8].set_title('Pooling #3')
for i in range(1, n_rows):
    ax[i, 8].imshow(pooling_3[:, :, i], cmap=plt.get_cmap('gray'))
    ax[i, 8].set_axis_off()

#dat ten cho cua so bang hinh anh - cua so dat tieu de
#figure_('CNN --> ReLU --> Pooling')

plt.show()
