import controllerProto.glove_pb2 as glove_pb2 

# msg = glove_pb2.System()
# msg.message = "fun"

# print(msg)



# bytMsg = msg.SerializeToString()
# print(bytMsg)
# print(type(bytMsg))
# print(str(bytMsg))

# df = '\n\x03fun'

# msg = glove_pb2.System()
# msg.ParseFromString(str.encode('\n\x03fun'))

# print(f"Mesege: {msg}")

import ast

# Исходная строка
df = "b'\\n\\x03fun'"

# Преобразование строки в bytes
byte_data = ast.literal_eval(df)

# Проверка результата
print(byte_data)  # Вывод: b'\n\x03fun'
print(type(byte_data))  # Вывод: <class 'bytes'>


# print(df.decode("utf-8")) 
# df2 = str.encode(df)
# print(df2)

msg = glove_pb2.System()
msg.ParseFromString(byte_data)

# print(f"Mesege: {msg}")
