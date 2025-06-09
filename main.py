import os
import sounddevice as sd
import soundfile as sf
import whisper
import numpy as np
from datetime import datetime

def selecionar_dispositivo():
    """Mostra dispositivos de entrada disponíveis e permite seleção"""
    print("\nDispositivos de entrada disponíveis:")
    dispositivos = sd.query_devices()
    entradas = [i for i, dev in enumerate(dispositivos) if dev['max_input_channels'] > 0]
    
    for i in entradas:
        print(f"{i}: {dispositivos[i]['name']}")
    
    while True:
        try:
            escolha = int(input("\nDigite o número do dispositivo: "))
            if escolha in entradas:
                return escolha
            print("Número inválido. Tente novamente.")
        except ValueError:
            print("Digite apenas números.")

def gravar_audio():
    """Captura áudio do dispositivo selecionado com configurações otimizadas"""
    dispositivo = selecionar_dispositivo()
    nome_dispositivo = sd.query_devices(dispositivo)['name']
    duracao = 15  # segundos
    taxa = 44100  # 44.1kHz para melhor qualidade

    print(f"\nGravando {duracao} segundos do {nome_dispositivo}...")
    print("Fale agora... (aguarde o término da gravação)")

    # Configurações de gravação
    audio = sd.rec(
        int(duracao * taxa),
        samplerate=taxa,
        channels=1,
        dtype='int16',
        device=dispositivo
    )
    sd.wait()  # Aguarda término da gravação

    # Processamento do áudio gravado
    max_val = np.max(np.abs(audio))
    if max_val > 0:
        audio = audio / (max_val * 1.2)  # Normalização para 80% do volume máximo
    
    return audio, taxa

def salvar_audio(audio, taxa):
    """Salva o áudio em arquivo WAV com verificação"""
    arquivo = f"audio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
    
    try:
        sf.write(arquivo, audio, taxa)
        print(f"\nÁudio salvo como: {os.path.abspath(arquivo)}")
        print(f"Tamanho do arquivo: {os.path.getsize(arquivo)} bytes")
        return arquivo
    except Exception as e:
        raise Exception(f"Erro ao salvar áudio: {str(e)}")

def transcrever(arquivo):
    """Realiza a transcrição usando Whisper com tratamento de erros"""
    print("\nCarregando Whisper...")
    
    try:
        # Verifica se o arquivo existe
        if not os.path.exists(arquivo):
            raise FileNotFoundError(f"Arquivo não encontrado: {os.path.abspath(arquivo)}")
        
        # Carrega modelo (usando base como padrão)
        modelo = whisper.load_model("base")
        
        print("Processando áudio... (isso pode levar alguns instantes)")
        
        # Transcrição com parâmetros otimizados
        resultado = modelo.transcribe(
            os.path.abspath(arquivo),
            language="pt",
            fp16=False,  # Desativa FP16 para compatibilidade com CPU
            verbose=True  # Mostra progresso
        )
        
        # Exibe e salva resultados
        print("\n" + "="*50)
        print("TRANSCRIÇÃO COMPLETA:")
        print(resultado["text"])
        print("="*50)
        
        txt_file = os.path.abspath(arquivo.replace(".wav", ".txt"))
        with open(txt_file, "w", encoding="utf-8") as f:
            f.write(resultado["text"])
        print(f"\nTranscrição salva em: {txt_file}")
        
        return resultado["text"]
    except Exception as e:
        raise Exception(f"Erro na transcrição: {str(e)}")

def main():
    """Função principal do programa"""
    print("=== TRANSCRITOR DE ÁUDIO ===")
    print("Selecione seu microfone e aguarde a transcrição\n")
    
    try:
        # 1. Gravação do áudio
        audio, taxa = gravar_audio()
        
        # 2. Salvamento do arquivo
        arquivo = salvar_audio(audio, taxa)
        
        # 3. Transcrição
        transcrever(arquivo)
        
    except Exception as e:
        print(f"\nERRO: {str(e)}")
        print("\nSoluções possíveis:")
        print("- Verifique se o arquivo de áudio foi criado")
        print("- Confira as permissões do diretório")
        print("- Tente executar como administrador")
    finally:
        input("\nPressione Enter para sair...")

if __name__ == "__main__":
    # Verifica dependências necessárias
    try:
        import sounddevice
        import whisper
    except ImportError:
        print("Erro: Bibliotecas necessárias não instaladas.")
        print("Execute: pip install sounddevice whisper")
        exit(1)
    
    main()