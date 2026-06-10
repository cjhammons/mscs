# Skeleton:
# Import grpc library and generated libraries
# Create channel to server
# Create Stub Object for each service defined in .proto
# Create param of type <proto>_pb.<type>Stub (e.g., moderate_pb2.EricStub)
# Call function in stub (e.g., ericstub.ericFunction(param))
# Use return value

# run with: python3 ./moderate_client.py


import grpc

# Import the generated modules, which will be based on the <file>.proto
# In our case, it was moderate.proto 
import moderate_pb2
import moderate_pb2_grpc


# Now you need to open a socket and use the library to make the call.

def run():
    
    # the grpc examples provide this as the sample code - which is nice and compact
#    print("Will try to greet world ...")
#    with grpc.insecure_channel("localhost:50051") as channel:
#        stub = helloworld_pb2_grpc.GreeterStub(channel)
#        response = stub.SayHello(helloworld_pb2.HelloRequest(name="you"))
#    print("Greeter client received: " + response.message)

    # For clarity, we'll break it apart piece by piece

    # Use the wrapper to open the socket to the server
    channel = grpc.insecure_channel("localhost:50051")
    
    # In the generated <name>_pb2_grpc.py there is a Stubb class for each
    # Service defined in the <name>.proto file - since we defined
    #   service Eric
    ericstub = moderate_pb2_grpc.EricStub(channel)
    # That stub has the functions you can call, as if calling them locally
    # you pass in whatever the parameter class was
    #   message FunctionParameter {
    #     string strparam = 1;
    #     int32 numparam = 2;
    #   }
    param = moderate_pb2.FunctionParameter(strparam="YEAH", numparam=999)
    # Then call the function
    retval = ericstub.ericFunction(param)
    # The return value will be a class of type defined in the proto
    #  message FunctionReturnVal { 
    #    int32 code = 1;
    #  } 
    # can print out like: 
    print("RET: " + str(retval.code))
    # or could do something like:
    print(str(retval))


    myfunctionstub = moderate_pb2_grpc.MyFunctionsStub(channel)
    ret1 = myfunctionstub.myfunction1(moderate_pb2.FunctionParameter(strparam="SOMETHING", numparam=888))
    ret2 = myfunctionstub.myfunction2(moderate_pb2.FunctionParameter(strparam="SOMETHING2", numparam=8882))
    
    channel.close()

if __name__ == "__main__":
    run()


