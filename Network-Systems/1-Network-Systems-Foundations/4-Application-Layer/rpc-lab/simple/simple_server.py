import grpc
from concurrent import futures
import simple_pb2_grpc
import simple_pb2


class EchoService(simple_pb2_grpc.EchoServicer):

    def __init__(self, *args, **kwargs):
        pass

    def echo(self, request, context):
        # get the string from the incoming request
        mess = request.message
        print("Received: " + mess)

        retval = simple_pb2.Message()
        retval.message = mess

        return retval



def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    simple_pb2_grpc.add_EchoServicer_to_server(EchoService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()