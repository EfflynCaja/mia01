# SISTEMA DE MEDICION MANUAL POR CAMARA
# Mide la distancia entre dos puntos siguiendo un patron llamado ArUco. 
# Descargar patron en el siguiente enlace: https://chev.me/arucogen/. 
import cv2
import numpy as np

# Inicializar la cámara
cap = cv2.VideoCapture(0)

# Variable global para almacenar los puntos
points = []

# Función de evento para capturar los puntos y dibujar la línea
def click_event(event, x, y, flags, param):
    global points
    if event == cv2.EVENT_LBUTTONDOWN:
        points.append((x, y))  # Guardar el punto donde se hace clic
        if len(points) > 2:           
            # Dibujar la línea entre los dos puntos
            # cv2.line(frame, points[0], points[1], (0, 255, 0), 2)  # Línea verde
            # cv2.circle(frame, points[0], 5, (0, 0, 255), -1)  # Punto rojo en el primer clic
            # cv2.circle(frame, points[1], 5, (0, 0, 255), -1)  # Punto rojo en el segundo clic
            # Reiniciar los puntos después de dibujar la línea
            points.clear()
    
        print(points)
 
# Capturar el primer fotograma para usarlo como fondo
ret, frame = cap.read()

# Crear la ventana para mostrar el video en tiempo real
cv2.imshow("Dibujar línea", frame)

# Configurar el evento de clic del mouse después de crear la ventana
cv2.setMouseCallback("Dibujar línea", click_event)

# Esperar hasta que se presione la tecla 'q' para salir
while True:
    ret, frame = cap.read()
    if not ret:
        print("Error al capturar el video")
        break

    if len(points) == 1:
        cv2.circle(frame, points[0], 5, (0, 0, 255), -1)  # Punto rojo en el primer clic
    if len(points) == 2:
        cv2.circle(frame, points[0], 5, (0, 0, 255), -1)
        cv2.line(frame, points[0], points[1], (0, 255, 0), 2)  # Línea verde
        cv2.circle(frame, points[1], 5, (0, 0, 255), -1)  # Punto rojo en el segundo clic
    
    # Mostrar el video con la línea dibujada
    cv2.imshow("Dibujar línea", frame)

    # Salir si se presiona la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
