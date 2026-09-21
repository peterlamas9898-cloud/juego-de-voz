import random
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import speech_recognition as sr
from googletrans import Translator

# Diccionario de palabras por nivel
words_by_level = {
    "facil": ["gato", "perro", "manzana", "leche", "sol"],
    "medio": ["banano", "escuela", "amigo", "ventana", "amarillo"],
    "dificil": ["tecnologia", "universidad", "informacion", "pronunciacion", "imaginacion"]
}

# Configuración de audio
duration = 5  # segundos de grabación
sample_rate = 44100
translator = Translator()

print("========================================================")
print("                  🎯 HABLA CORRECTO 🎯                  ")
print("========================================================")

# 1. Selección de dificultad
print("Selecciona el nivel de dificultad:")
print("1. facil")
print("2. medio")
print("3. dificil")

opcion = input("\nEscribe el nivel (facil, medio, dificil): ").strip().lower()

if opcion not in words_by_level:
    print("Nivel no válido. Se asignará 'facil' por defecto.")
    opcion = "facil"

puntos = 0
errores = 0
MAX_ERRORES = 3

print(f"\n🎮 ¡Nivel {opcion.upper()} seleccionado! El juego termina con 3 errores.")
print("--------------------------------------------------------")

# Bucle principal de juego (hasta llegar a 3 errores)
while errores < MAX_ERRORES:
    # Seleccionar palabra aleatoria
    palabra_es = random.choice(words_by_level[opcion])
    
    # Obtener traducción esperada en inglés
    traduccion_esperada = translator.translate(palabra_es, src='es', dest='en').text.lower()

    print(f"\n👉 Pronuncia en INGLÉS la traducción de: 【 {palabra_es.upper()} 】")
    print("🎙️ Habla ahora...")

    # Grabación de audio
    recording = sd.rec(
        int(duration * sample_rate),
        samplerate=sample_rate,
        channels=1,
        dtype="int16"
    )
    sd.wait()

    # Guardar audio
    wav.write("output.wav", sample_rate, recording)
    print("✅ Grabación completa, procesando...")

    # Reconocimiento de voz
    recognizer = sr.Recognizer()
    with sr.AudioFile("output.wav") as source:
        audio = recognizer.record(source)

    try:
        # Transcribir voz en inglés (en-US)
        recognized = recognizer.recognize_google(audio, language="en-US")
        recognized = recognized.lower()  # Convertir todo a minúsculas
        
        print("🗣️ Dijiste:", recognized)
        print("💡 Esperado:", traduccion_esperada)

        # Comparación
        if recognized == traduccion_esperada:
            puntos += 10
            print("   (^o^) / ¡CORRECTO! +10 puntos")
        else:
            errores += 1
            print(f"   (x_x) INCORRECTO. Llevas {errores}/{MAX_ERRORES} errores.")

    except sr.UnknownValueError:
        errores += 1
        print(f"🔊 No se pudo entender el habla. Llevas {errores}/{MAX_ERRORES} errores.")
    except sr.RequestError as e:
        print(f"⚠️ Error del servicio: {e}")

    print(f"📊 Puntuación actual: {puntos} | Errores: {errores}/{MAX_ERRORES}")

# Fin del juego al acumular 3 errores
print("\n========================================================")
print("🏁 ¡FIN DEL JUEGO! Has alcanzado el límite de 3 errores.")
print(f"🏆 Puntuación final: {puntos} puntos")
print("========================================================\n")