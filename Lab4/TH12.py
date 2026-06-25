# TH12.py - Bai toan CNN (Khong dung TensorFlow)
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

# ================== TẠO ẢNH MẪU NẾU KHÔNG CÓ FILE ==================
try:
    image = np.array(Image.open('girl3.jpg').convert('L'))  # Chuyển sang grayscale
    print("✅ Đã load girl3.jpg")
except:
    print("⚠️ Không tìm thấy girl3.jpg → Tạo ảnh mẫu")
    # Tạo ảnh grayscale mẫu
    x = np.linspace(-5, 5, 300)
    y = np.linspace(-5, 5, 300)
    X, Y = np.meshgrid(x, y)
    image = (np.sin(X**2 + Y**2) * 100 + 128).astype(np.uint8)

print("Shape ảnh:", image.shape)

# Hiển thị ảnh gốc
plt.figure(figsize=(6, 6))
plt.imshow(image, cmap='gray')
plt.axis('off')
plt.title('Original Gray Scale Image')
plt.show()

# ====================== KERNEL (Edge Detection) ======================
kernel = np.array([[-1, -1, -1],
                   [-1,  8, -1],
                   [-1, -1, -1]])

# ====================== CONVOLUTION ======================
def convolution_2d(img, kernel):
    h, w = img.shape
    kh, kw = kernel.shape
    pad = kh // 2
    output = np.zeros_like(img, dtype=float)
    
    for i in range(pad, h - pad):
        for j in range(pad, w - pad):
            patch = img[i-pad:i+pad+1, j-pad:j+pad+1]
            output[i, j] = np.sum(patch * kernel)
    return output

# Thực hiện Convolution
image_conv = convolution_2d(image.astype(float), kernel)

# ====================== ReLU ======================
image_relu = np.maximum(image_conv, 0)

# ====================== MAX POOLING ======================
def max_pooling(img, size=2, stride=2):
    h, w = img.shape
    out_h = (h - size) // stride + 1
    out_w = (w - size) // stride + 1
    pooled = np.zeros((out_h, out_w))
    
    for i in range(0, h - size + 1, stride):
        for j in range(0, w - size + 1, stride):
            pooled[i//stride, j//stride] = np.max(img[i:i+size, j:j+size])
    return pooled

image_pool = max_pooling(image_relu)

# ====================== HIỂN THỊ KẾT QUẢ ======================
plt.figure(figsize=(15, 5))

plt.subplot(1, 3, 1)
plt.imshow(image_conv, cmap='gray')
plt.axis('off')
plt.title('Convolution')

plt.subplot(1, 3, 2)
plt.imshow(image_relu, cmap='gray')
plt.axis('off')
plt.title('ReLU Activation')

plt.subplot(1, 3, 3)
plt.imshow(image_pool, cmap='gray')
plt.axis('off')
plt.title('Max Pooling')

plt.tight_layout()
plt.show()

print("✅ Hoàn thành TH12 (không dùng TensorFlow)")