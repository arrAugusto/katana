import cv2
import numpy as np
import time

def simulate_with_tooltip(image_path):
    # Cargar la imagen desde la ruta proporcionada
    image = cv2.imread(image_path)
    if image is None:
        print("Error: No se pudo cargar la imagen.")
        return

    # Convertir la imagen al espacio de color HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Definir el rango para el color azul en HSV
    lower_blue = np.array([100, 150, 50])
    upper_blue = np.array([140, 255, 255])

    # Crear una máscara para detectar azul
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # Encontrar los contornos en la máscara
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        # Seleccionar el contorno más grande
        largest_contour = max(contours, key=cv2.contourArea)

        # Suavizar el contorno para evitar saltos
        epsilon = 0.01 * cv2.arcLength(largest_contour, True)
        smooth_contour = cv2.approxPolyDP(largest_contour, epsilon, True)

        # Generar puntos interpolados entre los puntos del contorno suavizado
        interpolated_points = []
        for i in range(len(smooth_contour) - 1):
            # Puntos inicial y final
            x1, y1 = smooth_contour[i][0]
            x2, y2 = smooth_contour[i + 1][0]

            # Interpolar entre los puntos
            for t in np.linspace(0, 1, num=20):  # 20 puntos interpolados entre cada segmento
                x = int((1 - t) * x1 + t * x2)
                y = int((1 - t) * y1 + t * y2)
                interpolated_points.append((x, y))

        # Crear una copia de la imagen para mostrar el recorrido
        traced_image = image.copy()

        # Variables para calcular la dirección
        previous_x = None
        previous_y = None

        # Recorrer los puntos interpolados y mostrar el "shape" en movimiento
        for x, y in interpolated_points:
            frame = traced_image.copy()

            # Dibujar el círculo rojo en el punto actual
            cv2.circle(frame, (x, y), 10, (0, 0, 255), -1)  # Radio de 10 px para mejor visibilidad

            # Determinar dirección (Izquierda, Derecha, Recto)
            if previous_x is not None and previous_y is not None:
                delta_x = x - previous_x
                delta_y = y - previous_y

                # Detectar "recto" si los cambios son pequeños en ambas direcciones
                if abs(delta_x) < 5 and abs(delta_y) < 5:
                    direction = "Recto"
                elif delta_x > 5:  # Movimiento hacia la derecha
                    direction = "Derecha"
                elif delta_x < -5:  # Movimiento hacia la izquierda
                    direction = "Izquierda"
                else:
                    direction = "Recto"
            else:
                direction = "Inicio"

            # Actualizar las coordenadas previas
            previous_x, previous_y = x, y

            # Agregar tooltip con coordenadas y dirección
            tooltip_text = f"({x}, {y}) - {direction}"
            cv2.putText(frame, tooltip_text, (x + 20, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

            # Mostrar la imagen actualizada
            cv2.imshow("Recorriendo la Línea", frame)

            # Pausar para simular movimiento lento
            time.sleep(1.5)  # 1.5 segundos por punto para mayor lentitud

            # Salir si se presiona 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    else:
        print("No se detectó ninguna línea azul.")

    # Cerrar todas las ventanas
    cv2.destroyAllWindows()

# Ruta de la imagen
image_path = "C:/almacenes/openCV/katana/imagen.png"
simulate_with_tooltip(image_path)
