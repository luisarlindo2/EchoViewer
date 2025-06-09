# Transcritor de Áudio com Whisper (Python)

:contentReference[oaicite:1]{index=1}

---

## 📌 Funcionalidades

- :contentReference[oaicite:2]{index=2}
- :contentReference[oaicite:3]{index=3}
- :contentReference[oaicite:4]{index=4}
- :contentReference[oaicite:5]{index=5}
- :contentReference[oaicite:6]{index=6}

---

## 🛠️ Requisitos

- :contentReference[oaicite:7]{index=7}
- Bibliotecas:
  ```bash
  pip install sounddevice soundfile whisper numpy
  ```

Precisa da dependencia FFmpeg (para Whisper funcionar corretamente)

🔧 Ambiente Virtual (venv)
É altamente recomendado usar um ambiente virtual para evitar conflitos:

python -m venv .venv

🏃 Uso
Com o ambiente ativado, execute:

python main.py

O fluxo será:

Seleção do dispositivo de áudio

Gravação de 15 segundos

Salvamento do arquivo WAV (nome: audio_YYYYMMDD_HHMMSS.wav)

Transcrição do áudio usando o modelo Whisper

Impressão da transcrição no console e gravação em audio\_\*.txt

⚙️ Personalizações
Duração da gravação: ajuste o valor em DURATION = 15

Taxa de amostragem: altere 44100 ou 16000 nas configurações

Modelo Whisper: substitua "tiny" por "base", "small" etc.
