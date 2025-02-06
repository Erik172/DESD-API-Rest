from concurrent import futures
import grpc
import converter_pb2
import converter_pb2_grpc
from pdf2image import convert_from_bytes
from PIL import Image, ImageSequence
import io

class ConverterServicer(converter_pb2_grpc.ConverterServicer):
    def ConvertFile(self, request, context):
        file_content = request.file_content
        file_name = request.file_name.lower()
        images = []

        if file_name.endswith('.pdf'):
            images = convert_from_bytes(file_content)
        elif file_name.endswith('.tif') or file_name.endswith('.tiff'):
            with io.BytesIO(file_content) as file:
                tiff_image = Image.open(file)
                images = [page.convert("RGB") for page in ImageSequence.Iterator(tiff_image)]

        jpg_images = []
        for image in images:
            with io.BytesIO() as output:
                image.save(output, format="JPEG")
                jpg_images.append(output.getvalue())

        return converter_pb2.ConvertResponse(images=jpg_images)

def serve():
    # 1GB
    max_message_length = 1024 * 1024 * 1024
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10),
        options=[
            ('grpc.max_send_message_length', max_message_length),
            ('grpc.max_receive_message_length', max_message_length),
        ]
    )
    converter_pb2_grpc.add_ConverterServicer_to_server(ConverterServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()