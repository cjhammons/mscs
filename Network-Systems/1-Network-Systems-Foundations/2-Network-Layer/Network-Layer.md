Network Layer
---

# Introduction

What if nodes on a link have different linke types?
What if the nodes have different Admins? Such as different companies.
What if Nodes are in different locations? Are MAC table lookups going to scale to billions of devices?

The Network Layer addresses these needs.

## Overview

- How do we address nodes scalability across different networks
- Given a dest address how do we forward it scalably 
- How do networks coordinated 
- How are addresses assigned and mapped to link layer addresses 
- What tools can an admin use to troubleshoot beyond their network boundaries

# Internet Protocol

## Internetworking 

- Enable communications between multiple heterogeneous networks 
- Key: Router at the edge of each Network 

Note: At this layer, units of data are called **Packets**

## Service Model of the Internet Protocol 

- Best Effort
    - Delivery: packets may get dropped 
    - Timing: no guarantee on how long it takes to deliver packets 
    - Order: Packets may get re-ordered in the network 
- Reasoning: inter-connecting different link layers requires lowest common denominator 

## Addressing in IP

- Each interface gets an IP address 
- IPv4: 32 bits in dotted decimal (e.g. 192.168.0.1)
- IPv6: 128 Bits in hextets (16 bits) separated by colon
    - Ex: `2001:0db8:0000:0000:0000:ff00:0042:8329`
    - Leading zeroes can be dropped: `2001:0db8:0:0:0:0042:8329
    - consecutive 0s can be replaced with `::`: `2001:0db8::ff00:0042:8329`

## Structure Adds Scalability 

- In Ethernet we saw tables had 1 entry per destination 
- That doesn't scale to billions of devices worldwide 
- Solution: Add structure to addresses so devices can be grouped 

### Subnet

A **subnet** is a scale of consecutive IP addresses 

- High order bit sin a subnet are all the same 
- Low order bits identify host uniquely within that network 
- Now, just need to know how to get to the subnet 

### CIDR (pronounced "cider")

- Classless Inter-Domain Routing 
- Format: a.b.c.d/x
- X is the length of the prefix - number of high order bits that are the same 
- a.b.c.d values which are teh same (use 0 for low order bits) 

EX:

Prefix: 2.1.1.0/24
Devices:
    - 2.1.1.0
    - 2.1.1.1
    - ...
    - 2.1.1.255 

### Hierarchical 

- Two subnets can combine 
- 1.1.0.0/24 and 1.1.1.0/24 = 1.1.0.0/23 

# Router Data Plane

## Role of a Router

- Gateway
- Forwarding traffic to a destination 

## Forwarding vs Routing 

###  Forwarding: Data Plane

- Direct a packet to an output port/link 
- Uses a forwarding table 

### Routing: Control plane 

- Computes paths by coordinating with neighbors 
- Creates forwarding table 

### Packet Forwarding 

- Control plane (route processor) calculates the forwarding table 
- Data plane - life of packet 
    - Received at ingress of line card 
    - lookup destination in forwarding table (determines output port)
    - send packet over switch fabric to output port 
    - Line card transmits packet


### Longest Prefix Match (LPM)

- find most specific prefix that matches the destination 

Given 2 subnets where prefixes overlap:
- 11.11.0.0/16 
- 11.11.11.0/25

Lookup table:

Destination | Port 
--- | ---
11.11.0.0/16 | 1 
11.11.11.0/24 | 2 

Given `Dst` = 11.11.11.11

Using **Longest Prefix Match (LPM)** find most specific prefix that matches the destination, it would route to **Port 2**


## Evolution of switching fabrics 

Generation | Architecture Type | Mechanism | main bottleneck/tradeoff
---        | ---               | ---        | ---
Gen 1      | Switching via Memory | Input port copies packet to system memory; central CPU resolves lookup and copies packet to output port | CPU & Memory bandwidth: Shared bus transfers and CPU processing limit system parallelism 
Gen 2 | Switching via bus | Distributed architecture. Forwarding tables are pushed downstream to line cards. Packets skip main memory | Bus contention: shared physical bus allows only one packet transfer at any given time slot 
Gen 3 | Switching Fabric | Parralel architecture. Uses advanced topologies such as a **crossbar switch** to split data into tiny time slots, connecting multiple inputs to multiple outputs concurrently | Requires specialized hardware
Gen 4 | Cloud & Virtualized Software | Return to memory-based switching leveraging massive modern parallelization. Optimized for VE | Does not entirely replace Gen3, but dominates Virtualized, cloud-scale, and software-defined networks












