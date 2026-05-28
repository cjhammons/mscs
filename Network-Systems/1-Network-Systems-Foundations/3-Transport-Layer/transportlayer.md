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



