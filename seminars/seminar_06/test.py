import cv2
import numpy as np

def nothing(x):
    pass

# Укажите пути к вашим двум фото (например, с разным освещением или жестами)
img1 = cv2.imread('/home/homa/education/cv_course_2026/seminars/seminar_06/data/hand_4.jpg') 
img2 = cv2.imread('/home/homa/education/cv_course_2026/seminars/seminar_06/data/hand.jpg') # Укажите путь ко второму фото

# Чтобы склеить картинки, они должны быть строго одного размера.
# Уменьшаем их (480x360), чтобы итоговое склеенное окно (960x360) влезло на экран
target_size = (480, 360)
img1 = cv2.resize(img1, target_size)
img2 = cv2.resize(img2, target_size)

# Создаем окно управления
cv2.namedWindow('HSV_Tuner')

# Создаем ползунки для настройки
cv2.createTrackbar('H_min', 'HSV_Tuner', 0, 179, nothing)
cv2.createTrackbar('S_min', 'HSV_Tuner', 20, 255, nothing)
cv2.createTrackbar('V_min', 'HSV_Tuner', 70, 255, nothing)
cv2.createTrackbar('H_max', 'HSV_Tuner', 20, 179, nothing)
cv2.createTrackbar('S_max', 'HSV_Tuner', 255, 255, nothing)
cv2.createTrackbar('V_max', 'HSV_Tuner', 255, 255, nothing)

while True:
    # Размываем оба фото
    blurred1 = cv2.GaussianBlur(img1, (5, 5), 0)
    blurred2 = cv2.GaussianBlur(img2, (5, 5), 0)
    
    hsv1 = cv2.cvtColor(blurred1, cv2.COLOR_BGR2HSV)
    hsv2 = cv2.cvtColor(blurred2, cv2.COLOR_BGR2HSV)
    
    # Считываем текущие значения ползунков
    h_min = cv2.getTrackbarPos('H_min', 'HSV_Tuner')
    s_min = cv2.getTrackbarPos('S_min', 'HSV_Tuner')
    v_min = cv2.getTrackbarPos('V_min', 'HSV_Tuner')
    h_max = cv2.getTrackbarPos('H_max', 'HSV_Tuner')
    s_max = cv2.getTrackbarPos('S_max', 'HSV_Tuner')
    v_max = cv2.getTrackbarPos('V_max', 'HSV_Tuner')
    
    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])
    
    # Применяем маску к обоим
    mask1 = cv2.inRange(hsv1, lower, upper)
    mask2 = cv2.inRange(hsv2, lower, upper)
    
    # Получаем результаты
    result1 = cv2.bitwise_and(img1, img1, mask=mask1)
    result2 = cv2.bitwise_and(img2, img2, mask=mask2)
    
    # Склеиваем маски и результаты по горизонтали (бок о бок)
    combined_masks = np.hstack((mask1, mask2))
    combined_results = np.hstack((result1, result2))
    
    # Показываем склеенные изображения
    cv2.imshow('Masks (Black/White)', combined_masks)
    cv2.imshow('Results', combined_results)
    
    # Нажмите 'q' для выхода
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print(f"Ваши идеальные параметры:")
        print(f"lower_skin = np.array([{h_min}, {s_min}, {v_min}])")
        print(f"upper_skin = np.array([{h_max}, {s_max}, {v_max}])")
        break

cv2.destroyAllWindows()