# SISTEMA DE MEDICION AUTOMATICA POR CAMARA
# Mide la distancia entre dos puntos siguiendo un patron llamado ArUco. 
# Descargar patron en el siguiente enlace: https://chev.me/arucogen/. 
import cv2
import numpy as np
import cv2.aruco as aruco

# Configuración del marcador Aruco
ARUCO_DICT = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
ARUCO_SIZE_MM = 40.0  # Tamaño físico del marcador en mm

# Inicializar cámara
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error al capturar el video")
        break

    # Convertir a escala de grises
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detectar marcadores Aruco
    corners, ids, _ = aruco.detectMarkers(gray, ARUCO_DICT)
    if ids is not None:
        for corner in corners:
            # Dibujar el marcador detectado
            aruco.drawDetectedMarkers(frame, [corner])

            # Calcular el tamaño del marcador en píxeles
            pixel_width = np.linalg.norm(corner[0][0] - corner[0][1])

            # Relación píxeles por mm
            pixels_per_mm = pixel_width / ARUCO_SIZE_MM

            # Detección de rocas con separación
            edges = cv2.Canny(gray, 100, 150)

            # Transformaciones morfológicas para separar objetos conectados
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))  # Aumentamos el tamaño del kernel
            edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel, iterations=2)

            # Transformada de distancia
            dist_transform = cv2.distanceTransform(edges, cv2.DIST_L2, 5)
            _, sure_fg = cv2.threshold(dist_transform, 0.4 * dist_transform.max(), 255, 0)
            sure_fg = np.uint8(sure_fg)

            # Encontrar contornos después de separar objetos
            contours, _ = cv2.findContours(sure_fg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            for contour in contours:
                # Filtrar por área mínima (para ignorar ruido)
                area = cv2.contourArea(contour)
                if area < 500:  # Filtramos rocas muy pequeñas
                    continue

                # Encontrar el diámetro en píxeles
                x, y, w, h = cv2.boundingRect(contour)
                diameter_pixels = max(w, h)

                # Convertir a milímetros
                diameter_mm = diameter_pixels / pixels_per_mm

                # Dibujar solo las rocas mayores a 80 mm
                if diameter_mm >= 10:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    cv2.putText(frame, f"{diameter_mm:.2f} mm", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Mostrar el video en tiempo real
    cv2.imshow("Detección de Diámetro", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

