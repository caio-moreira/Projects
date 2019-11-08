import os
import numpy as np
import cv2
from PIL import Image as img


# "Global" variables, containing the paths of the most relevant directories
current_file_path = os.path.dirname(__file__)
image_path = os.path.join(current_file_path, "images")
result_path = os.path.join(current_file_path,"faces")
training_data = os.path.join(current_file_path,"training_data")

def save_faces(cascade_classifier, img_name):
    """ Function that saves all the faces in a given image.

    This function selects every face detected in a given image and saves it.
  
    Keyword arguments: 
        cascade_classifier -- the object of the cascade classifier
        img_name -- name of the image.
    """
    
    # Opening the image and converting it to grayscale, then converting it to a numpy array
    image = img.open(os.path.join(image_path, img_name)).convert('L')
    image_array = np.array(image, 'uint8')

    #Codigo que itera em cada rosto encontrado na foto aberta acima
    for i, face in enumerate(cascade_classifier.detectMultiScale(image_array)):
        #Salva as coordenadas da sub imagem encontrada
        x, y, w, h = face
        
        #Salva a sub imagem encontrada na variavel abaixo usando as coordenadas
        sub_face = image_array[y:y + h, x:x + w]

        #Cria a pasta de resultados caso nao exista
        if not os.path.exists(result_path):
            os.makedirs(result_path)

        #Salva a imagem na pasta criada acima
        cv2.imwrite(os.path.join(result_path, "{}_0{}.jpg".format(img_name, i)), sub_face)


if __name__ == "__main__":
    
    #Inicializa o classificador em cascata atraves do path do arquivo
    face_cascade = os.path.join(current_file_path, "haarcascade_frontalface_default.xml")
    cascade_classifier = cv2.CascadeClassifier(face_cascade)

    #Itera pelas imagens na pasta image_path e segmenta cada uma delas
    for f in [f for f in os.listdir(image_path) if os.path.isfile(os.path.join(image_path, f))]:
        #Chama a funcao que segmenta e salva as sub faces
        save_faces(cascade_classifier, f)

    #Cria o reconhecedor que usa o algoritmo LBPH
    face_recognizer = cv2.face.LBPHFaceRecognizer_create()
    
    #Inicializa o dicionario da turma para que se possa dar a presença depois
    turma = {}

    #Inicializa os vetores que vao guardar as faces para treinamento e os nomes das faces
    faces = []
    labels = []

    #Itera por cada pasta de sujeito na pasta de treinamento
    for i, subject in enumerate(os.listdir(training_data)):
        
        #Adiciona o nome do sujeito como chave no dicionario da turma com o valor default "Faltou"
        turma[str(subject)] = "Faltou"

        #Cria uma variavel que tem o path para o sujeito atual
        local_path = os.path.join(training_data, subject)

        #Itera em cada foto de treinamento do sujeito atual no path dele
        for face in os.listdir(local_path):

            #Inicializa e converte a imagem como na funcao save_faces
            face_file = img.open(os.path.join(local_path, face)).convert('L')
            face_final = np.array(face_file, 'uint8')

            #Segmenta a imagem, que so tem um rosto, o do sujeito, para armazena-la
            face_points = cascade_classifier.detectMultiScale(face_final)
            #Salva as coordenadas do rosto segmentado
            x, y, w, h = face_points[0]
            #Adiciona na lista de faces o rosto segmentado atraves de suas coordenadas
            faces.append(face_final[y:y + h, x:x + w])
            #Adiciona o nome do sujeito no array de nomes para dar nome a face encontrada acima
            #Converte para int por causa das restricoes de tipo do metodo de treinamento abaixo
            labels.append(int(subject))

    #Treina o reconhecedor com os arrays inicializados acima
    face_recognizer.train(faces, np.array(labels))

    #Passa por cada rosto no path de resultados, que contem os rostos segmentados da imagem da sala
    for face_file in os.listdir(result_path):

        #Carrega a imagem
        face = cv2.imread(os.path.join(result_path, face_file))
        
        #Converte ela para grayscale(nivel de cinza)
        gray = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)

        #Prediz qual pessoa esta na imagem, poe o resultado no formato de tupla de duas posicoes
        prediction = face_recognizer.predict(gray)

        #Salva o nome e a confianca, que estao na primeira e segunda posicao da tupla, respectivamente
        name = str(prediction[0])
        confidence = prediction[1]

        #Printa os resultados para avaliacao
        #print(name, confidence)
        
        #Da a presenca para o aluno predito
        turma[name] = "Presente"
        
        #Cria uma janela nomeada com o nome predito pelo algoritmo
        cv2.namedWindow(name, cv2.WINDOW_NORMAL)
        #Posiciona essa janela na posicao (100, 100) do monitor
        cv2.moveWindow(name, 100, 100)
        #Mantem a janela com tamanho e proporcoes normais, evitando a tela cheia, que pode distorcer a imagem
        cv2.setWindowProperty(name, cv2.WINDOW_NORMAL, cv2.WINDOW_KEEPRATIO)
        #Mostra a janela nomeda no monitor, com a foto que foi usada para predizer
        #Possibilita a avaliacao da precisao do algoritmo
        cv2.imshow(name, face)
        #Metodo que espera qualquer tecla ser pressionada para dar prosseguimento ao codigo
        cv2.waitKey(0)
        #Metodo que fecha todas as janelas abertas pelo metodo cv2.imshow()
        cv2.destroyAllWindows()
        
    print()
    #Printa o dicionario da turma para avaliacao dos resultados
    for aluno in turma:
        print(aluno, turma[aluno])