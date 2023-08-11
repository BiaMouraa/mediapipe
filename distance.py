
###########################################
##### CONTADOR DE DEDOS COM MEDIAPIPE #####
#### OBS: IMPLEMENTADO P/ MAO ESQUERDA ####
###########################################

import mediapipe as mp
import cv2
import math

# Inicia a captura da webcam
video = cv2.VideoCapture(2)

# Inicia variáveis auxiliares com mediapipe
hand = mp.solutions.hands
Hand = hand.Hands(max_num_hands = 2) #Detecta apenas 1 mao
mpDraw = mp.solutions.drawing_utils

while True:
    check, img = video.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    cv2.flip(img, 1)
    cv2.flip(imgRGB, 1)

    #Mapeia os pontos da mao presente na imagem
    results = Hand.process(imgRGB)
    handsPoints = results.multi_hand_landmarks
    h,w,_ = img.shape
    pontos = []

    if handsPoints: #se houver pontos, ou seja, se for identificada a mao
        #Percorre todos os pontos identificados e desenha eles
        for points in handsPoints:
            mpDraw.draw_landmarks(img, points, hand.HAND_CONNECTIONS)
            #Imprime a numeracao de cada ponto e adiciona suas coord. no array
            for id,cord in enumerate(points.landmark):
                cx, cy = int(cord.x*w), int(cord.y*h)
                pontos.append((cx,cy))

        dedos = [8,12,16,20] #pontos das extremidades de cada dedo
        contador = 0
        length = []
        if points: #se houver pontos, ou seja, se for identificada a mao
            cv2.line(img, pontos[4], pontos[8], (255,0,0), 3)
            length.append(math.hypot(pontos[4][0]-pontos[8][0], pontos[4][1]-pontos[8][1]))
            cv2.putText(img, str(int(length[0])), (pontos[4][0], pontos[4][1]-50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 2)
            for i in range(3):
                cv2.line(img, pontos[dedos[i]], pontos[dedos[i+1]], (255,0,0), 3)
                length.append(math.hypot(pontos[dedos[i]][0]-pontos[dedos[i+1]][0], pontos[dedos[i]][1]-pontos[dedos[i+1]][1]))
                cv2.putText(img, str(int(length[i+1])), (pontos[dedos[i]][0]-50, pontos[dedos[i]][1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 2)

        print("Distancia em pixel")
        print("dedao -> indicador: ", length[0])
        print("indicador -> meio: ", length[1])
        print("meio -> anelar: ", length[2])
        print("anelar -> mindinho: ", length[3])
        print("\n")

    cv2.imshow('Imagem', img)
    cv2.waitKey(1)