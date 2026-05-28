Transport Layer
---

# Introduction

## Core Problems Addressed by Transport Layer 

### Multiplexing and Demultiplexing

- We have multiple applicaitons running - *which applications is a packet for?*
    - a single host may run muletiple applications simultanously

### Reliable Transfer 

- Allow an application to be assured that what the ysend is what is received

### Congestion Control

- Congestion in the network will occur - leading to packets being dropped
- What if senders could detect this and backoff as needed?

# Multiplexing 

The transport layer shifts the scope from **Host-to-Host** (Network Layer) to **Process-to-Process** (Transport layer)

**Mulitplexing**: sending
**Demultiplexing**: receiving 

## Ports and Headers 

- Transport Header Structure:
    - Src port
    - Dest port 
- Port Assignments:
    - 80 common for Web Servers 
    - 22 for Secure Shell (SSH)

## Transport Protocols 

- Connectionless 
    - Host uses Dest IP and Dest Port to demultiplex to specific process 
    - No established process required 
    - Only state is (IP, port) to process mapping
- Connection-oriented
    - 4typle of Src IP, Dest IP, Src Port, Dest Port identifies Connection 
    - requires pre-establishment 
    - host keeps more state about the connection 

### User Datagram Protocol (UDP)

- connecitonless 
- Simple multiplexing / demultiplexing 
- inherits IP's service - best effort delivery of each datagram 

### Transport Control Protocol (TCP)

- connecion-oriented 
- single process can have multiple connections 
    - src IP
    - dest IP
    - src port 
    - dest port 
- in-order reliable stream 

# Reliable Transfer 

- Goal - Allow an application to be assured that what they send is what is received (same data, same order) 
- **TCP only**. Unlike UDP, TCP provides a reliable, in-order byte stream 

## Causes of data loss 

1. **Physical Errors** (Link Layer). Bit flits, dropped corrupted frames 
2. **Router Congestion** (Network Layer). Buffer overflow
3. **Packet Reordering** (Routing Dynamics): Protocols like BGP may update routes dynamically due to failures or policy changes

## TCP Mechanism for Reliability 

TCP incorporates key mechanism to overcome these issues:

### Sequence Numbers

- Function: Identifies the specific position of data within the byte stream 
- The sequence number indicates the **first byte** contained in the diagram 
- Example: If sending 300 bytes in chunks of 100:
    - Packet 1: Seq = 0 (bytes 0 - 99)
    - Packet 2: Seq = 100 (bytes 100-199)
    - Packet 3: Seq = 200 (bytes 200-299)

### Acknowledgement Numbers 

- Informs the sender which data has been received 
- ACK specifies the **next byte** the receiver expects to receive 
- EX: ACK of 200 implies all bytes up to 199 have been received 

### Retransmission Strategies 

If data is lost, the sender must resend it. There are two primary signals that TCP uses to trigger Retransmission

#### Timeouts 

- Sender watis for an ACK. If none arrives within a calculated time, it assumes the packet (or ack) was lost.
- The timing calculation is based in Estimated Rount Trip Time (RTT) pluse a safety buffer.


#### Duplicate ACKs

- If the receiver gets out-of-order packets (e.g. receives bytes 100-199 before 0-99) it continues to send ACKs for the missing byte (e.g. repeatedly ACKing (expecting 0)
- Receiving multiple duplicate ACKs for the same sequence number is a strong indicator that a packet was dropped, prompting faster Retransmission than waiting for timeout 

## Flow Control (Preventing Receiver Overloads)

- Sender may transmit data faster than the receiver can process or store it 
- TCP receiver advertises free buffer space in `rwnd` (received window) field in TCP header 
- Sender limits amount of unACKed "in flight" data to received `rwnd`


# TCP Connection Establishment

## Necessity of State Management 

The mechanisms of SEQ Numbers, ACK numbers, Retransmission, and Flow Control all require state.

### Components of TCP State 

- **Buffers**: Send buffers (holing data until ACKed) and receive buffers (holding out-of-order data)
- **Variables**: ACK numbers, estimated RTT, and receive windows 
- **Resource Contraint**: Since memory and processing resources are finite, the system must explicitly agree to establish a connection before allocating this state 

## Concept of Connections Establishment 

- TCP is connection oriented 
- Each process must agree to form a connection 
- **Three way handshake**
    - A -> B: "I'd like to connect"
    - B -> A: "Sounds good to me"
    - A -> B: "Thanks, connection established" 

## TCP Flags Involved 

- **SYN (Synchronize)**: Indicates Synchronization of sequence numbers; marks start of a connection 
- **ACK (Acknowledgement)**: Indicates that the ACK Number field is valid 

## Three Way Handshake Step-by-Step 

### Step 1: Host A sends SYN 

- Host A selects an initial Sequence Number (e.g. seq = 1000)
- Sets the SYN Flag 
- Packet: [SYN, seq=1000]

### Step 2: Host B sends SYN-ACK 

- Host B creates state for connection 
- ACKs Host A's SYN: Sets ACK flag and ACK number to 1001 (next expected byte) 
- Synchronizes its own sequence: Selects its own initial Sequence Number (e.g. seq = 600) and sets the SYN flag 
- Packet: [SYN, ACK, seq=600, ack=1001]

### Step 3: Host A sends an ACK 

- Host A acknowledges Host B's SYN 
- Sets ACK flag and ACK number to 601 (next expected byte from B) 
- Packet: [ACK, ack=601]




