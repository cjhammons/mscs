Module 1: Link Layer
---

Date: 3/25/26

# Introduction


## Links

- Networks consist of **links** interconnecting nodes through wires or wirelessly
- Typically implemented on the Network Interface Card (NIC)

## Problems solved by Link Layer

1. How do we encode the data such that each side can understand who it's destined for, and how to interpret the data?
2. How do we detect if an error has occured, and better yet, correct it?
3. For shared access mediums, how do we coordinate between nodes to regulate access to the medium?
4. How to extend into a local area network (LAN) to extend beyond the physical limits of the of the transmission medium?



# Encoding into Frames

Frames help solve the first problem addressed by link layer: *How do we encode the data such that each side can understand who it's destined for? And how do we inteprete it?*

## Structring the data

- Assume you can transmit 1s and 0s throug whatever medium
- making sense of the series of 1s and 0s needs structure

## Frame parts

- **Payload**: data that is to be transmitted
- **Header** and **Trailer**: Extra information to help understand how to handle the Payload

## Ethernet

- Dest is for filtering messages (is it for this node)
- Source is useful to know who sent message (so node can reply)
- Type - What the data is
- Frame Check Sequence (FCS) - for error handling

| **DEST** | **Source** | **Type** | *data* | **FCS** |
--- | --- | --- | --- | --- |
| 48 bits  | 48 bits    | 16 bits  |   -    | 32 bits |

### Media Access Control (MAC) address

- 48 bits, displayed with colons
- Historically assigned as part of the manufacturer and globally unique (with virtualization, not the case)

### Broadcast addressed

- Special destination address which says this is for everybody

FF:FF:FF:FF:FF:FF

## Different Frame Formats

Key takeaway is that some standard defines the format, so everyone using it can know how to speak to one another.
- ATM
- 802.11

**Date 3/30/26**

# Error Handling

*Detecting Bit Flips*

## Parity

Force every transmission to have an even (or odd) number of 1s by adding 1 extrabit to 0 or 1 based number of 1s in data. If a single bit gets flipped, it would make the transmission odd (or even)

- **Even Parity**: Parity forcing an even number of 1s 
- **Odd Parity**: Parity forcing an odd number of 1s 

### XOR

We count 1s using XOR

Example:

0101 => 1 XOR 0 XOR 1 XOR 0 = 0 (even number of 1s)
1110 => 1 XOR 1 XOR 1 XOR 0 = 1 (odd number of 1s)

### Parity Example

Even parity.

#### Ex 1 

Data: 11000000 => Already even, so we add 0 to end of transmission: 11000000**0** 

**Received**: 110000000. We XOR it to get 0, meaning it is even and correct.

#### Ex 2

Data: 01010111 => Odd. So add 1 to transmittion: 01010111**1**

**Received**: 01010111. We XOR it and get 0, meaning it is even correct

#### Ex 3:

**Received**: 010101101 => Odd. Which means it is odd and an Error.

### Parity Limitations:

What if there are 2 bit flips?

## Cyclic Redundancy Check (CRC)

CRC is a more powerful form of error detection. Cyclic codes are particularly suited to detect burst errors. It has been adopted for the FCS in Ethernet.

Given:
- **D**: Data to be transmitted
- **G**: Generator polynomial (value defined by ethernet standard) (r+1 bits)
- **R**: Extra bits added by CRC (r crc bits) 
- Formula for bit pattern: **<D,R> = D\*2^r XOR R**

| Data bits | Extra Bits |
| ---  | ---  |
| D    | R


Calculate: Find R such that <D,R> id divisible by G (mod 2)

Check: Receiver divides <D,R> by G. If remainder is 0, no error. Otherwise, error 

### Example

- r = 3
- G = 1010 (r+1=4 bits)
- D = 11101010
- Find: R (3 bits)

#### Step 1: Set R = 0 

<D,R> = 11101010 000

#### Step 2: Divide <D,R> by G

11101010000 / 1010 = 1101011 Remainder (R) 110

R is 110, so we would transmit out new <D,R> = 11101010 110

#### Step 3: Check on receive Side 

- Received <D,R>
- Divide by G 
- If remainder is 0 it is correct. Else Error 

### CRC in Ethernet 

Detects:
- any 1 bit error 
- any 2 adjacent 1 bit errors 
- any odd number of 1 bit errors 
- any burst of errors with a length of 32 or less 

Can be calculated as bytes arrive off the wire. Simple calculation only involving XOR 

# Sharing the Link

Date: 4/3/26

Problem: how do we coordinate between nodes to regulate access to the medium.

## Multiple Access Protocols 

How do we share the link *fairly* and *efficiently*?

### Possible Approaches

- **Channel Partitioning**: Diving link into smaller pieces and assign to each node 
- **Random**: Deal with collisions when they happen

### Partitioning by Time 

**Time Division Multiple Access (TDMA)**

- Divide into equal sized time slots
- assign slots to nodes 

| 1 | 2 | 3 | 4 | 1 | 2 | 3 | 4 |
| --- | --- | --- | --- | --- | --- | --- | --- |

Nodes can only send during their slots. For example, slots are 100 bytes. 1 has 10 bytes to send, 2 has 0, 3 has 200 (split over 2 sycles), 4 has 150 (also split over 2 cycles). This creates inefficiencies. 

### Partition by Frequency

- **Frequency Division Multiple Access (FDMA)**
- Divide frequency spectrum and assign each node it's own frequency 

## Random Multi Access Protocols

- When to send? 
    - Anytime? make an attempt to not interfere?
- How does a node know if transmission was successful?
    - can a ndoe detect this? Does receiver have to ack?
- What happens if transmission failed?
    - Resend immediately? Wait for some amount of time?

### When to send 

- Carrier Sense Multiple Access (CSMA)
    - used in both Ethernet and Wi-Fi
- Node will read from the channel to see if another node is sending and transmits when it senses idle 

### Knowing if a Transmission was Successful (CSMA / CD - Ethernet)

- CSMA / CD - collision detection (802.3)
- Ethernet NICs can read while transmitting 
- If what it reads is different than what it's sending, it detects a collision 
- Node will send a "jam" signal - transmit fixed bit pattern to ensure everyone detects the collision 

#### WIFI 

- CSMA / CA collision avoidance (802.11)
- 802.11 NICs cannot read while transmitting and may be out of range of some nodes (z can't sense x is sending)
- It depends on an explicit acknowledgement from receiver 
- if it doesn't receive an ACK in certain period of time, assumes collision
- Optional RTS / CTS: 
    - requests to send 
    - clear to send 

### When a transmission fails 

- Re-transmit the frame some time period later (backoff)

CSMA/CA and CSMA/CD specify:
- random backoff time - to avoid nodes repeatedly colliding 
- Exponentially increasing - when multiple transmissions fail, wait longer each time 


# Local Area Network (LAN) 

## Ethernet 

### Ethernet Switching 

- Scalability challenges with shared cable 
- Switching solves this 
    - uses point to point full-duplex links 
    - special nodes (switches) can direct traffic to destination 

### Ethernet Addressing 

Recall:
- each NIC has a MAC address 
- each frame contains src and dest MAC address 

#### MAC Address Table 

DEST MAC ADDRESS | OUT PORT 
--- | ---
AA:AA:AA:AA:AA:AA | 0 
BB:BB:BB:BB:BB:BB | 1 
CC:CC:CC:CC:CC:CC | 2 

- Table in switch maps destination addres to output ports 
- Receive fraime, lookup destination, send frame 

How do we fill the MAC address table? 

- Table starts empty
- When switch receives a frame it **learns** the source is at that port 
- if destination is unknown, **flood** to all ports 
    - all but actual destination ignore it 
    - if destination replies, switch will learn the address on that port 
- Switches are limited in number of ports, so you can extend with a topology of switches 

**Problem: Loops**

- recall that there are broadcast MAC addresses 
- recall that we used flooding forlearning 

**Solution to Loops**

- Could keep track of messages seen 
- Could limit the number of hops a given message takes 
- Could turn off links that create the loop (with a protocol like Spanning Tree Protocol)
- Architect network such that looping won't occur (e.g. topology, or avoid broadcasts and flooding)

## Wireless LAN 

- The special nodes in this case are access points (AP)
- APs commonly connected to a wired network 
- All traffic goes via the APs (even if nodes are in range) 
- Key challenge here is associating with an AP 







