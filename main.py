import cv2
import numpy as np

def process_video():
    # Inicia la captura desde la cámara
    cap = cv2.VideoCapture(0)  # "0" selecciona la cámara predeterminada
    if not cap.isOpened():
        print("No se pudo abrir la cámara")
        return

    while True:
        # Lee un frame desde la cámara
        ret, frame = cap.read()
        if not ret:
            print("No se pudo leer el frame")
            break

        # Convertir el frame al espacio de color HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Definir el rango para el color azul en HSV
        lower_blue = np.array([100, 150, 50])
        upper_blue = np.array([140, 255, 255])

        # Crear una máscara para detectar el color azul
        mask = cv2.inRange(hsv, lower_blue, upper_blue)

        # Encontrar contornos en la máscara
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Variables para mostrar la dirección
        direction = "Detener"  # Por defecto, el movimiento está detenido

        if contours:
            # Seleccionar el contorno más grande
            largest_contour = max(contours, key=cv2.contourArea)

            # Calcular el momento del contorno para encontrar su centroide
            moments = cv2.moments(largest_contour)
            if moments["m00"] != 0:
                cx = int(moments["m10"] / moments["m00"])  # Coordenada X del centroide
                cy = int(moments["m01"] / moments["m00"])  # Coordenada Y del centroide

                # Determinar la posición del centroide en relación al centro del frame
                frame_center = frame.shape[1] // 2  # Centro del frame en el eje X

                if cx < frame_center - 50:  # Ajusta el umbral según sea necesario
                    direction = "Izquierda"
                elif cx > frame_center + 50:
                    direction = "Derecha"
                else:
                    direction = "Recto"

                # Dibujar el centroide en el frame
                cv2.circle(frame, (cx, cy), 10, (0, 255, 0), -1)

        # Dibujar texto en el frame con la dirección detectada
        cv2.putText(frame, f"Direccion: {direction}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Mostrar el frame
        cv2.imshow("Video en Tiempo Real", frame)

        # Salir con la tecla 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Ejecutar la función
process_video()
