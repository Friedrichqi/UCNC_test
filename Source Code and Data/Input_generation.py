import random
import sys
sys.stdout = open('Input.in', 'w')

# Function to generate random inputs for commodities
def generate_random_commodities():
    commodities = []
    for id_commodity in range(num_commodities):
        # Randomly choose the number of packets for this commodity
        #num_packets = random.randint(1, max_packets)
        num_packets = max_time * lamb[id_commodity]
        
        
        # Randomly choose the number of service functions for this commodity
        num_services = random.randint(1, max_services)
        
        #generate source and destination, with 50% unicast and 50%multicast
        if random.random() < 0.5:
            num_dest = 1
        else:
            num_dest = random.randint(2, 4)
        dest = random.sample(range(1, 12), num_dest)
        dest.sort()
        sour = random.randint(1, 11)
        
        
        # Generate the service function chain for this commodity
        service_chain = []
        for _ in range(num_services):
            r = round(random.uniform(0.01, 2), 2)
            epsilon = round(random.uniform(1, 2), 2)
            service_chain.append((r, epsilon))
            
        
        # Append the commodity to the list
        commodity = {
            'num_packets': num_packets,
            'service_chain': service_chain,
            'sour': sour,
            "dest": dest
        }
        commodities.append(commodity)
    return commodities

# Example usage
num_commodities = 10  # Number of commodities
lamb = [0 for _ in range(num_commodities)]
for i in range(num_commodities):
    lamb[i] = random.randint(2, 2)
max_time = 999    # Maximum arrival time
max_services = 5     # Maximum number of service functions in a chain

# Generate random commodities
random_commodities = generate_random_commodities()
# Printing the generated commodities
print(num_commodities)
for id_commodity in range(num_commodities):
    print(id_commodity)
    print(random_commodities[id_commodity]['sour'], *random_commodities[id_commodity]['dest'])
    for i in range(len(random_commodities[id_commodity]['service_chain'])):
        print(*random_commodities[id_commodity]['service_chain'][i], end=' ')
    print()

 
print()

# Generate input for each commodity
for t in range(max_time):
    print(t)
    for id_commodity in range(num_commodities):
        num = random.randint(0, 2 * lamb[i])
        if num == 0:
            continue
        #random_commodities[id_commodity]['num_packets'] = random_commodities[id_commodity]['num_packets'] - num
        print(id_commodity, num)
    print()
        