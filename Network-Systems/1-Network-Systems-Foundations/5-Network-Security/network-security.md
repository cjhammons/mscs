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


