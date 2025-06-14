import serial
import logging
from datetime import datetime
from db_manager import DatabaseManager

# Configurações
PORTA_SERIAL = "rfc2217://localhost:5000"
COD_MAQUINA = "maq001"
ORDEM_PRODUCAO = "OP00123"
DISTANCIA_MIN = 5.0
DISTANCIA_MAX = 100.0

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

def detectar_folha(distancia, estado):
    """
    Detecta uma nova folha baseada na distância e atualiza o estado.
    """
    if estado["ultima_posicao"] == "inicio" and distancia > DISTANCIA_MAX:
        estado["ultima_posicao"] = "meio"
    elif estado["ultima_posicao"] == "meio" and distancia < DISTANCIA_MIN:
        estado["ultima_posicao"] = "inicio"
        estado["folhas"] += 1
        logging.info(f" Nova folha registrada! Total: {estado['folhas']}")
    return estado["folhas"]

def processar_linha(linha, estado, db):
    """
    Processa uma linha vinda do sensor, valida e armazena os dados.
    """
    try:
        distancia = float(linha.strip())
        data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        folha = detectar_folha(distancia, estado)

        logging.info(f"[{data_hora}] {distancia:.1f} cm | OP={ORDEM_PRODUCAO} | folhas={folha}")
        
        db.inserir_leitura(
            cod_maquina=COD_MAQUINA,
            ordem_producao=ORDEM_PRODUCAO,
            data_hora=data_hora,
            distancia=distancia,
            folhas=folha
        )
    except ValueError:
        logging.warning(f"Linha inválida recebida do sensor: {linha.strip()}")

def monitorar_sensor():
    """
    Função principal que conecta ao sensor e inicia o monitoramento contínuo.
    """
    logging.info(" Iniciando monitoramento do sensor...")

    estado = {
        "ultima_posicao": "inicio",
        "folhas": 0
    }

    try:
        with serial.serial_for_url(PORTA_SERIAL, baudrate=9600, timeout=1) as ser, \
             DatabaseManager("dados_sensor.db") as db:
            
            logging.info(" Conectado ao sensor via RFC2217")
            logging.info(" Monitorando sensor...\n")

            while True:
                linha = ser.readline().decode().strip()
                if linha:
                    processar_linha(linha, estado, db)

    except KeyboardInterrupt:
        logging.info("\n Monitoramento encerrado pelo usuário.")
    except serial.SerialException as e:
        logging.error(f"Erro na comunicação serial: {e}")
    except Exception as e:
        logging.exception("Erro inesperado durante a execução:")
