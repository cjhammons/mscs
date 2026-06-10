# Skeleton
# Import grpc, concurrent, and generated libraries
# Create Class for each service specified in .proto
# Create function for each function specified in .proto
  # input: request is of type <proto>_pb.<type> (e.g., moderate_pb2.FunctionParameter)
  # return object of type <proto>_pb.<type> (e.g., moderate_pb2.FunctionReturnVal)

# run with: python3 ./moderate_server.py

import grpc
from concurrent import futures

# Whatever your <file>.proto was called, 
# <file>_pb2.py and <file>_pb2_grpc.py are created
# In this case: we used moderate.proto
import moderate_pb2_grpc
import moderate_pb2


# For each service specified in your .proto, you need to create a class
# Good choice for a name will be <ServiceName>Service
# in moderate.proto - service MyFunctions {
# so we defined a class - MyFunctionsService
# Note class MyFunctionsServicer(object) was defined in the generated moderate_pb2_grpc.py
# That becomes the parent to this class (put it in parentheses)
class MyFunctionsService(moderate_pb2_grpc.MyFunctionsServicer):

    # Needed init function
    def __init__(self, *args, **kwargs):
        pass

    
    # For each function defined within the service, you need a function in the class
    # This has to be named exactly what you called it in the .proto file
    # Note in the generated moderate_pb2_grpc.py, in the parent MyFunctionsServicer class,
    #   these functions are defined there.
    # The function will have these as its parameters (self, request, context).
    def myfunction1(self, request, context):
        # request will be the type defined in the proto file.
        # in this case, it was FunctionParameter
        # message FunctionParameter {
        #  string strparam = 1;
        #  int32 numparam = 2;
        # }
        # request will be a class with variables strparam and numparam in it
        print("Called myFunction1")
        print(request.strparam) 
        print(request.numparam)

        # For the return value, you return an object of type defined in the proto file
        # message FunctionReturnVal { 
        #    int32 code = 1;
        # } 
        retval = moderate_pb2.FunctionReturnVal()
        retval.code = 111
        return retval

    def myfunction2(self, request, context):
        print("Called myFunction2")
        print(request.strparam) 
        print(request.numparam)
        # a short hand alternative
        return moderate_pb2.FunctionReturnVal(code=99)


        return simple_pb2.Message(**result)


# Since moderate.proto had 2 services defined (MyFunction, defined above, and Eric, defined here)
class EricService(moderate_pb2_grpc.EricServicer):
    def __init__(self, *args, **kwargs):
        pass
    
    # One function was defined (ericFunction) and the parameter was the same as the other functions
    # so the code will look similar
    # But this isn't a requirement.
    def ericFunction(self, request, context):
        print("Called ericFunction")
        print(request.strparam) 
        print(request.numparam)
        # a short hand alternative
        return moderate_pb2.FunctionReturnVal(code=55)


# Last thing to add is the code to open up the socket
# It'll be wrapped in some grpc library code, and the below
# is a standard template you can use.

def serve():
    # standard code to define the server
    port = "50051"  # Set to whatever you want
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    # Here you need to add the classes you created to the server 
    # For each service, generated in <protoname>_pb_grpc.py will be functions:
    #   add_<ServiceName>_to_server which take in the class you created and the server (created above)
    moderate_pb2_grpc.add_EricServicer_to_server(EricService(), server)
    moderate_pb2_grpc.add_MyFunctionsServicer_to_server(MyFunctionsService(), server)


    # Then standard code to start the server and wait for connections
    server.add_insecure_port("[::]:" + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()


if __name__ == "__main__":
    serve()

