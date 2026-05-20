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

# Routing (Control Plane)

- Gatewway
- Forwarding traffic to a destination 

## Key Function of control plane: Calculate forwarding table 

- Routing protocols differ in how they approach each problem:
    - What info each router knows (entire topology or just its neighbors)
    - What info each router exchanges (all routes or single route)
    - What calculation is performed (shortest path or whats locally best) 

## Decentralized control plane 

These are traditionally known as routing protocols 

- Link-state protocol - OSPF (intra-domain)
- Path-Vector protocol - BGP (Inter-domain)

## Centralized Control Plane

Shifts calculation logic to external software baSED SDN controller. Routers act as pure data plane devices.

# Routing: Link State Protocol 

## Decentralized control plane

Traditionally what you'd know as **Routing Protocols** which answer:

- What info each router knows (e.g. entire topology or just neighbors)
- What info each router exhanges (e.g. everything it has learned or just what it has selected)
- What calculation is performed (e.g. shortest path or what's locally best) 

## OSPF - Open Shortest Path First 

- Widely used Link State Protocool in LANs
- Each router establishes peering with neighbors 
- Link states are flooded to entire network
- each router calculates shortest path(s) 

## Link States and Information Exchange 

- connection to other routers - tells who the neighbor is 
- connection to network with end hosts - tells prefixed reachable 

### Flooding and update process 

- Routers send **Link State Updates (LSUs)** to share their known states with immediate neighbors 
- Receiving routers store these updates in a local database and flood the new information out of their interfaces to *their* neighbors 

### Network Convergence

- The iterative exchange of updates continues until every router in the network processes an identical, synchronized **Link State Database (LSDB)**
- At convergence, every individula router has full visibility of the entire network topology

## Shortest Path Calculation (Dijkstra's Algorithm)

Graph representation: the network is viewed as a graph. 

Result: The algorithm yiels a shortest-path tree rooted at *u* that spans every node in the network.

### Algorithm 

Definition: **Dijkstra's Algorithm** is an algorithm for finding the shortest paths between nodes in a weighted graph.

Start at root node *u*, assess immediate next-hop costs, and select lowest-cost neighbor (node *w*)


#### Pseudocode
```
function Dijkstra(Graph, source):

    for each vertex *v* in *Graph.Vertices*:
        dist[v] = INFINITY
        prev[v] = UNDEFINED
        add v to Q 
    dist[source] = 0 

    while Q is not empty:
        u = vertex in Q with minimum dist[u]
        Q.remove(u)

        for each edge (u, v) in *Graph*:
            alt = dist[u] + Graph.Distance(u,v)
            if alt < dist[v]:
                dist[v] = alt 
                prev[v] = u 

    return dist[], prev[]
```

## Forwarding table construction and Network Dynamics

- Populating the Forwarding table: the calculated shortest-path tree indicates the precise next-hop interface for any given destination IP address mapping
- Network Dynamics: 
    - Network Changes such as adding a new router, experiencing link/node failure, or introducing a new IP prefix - alter local link state 
    - The router that detects the change instantly generates a new Link State Update and floods it through the network 
    - The network undergoes the update process until it reaches a new state of convergence, triggering all routers to re-run Dijkstra's algorithm and update their forwarding tables 

# Routing: Path Vector Protocol 


## The Internet 

- **The Internet** is a collection of  many inter-connected networks called **Autonomous Systems**.
- **Autonomous Systems** are a network administered by a single enterprise or commercial entity.
- **Border Gateway Protocol**: is a protocol that provides a mechanism for distinct Autonomous systems to communicate and exchange routing information across network boundaries.

## BGP Process 

### Algorithm 

1. Establish peering sessions with direct neighbors
2.  Process route updates, failures, or configuation shifts 
3. Update the internal routing table 
4. Compute the locally optimal route for an IP prefix 
5. Advertise changes or new path choices to neighboring peers 

### Definitions 

- **Route**: A path mapped to a specific destination IP prefix (e.g. 1.2.3.0/24)
- **Path**: A sequence of autonomous system numbers (ASNs) used to track network hops

## Handling Network Dynamics

- **Link Failures**: If a link drops, the detecting AS updates its local topology table and purges the invalid entry 
- **Route Withdrawals**: An explicit message type sent to neighbors to unannounce or revoke previously a previously advertised route 
- **Route Updates**: sent alongside or following a withdrawal if an alternative path is chosen locally, ensuring neighbors converge on a new path 
    - *Split Horizon Rule*: An AS will not advertise a path back to the specific neighbor it originally learned that path from 


## Internal vs External BGP boundaris 

- Network abstraction vs reality: Large networks consist of many internal routers rather than a single logical node. 
- eBGP (external BGP): used to exchange routing information between edge routers of *different* networks 
- iBGP (internal BGP): used to distribute the externally learned routing information to all internal routers within the same autonomous system 
- prefix injection: how an AS originates a prefix into BGP 
    - dynamicaly via redistributionfrom Interio Gateway Protocols like OSPF 
    - statically via manual router configurations 


## Inter-domain business relations and policies 

- Provider: paid money to transfer traffic 
- Customer: pays money to a provider to have its traffic carried 
- Peer: financially neutral arrangement where two ASes connect to each other and will send traffic through each other 
- BGP Policies to control what is being announced. e.g. a provider will block non-lucrative transit traffic 

## Best Path Calculation Algorithm 

1. **Local Preference**: numerical value assigned by routing policy
2. **AS Path Length**: number of AS-level hops in the path 
3. **Multiple exit discriminator (MED)**: allows one AS to specify that one exit point preferred
4. **eBGP over iBGP**: Learned trhough external neighbor over internal 
5. **Shortest IGP path cost**: Exit this network as quickly as possible 
6. **Router id**: arbitrary tiebreaker 



































