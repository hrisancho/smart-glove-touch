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
            if keyInServece == "ip-addres":
                try:
                    ipaddress.ip_address(templates[servece][keyInServece])
                except:
                    exit(f"Ip-адрес {templates[servece][keyInServece]} который вы указали не является валидным пожалуйста проверте его на корректность в {servece} сервисе")
            # print()
            # print(map)
            # print(f" {servece} ajbs;dbc;ipab  ")
    return templates
