
import cv2
import numpy as np
from PIL import Image, ImageDraw

# Функция для создания круглого макета
def create_circular_mask(h, w, center=None, radius=None):
    if center is None:
        center = (int(w/2), int(h/2))
    if radius is None:
        radius = min(center)

    Y, X = np.ogrid[:h, :w]
    dist_from_center = np.sqrt((X - center[0])**2 + (Y-center[1])**2)

    mask = dist_from_center <= radius
    return mask

# Открываем видео
video = cv2.VideoCapture("./_apps/circle_video/media/VIDEO.mp4")

# Создаем новое видео
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
out = cv2.VideoWriter("new_video.mp4", fourcc, 30.0, (400, 400))

while True:
    ret, frame = video.read()
    if not ret:
        break

    # Преобразуем кадр в изображение PIL
    img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    # Создаем круглую маску
    mask = create_circular_mask(img.size[1], img.size[0])

    # Применяем маску к изображению
    masked_img = Image.fromarray(np.array(img) * np.expand_dims(mask, axis=2))

    # Преобразуем изображение обратно в кадр OpenCV
    masked_frame = cv2.cvtColor(np.array(masked_img), cv2.COLOR_RGB2BGR)

    # Записываем кадр в новое видео
    out.write(masked_frame)

# Закрываем видео
video.release()
out.release()
cv2.destroyAllWindows()
