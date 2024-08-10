import controllerProto.glove_pb2 as glove_pb2 
import ast

from websockets.sync.client import connect
import crcengine

sysmsg = glove_pb2.System(
    message = "Првиет мир"
)


bitsys = sysmsg.SerializeToString()


crc_algorithm = crcengine.new('crc32')
result = crc_algorithm(bitsys)

msg = glove_pb2.MessageWitchCRC(
            msg = bitsys,
            kind = glove_pb2.CRCType.crc32,
            crc = result,
            type = glove_pb2.MessageType.system
)

print(type(msg))

with connect("ws://127.0.0.1:8000/ws/imu") as websocket:

        
        bitmsg = msg.SerializeToString()
        websocket.send(bitmsg)
        # message = websocket.recv()
        print(f"Received: {bitmsg}")


        websocket.close()





# ws.send("Hello, World")
print ("Sent")
print ("Receiving...")
