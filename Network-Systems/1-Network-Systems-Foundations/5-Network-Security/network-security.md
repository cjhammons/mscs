Network Security 
---

# Introduction 

- **Core Problem**: Communication occurs across mediums that may not be under user control. This means malicous parties can attack at various locations along the path 

## Pillars of Information Security 

1. **Confidentiality**: Information is only visible to intended recipients
2. **Integrity**: Data has not been modified/corrupted
3. **Availability**: information can be accessed 

## Vulnerabilities and solutions by layer 

### Network layer: Data plane 

Example: 
- A company has 2 sites and employees at different sites want to share information with each other. If attacker can see traffic, will get access to secret data 
- Solution: IPsec

### Network Layer: Control Plane

- BGP communicates paths to reach IP fixes
- Example: if attacker can inject fake paths, it can get traffic directed to it 
-Solution: RPKI 

### Application & Transport Layers 

- TCP provides in-order reliable stream between two processes 
- HTTP provides application protocol to get and put web objects 
- Attacker could pretend to be the bank, or inspect / modify traffic 
- Solution: TLS/HTTPS 

# Basics Cryptography and Security Primitives 

## Cryptography Terminology 

- Actors
    - Alice & Bob: the legitimate communicating parties 
    - Eve: Eavsdropping attacker 
- Plaintext: Original, unencrypted message 
- Ciphertext: encrypted output that reveals no meaning if intercepted 
- Keys: Bit patterns used as input for encryption/decryption algorithms 
- Goal: Transform *m* into ciphertext using Key K_A, then back using key K_B

## Encryption techniques 

### Symmetric Encryption (Shared Key) 

- Alice and bob share a key, which is used in both the encryption and decryption 
- Fast, but need to share key 
- Problem: how to share key initially? 

### Asymmetric Encryption (Public Key) 

- Mechanism: a key pair is generated:
    - public key: Shared openly, used for encryption
    - private key: kept secret by owner, used for decryption
- Slow computation
- Only handles short messages directly
- solves key distribution problem 

#### RSA: encryption, decryption

1. given public key (n,e) and private key (n,d)
2. Message *m* is just a bit pattern and interpreted as an integer 
3. to encrypt message *m* (<n) computer *c = m^e* mod *n*
4. To decrypt received pattern *c* computer *m = c^d* mod *n* 

### Hybrid approach (session keys) 

Combine best of both worlds 
1. Alice uses Bob's **Public Key** to encrypt a randomly generated **Session Key**
2. Bob decrypts session key with **Private Key** 
3. Both parties use the shared **Session Key** with fast **Symmetric Encryption** for the rest of the Communication

## Message Integrity 

### Hashing 

- converts variable-length messages into a fixed-length **digest**
- computationally infeasible to find two different messages that produce the same digest (collision resistance)
- Limitation: if has is sent in the clear, and attacker can modify both message and hash 

### Hash-keyed Message Authentication Code (HMAC)

- Combines hashing with shared secret key 
- Process: Hash(Key || Message) (often double hashed for security)
- Benefit: since teh attacker does not know the secret key, they cannot generate a valid HMAC for a modified message. This ensures both integrity and authenticity of the data source 

## Digital Signatures 

- Goal: Prove message came from a specific sender and hasn't been altered 
- Mechanism (reverse of encryption): alice uses private key to "sign", Bob uses Alice's public key to verify 

## Digital Certificates 

- Problem: How do we trust that a Public Key actually belongs to Alice? An attacker could substitute their own key 
- Solution: Bind the identity (name, org, country) to the public key 
- Role of Certificate Authority (CA):
    - trusted 3rd party verifies identity
    - the CA signs the certificate using its own private key 
    - Browsers/OS have pre-installed root certificates (CA public keys) to verify these signatures 
    - If signature verifies, the identity bound to the public key is trusted 

# IPSec 

Threat Landscape:
- Link Layer: wi-fi is a broadcast medium; traffic can be intercepted in public spaces 
- Infrastructure: network providers may have a rogue employee, backdoors, or compromised routers
- Routing: misconfigurations or intentional BGP route hijacking can redirect traffic to an attacker's location 

IPsec creates an encrypted "tunnel" between two endpoints, ensuring confidentiality and integrity regardless of underlying network path. Commonly used in VPNs

## IPsec setup phases 

### Phase 1: SA-1 Parameter Exchange (IKE)

- Initiator says what algorithms it supports across 4 categories 
    - encryption- DES, AES...
    - Hash - SHA, MD5
    - DH Group - 1,2,5 
    - Auth - shared, certificate... 
- Responder chooses mutually supported options and sends them back 

### Phase 2: Key Exchange (Diffie Hellman) 

- IPsec uses shared keys for encryption and integrity 
- Diffie Hellman is a protocol to secretely share private keys 
- Algorithm:
    1. Public parameters: Initiator sends Prime(p) and Base (g) 
    2. SEcret generation:
        - Initiator picks secret x, calculates h_A = g^x mod p 
        - Responder picks secret y, calculates h_B = g^y mod p 
    3. Exchante: they swap h_A and h_B 
    4. Shared key calculation:
        - Initiator computes K = (h_B)^x mod p 
        - Responder computes K = (h_A)^y mod p 
    5. Both arrive at K = g^xy mod p. Even if an attacker sees p, g, h_A, h_B, they cannot easily derive K (discrete logarithm problem) 
- Usage: the shared key *K* is used for symmetric encryption and HMAC (integrity) for the tunnel 

### Phase 3: Authentication 

- Goal: Verify the identity of the peer before establishing the final tunnel parameters 
- Options decided in SA-1 param exchange:
    - pre-shared private key 
    - digital certificate
- This step uses keys determined with the DH key exchange step 

### Phase 4: SA-2 Parameter Exchange 

- Sets up security association for traffic exchange in case different parameters are desired 
- Used to set up traffic selectors which determine what traffic is allowed through the tunnel (5-tuple of IP src/dest, protocol, transport src/dest) 

## Traffic Exchange 

### Protocols 

1. AH (Authentication Header)
    - provides integrity and authentication only 
    - does not encrypt the paylaod 
2. ESP (Encapsulating Security Payload):
    - provides confidentiality (Encryption), Integrity, and Authentication 
    - Most common choice 

### Modes

1. Transport Mode 
    - host-to-host communication (single endpoint)
    - encrypts/authenticates only the payload (TCP/UDP segment)
    - original IP remains visible 
2. Tunnel Mode 
    - site-to-site (gateway-to-gateway) connections 
    - encapsulates entire the original IP inside a new IP packet with a new header 
    - hides the internal source and destination IP addresses of the end users. only the ege router IPs are visible 


















