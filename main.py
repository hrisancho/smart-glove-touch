# Инициализация логера 
import logging
import sys

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler(sys.stdout)
log_formatter = logging.Formatter("%(asctime)s [%(processName)s: %(process)d] [%(levelname)s]: %(message)s")
stream_handler.setFormatter(log_formatter)
logger.addHandler(stream_handler)
logger.info("Init logger")

# Проверка файла конфигурации 

# Описание функции для работы с приходящими данными
# Описание запуска сервиса 

# Допп:
# Описание конфига для работы сервиса в .yaml
# Описание запуска сервиса (настройка переменной среды; установка зависимостей; коныератция в wasm и запуск его)
# Написания requirements.txt (И перечисления всего что там есть с указанимем версии) 

from fastapi import Depends, FastAPI, HTTPException
import uvicorn

app = FastAPI(title="Sample FastAPI Application",
              description="Sample FastAPI Application with Swagger and Sqlalchemy",
              version="1.0.0", )



    
if __name__ == "__main__":
    uvicorn.run("main:app", port=9000, reload=True)