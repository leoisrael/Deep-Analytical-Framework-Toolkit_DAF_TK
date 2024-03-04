import cv2
import os
import argparse

# Configurando o argparse para ler os parâmetros de entrada
parser = argparse.ArgumentParser(description='Processa um vídeo e extrai frames em intervalos especificados.')
parser.add_argument('--input_video', type=str, required=True, help='Caminho do arquivo de vídeo de entrada.')
parser.add_argument('--output_dir', type=str, required=True, help='Diretório de saída para os frames extraídos.')
parser.add_argument('--frame_interval_ms', type=int, required=True, help='Intervalo de tempo entre frames em milissegundos.')

# Lendo os argumentos passados para o script
args = parser.parse_args()

video_path = args.input_video
output_dir = args.output_dir
frame_interval_ms = args.frame_interval_ms

# Criando o diretório de saída, se não existir
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Abrindo o vídeo
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Erro ao abrir o arquivo de vídeo.")
    exit()

fps = cap.get(cv2.CAP_PROP_FPS)
frame_interval = int(fps * (frame_interval_ms / 1000))

frame_count = 0
saved_frame_count = 0

while True:
    ret, frame = cap.read()
    
    if not ret:
        break

    if frame_count % frame_interval == 0:
        frame_resized = cv2.resize(frame, (640, 480))
        frame_gray = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2GRAY)
        cv2.imwrite(f'{output_dir}/frame_gray{saved_frame_count:05d}.jpg', frame_gray)
        saved_frame_count += 1

    frame_count += 1

cap.release()
cv2.destroyAllWindows()

print(f'Frames extraídos e salvos em: {output_dir}')
