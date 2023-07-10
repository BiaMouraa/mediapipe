
###########################################
##### CONTADOR DE DEDOS COM MEDIAPIPE #####
#### OBS: IMPLEMENTADO P/ MAO ESQUERDA ####
###########################################

import mediapipe as mp
import cv2

# Inicia a captura da webcam
video = cv2.VideoCapture(0)

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
                cv2.putText(img, str(id), (cx, cy+10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 2)
                pontos.append((cx,cy))

        dedos = [8,12,16,20] #pontos das extremidades de cada dedo
        contador = 0
        if points: #se houver pontos, ou seja, se for identificada a mao
            if pontos[4][0] < pontos[2][0]: #condicao dedao esquerdo
                contador += 1
            for x in dedos:
                if pontos[x][1] < pontos[x-2][1]:
                    contador += 1

            cv2.putText(img, str(contador), (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 4, (255,0,0), 5)
            print("Coordenadas em pixel")
            print("Dedao: ", pontos[4])
            print("Indicador: ", pontos[8])
            print("Meio: ", pontos[12])
            print("Anelar: ", pontos[16])
            print("Mindinho: ", pontos[20])
            print("\n")

    cv2.imshow('Imagem', img)
    cv2.waitKey(1)