# Skeleton:
# Import grpc library and generated libraries
# Create channel to server
# Create Stub Object for each service defined in .proto
# Create param of type <proto>_pb.<type>Stub (e.g., simple_pb2.EchoStub)
# Call function in stub (e.g., echostub.echo(param))
# Use return value

# run with: python3 ./simple_client.py


import grpc
import simple_pb2_grpc
import simple_pb2


def run():
    channel = grpc.insecure_channel("localhost:50051")

    echostub = simple_pb2_grpc.EchoStub(channel)

    param = simple_pb2.Message(message="HELLO")
    print("PARAM: " + str(param))

    retval = echostub.echo(param)

    print("RETVAL: " + str(retval))


if __name__ == '__main__':
    run()
