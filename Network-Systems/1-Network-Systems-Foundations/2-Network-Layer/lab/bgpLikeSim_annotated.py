# Task: Create some functions for a simplified BGP router
#   Specifically, the withdraw, update, and next_hop functions of the Router
#   The class Route will be used.
# 
#   withdraw(rt) - rt is type Route. If a simplified BGP router gets this message, it will   
#                  remove the route from the RIB (Routing Information Base)


class Route:
    # A prefix is in form 
    neighbor = ""  # The router that sent this route - will be a.b.c.d
    prefix = ""    # The IP address portion of a prefix - will be a.b.c.d
    prefix_len = 0 # The length portion of a prefix - will be an integer (e.g., 24 for /24)
    path = []      # the AS path - list of integers (Autonomous System numbers)

    def __init__(self, neigh, p, plen, path):
        self.neighbor = neigh
        self.prefix = p
        self.prefix_len = plen
        self.path = path 

    # convert Route to a String    
    def __str__(self):
        return self.prefix+"/"+str(self.prefix_len)+"- ASPATH: " + str(self.path)+", neigh: "+self.neighbor

    # Get the prefix in the a.b.c.d/x format
    def pfx_str(self):
        return self.prefix+"/"+str(self.prefix_len)


# Implement the following functions:
#  update - the router received a route advertisement (which can be a new one, or an update)
#         - the function needs to store the route in the RIB
#  withdraw - the router received a route withdraw message
#          - the function needs to delete the route in the RIB
#  nexthop - given ipaddr in a.b.c.d format as a string (e.g., "10.1.2.3"), perform a longest prefix match in the RIB
#          - Select the best route among multiple routes for that prefix by path length.  
#          - if same length, return either

class Router:
    # You can use a different data structure
    # dictionary with key of the prefix, value a list of Route
    # example: rib["10.0.0.0/24"] = [Route("1.1.1.1", "10.0.0.0", 24, [1,2,3]), 
    #                                Route("2.2.2.2", "10.0.0.0", 24, [10,20])]
    #          rib["10.0.0.0/22"] = [Route("3.3.3.3", "10.0.0.0", 22, [33,44,55,66])]
    rib = {} 

    # If you use the same data structure for the rib, this will print it
    def printRIB(self):
        for pfx in self.rib.keys():
            for route in self.rib[pfx]:
                print(route) 


    # ============================================================================
    # UPDATE FUNCTION
    # ============================================================================
    # ALGORITHM: Store or update a route in the RIB
    # 
    # BGP routers receive route advertisements from neighbors. Each advertisement
    # contains: prefix, prefix length, AS path, and the neighbor that sent it.
    # 
    # Key behaviors:
    # 1. Routes are stored by prefix key (e.g., "10.0.0.0/24")
    # 2. Multiple neighbors can advertise the SAME prefix (we store all of them)
    # 3. If the SAME neighbor sends an update for the same prefix, we REPLACE
    #    their old route (BGP doesn't keep stale announcements from same neighbor)
    # 4. Different neighbors for the same prefix are BOTH kept (for path selection)
    #
    # Time Complexity: O(n) where n = number of routes for that prefix
    # Space Complexity: O(1) - just modifies existing data structure
    # ============================================================================
    def update(self, rt):
        # Create a unique key for this prefix (e.g., "10.0.0.0/24")
        # This key groups all routes to the same destination prefix
        prefix_key = f"{rt.prefix}/{rt.prefix_len}"
        
        # Initialize the list for this prefix if it doesn't exist yet
        # This is the first time we're hearing about this prefix
        if prefix_key not in self.rib:
            self.rib[prefix_key] = []
        
        # Check if we already have a route from this specific neighbor for this prefix
        # In BGP, each neighbor can only have ONE active route per prefix at a time
        found = False
        for i, existing_route in enumerate(self.rib[prefix_key]):
            if existing_route.neighbor == rt.neighbor:
                # Found the neighbor, replace THIS specific route in the list
                # This handles BGP route refresh/update from the same neighbor
                self.rib[prefix_key][i] = rt
                found = True
                break
        
        # If we didn't find the neighbor, add the new route to the list
        # This is a new neighbor advertising this prefix to us
        if not found:
            self.rib[prefix_key].append(rt)
        



    # ============================================================================
    # WITHDRAW FUNCTION
    # ============================================================================
    # ALGORITHM: Remove a route from the RIB when a neighbor withdraws it
    # 
    # BGP neighbors can send WITHDRAW messages when they no longer want to
    # advertise a route (e.g., link failure, policy change).
    # 
    # Key behaviors:
    # 1. Find the specific route from the withdrawing neighbor
    # 2. Remove ONLY that neighbor's route (other neighbors' routes stay)
    # 3. If NO routes remain for a prefix, DELETE the prefix key entirely
    #    (clean up prevents stale entries in the RIB)
    #
    # Time Complexity: O(n) where n = number of routes for that prefix
    # Space Complexity: O(n) for creating the filtered list
    # ============================================================================
    def withdraw(self, rt):
        # Create the same prefix key format as in update()
        prefix_key = f"{rt.prefix}/{rt.prefix_len}"
        
        # If this prefix doesn't exist in our RIB, nothing to withdraw
        # (gracefully handle case where neighbor withdraws a route we never knew about)
        if prefix_key not in self.rib:
            return 
        
        # Filter out the route from the specific neighbor
        # List comprehension creates a NEW list containing only routes where
        # the neighbor is NOT the one withdrawing
        updated_routes = [
                route for route in self.rib[prefix_key]
                if route.neighbor != rt.neighbor
        ] 
        
        # Check if there are still routes left for this prefix
        if len(updated_routes) > 0:
            # Other neighbors still advertise this prefix, update the list
            self.rib[prefix_key] = updated_routes
        else:
            # No routes remain for this prefix - CLEAN UP!
            # Delete the prefix key entirely from the RIB
            # This is important for next_hop() to correctly return None
            del self.rib[prefix_key]
        return 
    
    def convertToBinaryString(self, ip):
        # Helper function to convert IP address to binary string
        # Used for understanding prefix matching (though next_hop uses integer math)
        vals = ip.split(".")
        a = format(int(vals[0]), 'b').rjust(8, '0')
        b = format(int(vals[1]), 'b').rjust(8, '0')
        c = format(int(vals[2]), 'b').rjust(8, '0')
        d = format(int(vals[3]), 'b').rjust(8, '0')
        return a+b+c+d



    # ============================================================================
    # NEXT_HOP FUNCTION
    # ============================================================================
    # ALGORITHM: Find the best next-hop router for a destination IP address
    # 
    # This implements TWO selection criteria in order:
    # 
    # PHASE 1: LONGEST PREFIX MATCH
    # - Find ALL prefixes that contain the destination IP
    # - Select the prefix with the LONGEST prefix length (most specific match)
    # - Example: /24 is more specific than /16, so prefer /24
    # - This is the fundamental IP forwarding rule
    #
    # PHASE 2: SHORTEST AS PATH
    # - Among routes for the winning prefix, select the one with shorte
