There were two examples discussed in the video - one simple, one moderate complexity. 
There is a folder for each of them.  The below describes the simple case.  
Just replace simple with moderate for all of the file names. 


Input files Created for Example:
   simple.proto, simple_server.py, simple_client.py

To take simple.proto specification that defines the schema of the communication.
   (this assumes you are in the /home/coder/project/learn/simple directory)
   python -m grpc_tools.protoc --proto_path=.  ./simple.proto --python_out=. --grpc_python_out=.

Note: you need to install the grpc tools:
   python -m pip install grpcio
   python -m pip install grpcio-tools

   See: https://grpc.io/docs/languages/python/quickstart/

The files that should be generated:
   simple_pb2.py, simple_pb2_grpc.py

To run - open two terminal:
Terminal 1: 
   python3 simple_server.py 
Terminal 2:
   python3 simple_client.py
   
Note: you can run these in the vscode debugger as well if desired.
