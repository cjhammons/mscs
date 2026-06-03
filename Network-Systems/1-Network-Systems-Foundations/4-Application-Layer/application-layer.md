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

1. Root DNS Server: 13 known root servers 
2. Top-Level domain: Domains like .com, .edu, .org 
3. Authoritative DNS server: hold the actual records for specific domains (e.g. dns.cs.umass.edu) 
4. Local DNS server (Resolver): first point of contact for a host. Often provided by ISP or university 

### Query modes 

- **Recursive Query**: local DNS server takes full responsibility for finding the answer and returning the final result to host 
- **Iterative Query**: a server responds with the best answer it has (often a referral to another server) rather than doing the full lookup itself 

## DNS Resolution process 


