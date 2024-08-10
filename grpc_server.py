import grpc_pb2
import grpc_pb2_grpc

class Touch(grpc_pb2_grpc.TouchServicer):
    def SentMessage(self, request, context):
        return None