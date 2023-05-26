import logging
import os
import datetime

# Crie o diretório logs se não existir
log_dir = os.path.dirname(os.path.abspath(__file__))
os.makedirs(log_dir, exist_ok=True)

# Configuração global do logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s - %(filename)s - %(message)s',
    handlers=[
        logging.FileHandler(f'{log_dir}/app.log'),
        logging.StreamHandler()
    ]
)

# Obtém o logger para o projeto
logger = logging.getLogger('Social')

# Adiciona um filtro para incluir a data e hora atual e o nome do arquivo no log
class FileContextFilter(logging.Filter):
    def filter(self, record):
        record.filename = os.path.relpath(record.pathname, log_dir)
        record.asctime = datetime.datetime.fromtimestamp(record.created).strftime('%Y-%m-%d %H:%M:%S')
        return True

logger.addFilter(FileContextFilter())
