import yaml
from pprint import pprint
import logging
import socket
import ipaddress

def ConfigLoader(PathConfigYamlFile:str):
    try:
        with open(PathConfigYamlFile) as f:
            templates = yaml.safe_load(f)
    except:
        exit(f"Не правильный путь до файла config.yaml {PathConfigYamlFile}. Проверте его он должен включать в себя путь + название то есть /path/to/config.yaml расширение обязательно должно быть yaml, а файл может называться как угодно")
    
    for servece in templates:
        for keyInServece in templates[servece]:
            # Проверка ip адреса 
            if keyInServece == "ip-addres":
                try:
                    ipaddress.ip_address(templates[servece][keyInServece])
                except:
                    exit(f"Ip-адрес {templates[servece][keyInServece]} который вы указали не является валидным пожалуйста проверте его на корректность в {servece} сервисе")
            # Проверка grpc для максимального колличеста обрабатываемых запросов
            if keyInServece == "max-workers":
                if templates[servece][keyInServece] == None:
                    exit(f"Вы не указали такой параметр как max-workers он нужен для работы grpc сервиса, пожалйста укажите его в поле {servece} в файле /path/to/config.yaml")
                if templates[servece][keyInServece] == int:
                    exit(f"Вы указали не правильный тип данных для в парметре max-workers, так как он должен быть типа int, а у вас он{type(templates[servece][keyInServece])}, пожалуста исправте это в конфигурационном файле config.yaml")
            # Проверка типа протокола для общения с контроллером
            if keyInServece == "protocol":
                if templates[servece][keyInServece] not in ["ws","udp"]:
                    exit(f'Вы указали не правильный протокол для общения с контроллером, в данный момент параметр protocol в config.yaml имеет значение {templates[servece][keyInServece]} выберите параметр "ws" или "udp" и укажите его')

    if templates["smart-glove-touch"]["port-ws"] == templates["smart-glove-touch"]["port-grpc"]:
        exit(f"Укажите разные порты в config.yaml на которых будет работать gRPC и WebSoket сервисы в данный момент gRPC работает на {templates['smart-glove-touch']['port-grpc']} порту, а WebSoket на {templates['smart-glove-touch']['port-ws']} порту")
                
    return templates
