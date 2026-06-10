Module 4: Application Layer 
---

# Intro 
## Problem 1: Addressing

- IP Addressing isn't Human readable (want to go to youtube.com)
- IP address represents a single machine. YouTube has many servers 

## Problem 2: Programming 

- Link, network, and transport layer protocols are concepts, and the operating system network stack is their implementation
- How do we write programs to interface to this network?

## Problem 3: Application-level protocol 

- How should the process communicate what they want 
- How do processes encode data 

# Domain Name System (DNS)

- IP and MAC addresses are machine-readable.
- Hostnames are meant to be human readable and variable length 

## DNS Fundamentals 

- Distributed database of mappings between hostnames and IP addresses 
- application layer protocol running on UDP 
- **Resource Records (RR)**: Fundamental unit of storage in DNS
    - Format: (name, value, type, ttl)
    - **Type A**
        - Name - hostname 
        - Value - IP Address 
    - **Type NS**:
        - Name - domain 
        - Value - hostname of authoritative name server for this domain 

## Name Servers 

### Hierarchy:

1. Root DNS Servers
    - 13 known root servers 
    - DNS is critical infrastructure for the internet / web
    - known set of 13 root servers (IP addresses are configured in resolvers 
    - Each root server is replicated for reduncancy
2. Top-Level domain (TLD):
Domains like .com, .edu, .org 
3. Authoritative DNS server: hold the actual records for specific domains (e.g. dns.cs.umass.edu) 
4. Local DNS server (Resolver): first point of contact for a host. Often provided by ISP or university 

### Query modes 

- **Recursive Query**: local DNS server takes full responsibility for finding the answer and returning the final result to host 
- **Iterative Query**: a server responds with the best answer it has (often a referral to another server) rather than doing the full lookup itself 

## DNS Resolution process 

**Scenario**: a host at `engineering.nyu.edu` wants to find `gaia.cs.umass.edu` 
1. Host sends query to Local DNS server 
2. Local DNS server queries a Root Server 
3. Root server refers to the .edu TLD Server 
4. Local DNS server queries the .edu TLD server 
5. TLD server refers to the Authoritative Server (dns.cs.umass.edu)
6. Local DNS server quereis the Authoritative Server 
7. Authoritative server returns the IP address 
8. Local DNS server caches the result and returns it to host 

## Any Cast 

- Advertises a single IP prefix from multiple distinct locations
- Hosts trying to reach that prefix will (hopefully) go to the closest one 

## Message format 

Query and reply have same format 

### Structure 

- Identification: matches quereis to replies 
- Flags: indicates if its a query or reply, recursion desired, etc
- Questions: hostname being looked up 
- Answers: resource records answering the query 
- Authority: name servers that are authoritative for the domain (used when the resolver doesn't have the answer) 
- Additional: extra info to prevent further lookups (e.g., the IP address of the name server listed in the Authority section 

### Caching

Records can be cached at various levels to improve performance and reduce load 

### Questions 

- Contains a query of the hostname being looked up 

**Resource Record (RR) fields**

Field | Description | Length 
--- | --- | ---
NAME | Name of the requested Resource | Variable 
TYPE | Type of RR (A, AAAA, TXT, etc) | 2

Example query: 

```
queries
    www.google.com: type A, class IN 
    Type: A (Host Address)
    class: IN (0x0001)
```

### Answers 

- Response to queries if resolver has the answer 

Field | Description | Length 
--- | --- | --- 
NAME | Name of the node to which this record pertains | Variable 
TYPE | Type of RR in numeric form (e.g. 15 for MX RRs) | 2
CLASS | class code | 2 
TTL | Count of seconds the RR stays valid (Max is 2^31 - 1, which is about 68 years) | 4 
RDLENGTH | Length of RDATA field (specified in octets) | 2 
RDATA | Additional RR-specific data | variable, as per RDLENGTH 

Example query: 

```
Answers 
    www.google.com: type A, class IN, addr 74.125.131.147 
        Name: www.google.com
        Type: A (Host address) 
        class: IN (0x0001)
        Time to live: 5 minutes 
        Data length: 4 
        addr: 74.125.131.147 (74.125.131.147)
    www.google.com: type A, class IN, addr 74.125.131.103
    www.google.com: type A, class IN, addr 74.125.131.104
    www.google.com: type A, class IN, addr 74.125.131.106
    www.google.com: type A, class IN, addr 74.125.131.99 
    www.google.com: type A, class IN, addr 74.125.131.105 
```

### Authority 

If resolver doesn't know the answer, it responds with a name server that it knows is authoritative for the name or part of the name 

Example:

```
Authoritative nameservers:
    google.com: type NS, class IN, ns ns2.google.com 
        Name: google.com 
        Type: NS (Authoritative name server)
        class: IN (0x0001)
        Time to live: 2 days 
        Data length: 6
        Name Server: ns2.google.com 
```

### Additional 

- to help prevent further lookups, if the resolver can resolve the address of the nameserver in the authority record, it includes as an additional record 

example 

```
Additional Records 
    ns2.google.com: type A, class IN, addr 216.239.34.10
        Name: ns2.google.com 
        Type: A (Host Address)
        class: IN (0x0001)
        Time to live: 2 days 
        Data Length: 4
        Addr: 216.239.34.10
```

# Socket Programming 

Problem: programming 

- Link, Network, and transport protocols are concepts. Operating system network stack is their implementation 
- How do we write programs to interface to this network stack?

## Socket Fundamentals 

A socket is an abstract representation for the local endpoint of a network communication path 

### Funcionality 

- One application puts data into a socket 
- Another application gets data from the socket 
- Everything below this interface is handles by the OS and network protocols 

### Layers of Control 

- Application Developer: controls socket layer and above 
- Operating System: Controls transport layer and below 

## Berkely Sockets 

- Originated in 1983 and has been standard since 
- Socket is an abstract representation for the local endpoint of a network communication path 
- App puts data into socket, other app gets data from socket 


## Client-Server Model 

- Client: entity that initiates a connection 
- Server: entity that accepts connection 
- After connection is established (e.g. TCP 3-way handshake), they can communicate bidirectionally 

## TCP Server Window 

Function |	Description
--- | ---
socket() |	Creates a socket; returns a handle (file descriptor). Specifies IP version (IPv4/IPv6) and type (TCP stream / UDP datagram).
bind()	| Tells the OS which address (IP + Port) to use. E.g., port 80 for HTTP, port 22 for SSH.
listen() |	Notifies OS of willingness to accept incoming connections on this socket. Sets backlog size.
accept() |	Blocks waiting for connections. Returns client address information when a connection arrives.
recv()/send() |	Read/write calls to exchange data with the connected client.
close()	| Closes the socket, sending TCP FIN to terminate the connection.

### Python Server Example

```Python
import socket


def server_program():
    # get the hostname
    host = socket.gethostname()
    port = 5000  # initiate port no above 1024

    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(2)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))
    while True:
        # receive data stream. it won't accept data packet greater than 1024 bytes
        data = conn.recv(1024).decode()
        if not data:
            # if data is not received break
            break
        print("from connected user: " + str(data))
        data = input(' -> ')
        conn.send(data.encode())  # send data to the client

    conn.close()  # close the connection


if __name__ == '__main__':
    server_program()
```

## TCP Client Window 

Function |	Description
--- | ---
socket() |	Creates a socket and gets a file descriptor (similar to server).
connect() |	Initiates connection to a specific server address (IP + Port). Unique to TCP. Triggers 3-way handshake.
send()/recv() |	Exchanges data after connection is established.
close()	| Closes the socket, terminating the connection.

### Client Example 

```Python 
import socket


def client_program():
    host = socket.gethostname()  # as both code is running on same pc
    port = 5000  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server

    message = input(" -> ")  # take input

    while message.lower().strip() != 'bye':
        client_socket.send(message.encode())  # send message
        data = client_socket.recv(1024).decode()  # receive response

        print('Received from server: ' + data)  # show in terminal

        message = input(" -> ")  # again take input

    client_socket.close()  # close the connection


if __name__ == '__main__':
    client_program()
```

# Application Protocol: HTTP 

**Hypertext Transfer Protocal**

## Introduction 

Problem: how do processes encode data 

An application layer protocol defines:
- Message syntax
- Types of messages exchanged 
- Message semantics: meaning of information in fields 

## Syntax: Data encoding and presentation 

- Requirement: Receiver needs to be able to execute the same message as what the transmitter sent 
- Consideration: Debuggability vs bandwidth vs processing power 

## Taxonomy of data representation

### Data Types 

Type |	Examples |	Concerns
--- | --- | ---
Base Types |	Integers, Booleans |	Number of bits (16, 32, 64), byte order (Big-endian vs. Little-endian)
Flat Types |	Arrays, Structures |	Padding, length definition, alignment boundaries
Complex Types |	Trees, Linked Lists |	Serialization/Flattening for transmission across network

### Conversion Strategy 

#### Canonical Intermediate form 

- sender converts its internal representation to some agreed upon format 
- receiveer converts aggreed-upon format to its own representation 
- both sides perform conversion 

#### Receier Makes Right 

- Sender transmits data in its internal representation 
- includes information about representation
- receiver converts from the sender's representation to its own representation (if needed)
- works well if assumption os a homogeneous infrastructure 

### Tagging 

- Untagged: Agree on type, length, and location of data 
- Tagged: Include in message tags about data (e.g. type and length) 

## HTTP Fundamentals 

- Web's applicaiton-layer protocol 
- Client / Server exchange Web Objects 
    - htlm, jpeg, audio 
- Stateless - server doesn't retain information about past client requests 

### URL Structure 

Example: http://www.example.com/path/to/file 
- `http:` protocol 
- `www.example.com`: hostname 
- `/path/to/file`: path 

### Message format 

```
START_LINE <CRLF>
MESSAGE_HEADER <CRLF>
<CRLF>
MESSAGE_BODY <CRLF>
```


Field |	Request	Response
--- | ---
Start Line	| Request type + path + version	Version + status code
Message Header |	Various info about request	Various info about response (Content-Type, etc.)
Blank Line |	Separates header from body	Separates header from body
Message Body |	Requested content or uploaded data	Web object (HTML, image, etc.)

### Message Types 

Method |	Description
--- | ---
GET	|Retrieve document identified in URL
POST  |	Send/supply information to server
PUT	| Store document under specified URL
DELETE |	Delete specified URL
HEAD	| Retrieve metainformation (no body)
OPTIONS |	Request info about available options
TRACE |	Loopback request message
CONNECT |	For use by proxies

## Data Formats in HTTP 

I skipped this part because i am already familiar with html and json 

## HTTP Versions 


Version	Main | Innovation	Impact
--- | ---
HTTP/1.0 |	First major version	New TCP connection per request (slow)
HTTP/1.1 |	Persistent Connections	Reuse TCP connection for multiple requests (avoids 3-way handshake, slow start)
HTTP/2.0 |	Multiplexed Requests	Multiple requests/responses in parallel over one connection
HTTP/3.0 |	QUIC instead of TCP	Reduced latency, improved reliability over UDP-based transport

# Application Protocol: gRPC

Problem: the application layer needs to define how processes communicate 

## Remote Procedure Call (RPC) Fundamentals 

### Concept 

- Extends the idea of a local procedure call to a remote machine.
- Defined framework for data encoding, and communication protocol 

EX: 

Say a server has a function: 

```
int add (int x, inty) {
    return x + y 
} 
```

And a client wants to call that function like so: 
```
Z = add(11,22)
```

- the `add` function is not present on the client, they are pinging the server and having the logic performed there.
- Client-Side stub marshals the parameters and sends them. 
- Server-side stub unmarshals them, calls the actual function, encodes the result, and sends it back 
- The application developer calls a function as if it were local; the network details are hidden 

## Modern Webservices arechitecture 

- Services are partitioned into smaller services, each with APIs 
    - Example: rideshare having discrete microservices for ride hailing, payment, account management, etc 
- Could use REST (with JSON), but could also use gRPC as the protocol 

## gRPC - Modern Implementation 

- Based on protobufs - binary format to serialize data 
- Leverages HTTP 2 (persistent and pipelined messages 
- More efficient than JSON. Example comparison:

**JSON: 55 bytes** 
```
{
    "age": 35
    "first_name": "Stephane",
    "last_name": "Maarek"
}
```

Same data in a protocol buffer: 20 bytes 
```
message Person {
    int32 age = 1;
    string first_name = 2;
    string last_name = 3;
}
```

## HTTP vs gRPC 

Feature | HTTP/REST (JSON) | gRPC (Protobuf) 
--- | --- | ---
Data Format | Text-based, human-readable | Binary, compact 
Transport | HTTP/1.1 or HTTP/2 | HTTP/2 
Serialization | Manual or JSON library | Automatic via protobuf compiler 
Use Case | Public APIs, Web Browsers | Internal microservices, high performance 
Debugging | Easy (readable text) | Requires tools to inspect binary 

## gRPC Workflow 

### 1. Define `.proto` File 

- Specifies the service interface (functions, methods)
- Defines message structure (data types) 

Example: 

```
service Echo {
    rpc echo(Message) returns (Message) {}
}

message Message {
    string message = 1;
}
```

### 2. Compiler (`protoc`)

- Protocol buffer compiler generates languate-specific files (stubs) containing serialization/deserialization code 

### 3. Implement Server

- Import generated libraries
- Defines message structures (data types)

### 4. Implement client 

- Import generated libraries 
- Create a client stub 
- Call the remote functions directly via the stub 

## Walkthrough Example: Echo Client / Server 

### `.proto` definition 

`simple.proto`
```
syntax = "proto3";

service Echo {
  rpc echo(Message) returns (Message) {}
}
message Message {
  string text = 1;
}
```

### Compile 

Now run:
```bash
python -m grpc_tools.protoc \
    --proto_path=. \
    ./simple.proto \
    --python_out=. \
    --grpc_python_out=.
```

Which generates files `simple_pb2_grpc.py` and `simple_pb2.py`


### Implement Server 

```python 
import grpc 
from concurrent import futures 
import simple_pb2_grpc 
import simple_pb2 

# Create class for each service, in this case `EchoServicer`
class EchoService(simple_pb2_grpc.EchoServicer):

    def __init__(self, *args, **kwargs):
        pass 
    
    # Implement each function
    def echo(self, request, context):
        # get string from incoming request 
        mess = request.message 
        print("Received: " + mess)

        retval = simple_pb2.Message()
        retval.message = mess 

        return retval 

# Configure and start the server 
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    simple_pb2_grpc.add_EchoServicer_to_server(EchoService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()
```

### Implement Client 

```python
import grpc 
import simple_pb2_grpc 
import simple_pb2 

def run():
    channel = grpc.insecure_channel("localhost:50051")
    echosstub = simple_pb2_grpc.EchoStub(channel)

    param = simple_pb2.Message(message="HELLO")
    print(f"PARAM: " + str(param))

    retval = echostub.echo(param)
    print("RETVAL: " + str(retval))
```

## Advanced API Patterns in gRPC 

1. **Unary**: Standard request/response (see above example)
2. **Server Streaming**: Client sends one request, server sends a stream of responses 
3. **Client Streaming**: client sends a stream of requests, server responds once with a summary 
4. **Bidirectional Streaming**: Both client and server send streams of messages independently 











