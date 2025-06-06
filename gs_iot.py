import cv2
import mediapipe as mp
import pyttsx3

#Inicializando reconhecimento de mãos e motor de voz
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

engine = pyttsx3.init()

#Define idioma como português
voices = engine.getProperty('voices')
for voice in voices:
    if 'portuguese' in voice.name.lower() or 'brazil' in voice.name.lower():
        engine.setProperty('voice', voice.id)
        break


#Função para falar
def falar(texto):
    engine.say(texto)
    engine.runAndWait()

#Função para identificar gesto com base em landmarks
def detectar_gesto(landmarks):
    dedos = []

    #Função auxiliar para comparar com margem de tolerância
    def acima(ponta, base, margem=0.02):
        return ponta.y < (base.y - margem)

    #Polegar: distância horizontal entre ponta (4) e base (2)
    if landmarks[4].x < landmarks[3].x and abs(landmarks[4].y - landmarks[3].y) < 0.1:
        dedos.append(1)
    else:
        dedos.append(0)

    #Indicador
    dedos.append(1 if acima(landmarks[8], landmarks[6]) else 0)

    #Médio
    dedos.append(1 if acima(landmarks[12], landmarks[10]) else 0)

    #Anelar
    dedos.append(1 if acima(landmarks[16], landmarks[14]) else 0)

    #Mínimo
    dedos.append(1 if acima(landmarks[20], landmarks[18]) else 0)

    #Mapeamento
    if dedos == [0, 0, 0, 0, 0]:
        return "Punho fechado"
    elif dedos == [1, 0, 0, 0, 0]:
        return "Joinha"
    elif dedos == [0, 1, 0, 0, 0]:
        return "Indicador levantado"
    elif dedos == [1, 1, 1, 1, 1] or dedos == [0, 1, 1, 1, 1]:
        return "Mão aberta"
    else:
        return None  #Ignora gestos ambíguos

#Flags para evitar repetição de fala
ultimo_gesto = None
gesto_estavel = None
contagem_estavel = 0
frames_necessarios = 5  #número de frames com o mesmo gesto antes de agir


#Captura da câmera
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("❌ Não foi possível acessar a câmera.")
    exit()


import time
ultimo_tempo_acao = 0
cooldown = 2  #segundos entre ações faladas


while True:
    ret, frame = cap.read()
    if not ret:
        break

    #Conversão para RGB
    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    resultados = hands.process(img_rgb)

    if resultados.multi_hand_landmarks:
        for handLms in resultados.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)

            gesto = detectar_gesto(handLms.landmark)

            tempo_atual = time.time()
            if gesto:
                if gesto == gesto_estavel:
                    contagem_estavel += 1
                else:
                    gesto_estavel = gesto
                    contagem_estavel = 1

                if contagem_estavel >= frames_necessarios and gesto != ultimo_gesto and (tempo_atual - ultimo_tempo_acao > cooldown):
                    ultimo_gesto = gesto
                    ultimo_tempo_acao = tempo_atual

                    if gesto == "Mão aberta":
                        falar("Solicitando ajuda")
                    elif gesto == "Joinha":
                        falar("Tudo certo")
                    elif gesto == "Indicador levantado":
                        falar("Ativando lanterna")
                    elif gesto == "Punho fechado":
                        falar("Parando reconhecimento")

                    print(f"Gesto detectado: {gesto}")
            else:
                gesto_estavel = None
                contagem_estavel = 0


            cv2.putText(frame, gesto, (10, 50), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0, 255, 0), 2)

    cv2.imshow("Guia Gestual - Pressione Q para sair", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

#Liberação de recursos
cap.release()
cv2.destroyAllWindows()
