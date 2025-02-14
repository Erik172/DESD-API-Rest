import os
import grpc
import converter_pb2
import converter_pb2_grpc

CONVERTER_GRPC_HOST = os.getenv('CONVERTER_GRPC_HOST', 'converter:50051')

def convert_file_grpc(file_bytes, file_name):
    """Envía el archivo al microservicio de conversión (gRPC)."""
    max_message_length = 1024 * 1024 * 1024  # 1GB
    options = [
        ('grpc.max_send_message_length', max_message_length),
        ('grpc.max_receive_message_length', max_message_length),
    ]
    with grpc.insecure_channel(CONVERTER_GRPC_HOST, options=options) as channel:
        stub = converter_pb2_grpc.ConverterStub(channel)
        response = stub.ConvertFile(converter_pb2.ConvertRequest(file_content=file_bytes, file_name=file_name))
        return response.images