import cv2
import numpy as np
import matplotlib.pyplot as plt


# 灰度化
def rbg2gray(img):
    gray = 0.2126 * img[..., 2] + 0.7152 * img[..., 1] + 0.0722 * img[..., 0]
    return gray


def hog(imggray):
    img = cv2.imread(imggray).astype(np.float32)
    H, W, C = img.shape
    # 灰度化
    gray = rbg2gray(img)

    # 填充边框：填充厚度1
    # 填充内容：原始图片边框信息

    # print(gray[...])
    gray = np.pad(gray, (1, 1), 'edge')
    # print(gray[...])

    # 图像灰度化之后，在x方向和y方向上求出亮度的梯度
    # x方向： g_x = I(x + 1, y) - I(x - 1, y)
    # y方向： g_y = I(x, y + 1) - I(x, y - 1)
    # print("\n",gray)
    # print("\n",gray[1:H + 1, 2:])
    # print("\n",gray[1:H + 1, :W])
    gx = gray[1:H + 1, 2:] - gray[1:H + 1, :W]
    gy = gray[2:, 1:W + 1] - gray[:H, 1:W + 1]
    gx[gx == 0] = 1e-6  # 避免除0
    # print("\n",gx)

    # 从g_x和g_y确定梯度幅值和梯度方向：
    # 梯度幅值：mag =\sqrt{{g_x} ^ 2 + {g_y} ^ 2}
    amplitude = np.sqrt(gx ** 2 + gy ** 2)

    # 梯度方向： ang =arctan\frac{g_y}{g_x}}
    gradient = np.arctan(gy / gx)
    gradient[gradient < 0] = np.pi / 2 + gradient[gradient < 0] + np.pi / 2

    # 量化梯度：将梯度方向[0,180]（pi）进行9等分量化
    gradient_quantized = np.zeros_like(gradient, dtype=np.int)
    d = np.pi / 9
    # np.where(condition):输出满足条件 (即非0) 元素的坐标
    for i in range(9):
        gradient_quantized[np.where((gradient >= d * i) & (gradient <= d * (i + 1)))] = i

    out = (amplitude / amplitude.max() * 255).astype(np.uint8)

    m_h, m_w = amplitude.shape

    # 8个细胞组成block
    n = 8
    # " / "就表示 浮点数除法，返回浮点结果;" // "表示整数除法。
    cell_n_h = m_h // n
    cell_n_w = m_w // n
    histogram = np.zeros((cell_n_h, cell_n_w, 9), dtype=np.float32)

    for y in range(cell_n_h):
        for x in range(cell_n_w):
            for j in range(n):
                for i in range(n):
                    histogram[y, x, gradient_quantized[y * 4 + j, x * 4 + i]] += amplitude[y * 4 + j, x * 4 + i]

    img = img.astype(np.uint8)
    cv2.imshow("img", img)
    cv2.imshow("out", out)

    for i in range(9):
        plt.subplot(3, 3, i + 1)
        plt.imshow(histogram[..., i])
        plt.axis('off')
        plt.xticks(color="None")
        plt.yticks(color="None")
    plt.savefig("out.png")
    plt.show()

    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    img = "C:/Users/Administrator/Desktop/OpencvTestImg/imori.jpg"
    img1 = "C:/Users/Administrator/Desktop/OpencvTestImg/img10.png"
    hog(img)
