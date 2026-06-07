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

## Socket Funcamentals 

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


