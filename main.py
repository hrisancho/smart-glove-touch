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
import config

PathConfigYamlFile = "./config.yaml"

conf = config.ConfigLoader(PathConfigYamlFile = PathConfigYamlFile)

logger.info("Config loader ")

# Описание функции для работы с приходящими данными
# Описание запуска сервиса 

# Допп:
# Описание конфига для работы сервиса в .yaml
# Описание запуска сервиса (настройка переменной среды; установка зависимостей; коныератция в wasm и запуск его)
# Написания requirements.txt (И перечисления всего что там есть с указанимем версии) 

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi import Depends, FastAPI, HTTPException
import uvicorn

app = FastAPI(title="FastAPI Application for smart-glove-touch",
              description="Sample FastAPI Application with use websocket to communicate with the hand",
              version="0.1.0", )


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []
    # Исполняется во премя присоединения клиента
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    # Исполняется после отключения от соединения клиента
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
    # Что видит сам клинет после отправки сообщения
    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)
    # Оповещает всех клинтов подключенных к соединению
    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()



import controllerProto.glove_pb2 as controller_pb2
# Злоебучий grpc, не могу импортировать из папки, так что придётся 
import grpc_pb2 as server_pb2
import grpc_pb2_grpc as server_grpc
import ast
import crcengine

@app.websocket(str(conf["web-soket-endpoint"]["imu"]))
async def websocketIMU(websocket: WebSocket):
    # await manager.connect(websocket)
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_bytes()
            logger.info(f"Data raw: {data}")
            # bytdata = ast.literal_eval(data)

            logger.info(f"Byte data: {data}")
            # Добавить распознование какое сообщение прилетает 

            # Сообщение может отправляться без crc, если в поле kind указан nothing
            msg = controller_pb2.MessageWitchCRC()
            msg.ParseFromString(data)
            logger.info(f"Mesege: {msg}")
            # TODO вынести отдельно
            if CrcValid(msg=msg):
                # IMU:  IMUPack, RadIMUDataBatch
                # Моментальная отправка сообще
                if msg.type == controller_pb2.MessageType.system:
                    msgSys = controller_pb2.System()
                    msgSys.ParseFromString(msg.msg)
                    logger.warn(msgSys.message) 
                    continue

                if msg.type == controller_pb2.MessageType.imu_pack:
                    msgImu = controller_pb2.IMUPack()
                    msgImu.ParseFromString(msg.msg)


                if msg.type == controller_pb2.MessageType.raw_imu_data_batch:
                    msgImu = controller_pb2.RadIMUDataBatch()
                    msgImu.ParseFromString(msg.msg)
                    

            else:
                logger.warn("Crc сообщений не совпадают")
                continue
        

            # EMG:  EmgPack, RawEmgDataBatch


            # await manager.send_personal_message(f"You wrote: {data}", websocket)
            # await manager.broadcast(f"{data}")

    except WebSocketDisconnect:
        try:
            manager.disconnect(websocket)
        except ValueError:
            #  TODO удалить (так как скорее всего контролер будет отключаться не дожидаясь ответа) или изменить на более поздних стадиях
            logger.info("Не удалось удалить веб-сокет, так как он не найден в списке.")

        

        logger.info(f"The client (device) has disconnected from the connection {conf['web-soket-endpoint']['imu']}")
        await manager.broadcast(f"The client (device) has disconnected from the connection {conf['web-soket-endpoint']['imu']}")

# TODO доделать, на данный момент ничего не сделано
@app.websocket(str(conf["web-soket-endpoint"]["emg"]))
async def websocketEMG(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # await manager.send_personal_message(f"You wrote: {data}", websocket)

            await manager.broadcast(f"{data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)

        logger.info(f"The client (device) has disconnected from the connection {conf['web-soket-endpoint']['emg']}")
        await manager.broadcast(f"The client (device) has disconnected from the connection {conf['web-soket-endpoint']['emg']}")
    
if __name__ == "__main__":
    # Добавить паралельный запуск grpc сервера, для работы с websoket сервером
    if conf["smart-glove-touch"]["protocol"] == "ws":
        pass
    if conf["smart-glove-touch"]["protocol"] == "udp":
        pass
    uvicorn.run("main:app", host=str(conf["smart-glove-touch"]["ip-addres"]) , port=int(conf["smart-glove-touch"]["port-ws"]), reload=True)


def CrcValid(msg:controller_pb2.MessageWitchCRC):
    if msg.kind == controller_pb2.CRCType.crc32:
        crc_algorithm = crcengine.new('crc32')
        result = crc_algorithm(msg.msg)
        return msg.crc == result

    if msg.kind == controller_pb2.CRCType.crc16:
        crc_algorithm = crcengine.new('crc16-xmodem')
        result = crc_algorithm(msg.msg)
        return msg.crc == result

    if msg.kind == controller_pb2.CRCType.nothing:
        return True

