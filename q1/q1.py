import cv2
import numpy as np

video_path = "C:/Users/lukin/OneDrive/Área de Trabalho/Faculdade/Nova pasta/Python/pdi-atividade-main/q1/q1A.mp4"
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print(f"Erro ao abrir o vídeo: {video_path}")
    exit()

colidiu = False
passou_barreira = False
ultima_posicao_barra = None  

while True:
    ret, frame = cap.read()

    if not ret:
        print("Fim do vídeo ou erro na leitura.")
        break 

    frame = cv2.resize(frame, (800, 600))

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_red1 = np.array([0, 120, 70])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 120, 70])
    upper_red2 = np.array([180, 255, 255])

    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask_red = cv2.bitwise_or(mask1, mask2)

    contours_red, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    red_rect = None 
    for contour in contours_red:
        area = cv2.contourArea(contour)
        if area > 500: 
            x, y, w, h = cv2.boundingRect(contour)
            red_rect = (x, y, w, h)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3) 

    lower_blue = np.array([100, 150, 50])
    upper_blue = np.array([140, 255, 255])
    
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)

    contours_blue, _ = cv2.findContours(mask_blue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    blue_rect = None  
    for contour in contours_blue:
        area = cv2.contourArea(contour)
        if area > 500:  
            x, y, w, h = cv2.boundingRect(contour)
            blue_rect = (x, y, w, h)
            ultima_posicao_barra = blue_rect 

    if blue_rect is None and ultima_posicao_barra is not None:
        blue_rect = ultima_posicao_barra

    if red_rect and blue_rect:  
        rx, ry, rw, rh = red_rect
        bx, by, bw, bh = blue_rect

        if (rx < bx + bw and rx + rw > bx) and (ry < by + bh and ry + rh > by):
            colidiu = True  
            cv2.putText(frame, "COLISAO DETECTADA", (200, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 255), 3)

        if rx + rw < bx:
            passou_barreira = True  


    if passou_barreira:
        cv2.putText(frame, "PASSOU PELA BARREIRA", (180, 150), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 255), 3)


    cv2.imshow("Detecção de Colisão", frame)

    # Pressione 'ESC' para sair
    key = cv2.waitKey(30) & 0xFF
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
