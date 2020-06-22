

import numpy as np
import matplotlib.pyplot as plt
import random
import pandas as pd
import networkx as nx

## Visualise Final Graph
def create_graph(G, Population,Nodes, SimTime, positions):
       
    color_map = []
    for node in G:
        if (Nodes[node] ==1):
            color_map.append('blue') #susceptible
        elif (Nodes [node] ==2 ): 
            color_map.append('black') #infected
        else:
            color_map.append('red') #recovered
                    
    plt.title('Epidemic Network Time ='+ str(int(SimTime)))
    nx.draw(G, node_color=color_map, pos=positions, node_size=50, width=0.5 )
    plt.savefig(str(round(SimTime))+".png")

    # convert -delay 20 -loop 0 $(ls *.png -t -r) animated.gif to create


#
# Stocahastic SIR model
#
# Deterministic
# 2 - 80 - 79
# 3 - 94  - 94
# 4 - 98.6 - 98 Test 


#Set up graph
G = nx.Graph()

SimulationDuration = 120  # assume rates in days
MaxNumEvents = 10000
MaxRuns = 200
RecoveryPeriod = 5  # 5 days to recover
InitialInfected = 2

# Scenarios  - #Dictionary of scenarios, population, country name, Ro, RecoveryPeriod

scenarios = [{"Country": "Scotland", "Population": 200, "Beta": 4, "RecoveryPeriod": 5}]
            

for scenario in scenarios:

    Population = scenario["Population"]
    Country = scenario["Country"]
    RecoveryPeriod = scenario["RecoveryPeriod"]
    #R0 = scenario["R0"]
    Beta = scenario["Beta"]
    Gamma = 1. / RecoveryPeriod
    outb = 0
    rec = 0
    peak = 0
    EndTime: int = 0

    print("Scenario- Country", Country, "Beta ", Beta, "Gamma ", Gamma)

    Adj = np.random.randint (2, size = (Population,Population))  # creates random adjaceny matrix
    Adj = Adj.T * Adj # Creates Symmetric Matrix => not uni directional relationship    for run in range(1, MaxRuns):
        # Zero Arrays

    Adj.fill(1) # set connections between all
    
    Nodes = np.zeros(Population)
        
    #Initial conditions
    Infected=[InitialInfected] 
    Susceptible=[Population-InitialInfected] 
    Recovered=[0]
    Times =[0]

    
    Nodes[0:InitialInfected].fill(2) #Set initial Infected
    
    Nodes[np.where(Nodes==0)]=1 # If Infected Updated Susceptible Flag
    Nodes=Nodes.astype(int)
    np.random.shuffle(Nodes) # shuffle infected nodes
    #print("Initial Setup" ,Nodes)
    
    #Assume 3 types of people
    #Low, Medium and High
    #Low have 4 connections, Medium has 10 connections and High = 10 connections
      

    Low=4
    Medium=8
    High=20

    LowProp = .3
    MedProp = .2
    HighProp = .5

    LowNum = int(Population*LowProp)
    MedNum = int(Population*MedProp)
    HighNum = int(Population*HighProp)
    
    configmatrix=[Low]*LowNum + [Medium]*MedNum + [High]*HighNum
    #sum of degrees mut be even
    if (sum(configmatrix) % 2 > 0):
        configmatrix[0]=configmatrix[0]+1           

    cm=np.array(configmatrix)
    np.random.shuffle(cm)

    G=nx.configuration_model(cm) # Create graph from configuration model
    G=nx.Graph(G)
    positions=nx.spring_layout(G)


    #G = nx.from_numpy_matrix(Adj) #Generate graph from adjacency matrix
    ## Visualise Initial Graph
    #pos=nx.spring_layout(G)
    #nx.draw(G,pos)
    
    Adj = nx.to_numpy_array(G) #Generates Adjaceny matrix from graph
    #print(Adj)
    SimTime = Times[0]
    create_graph(G, Population,Nodes, SimTime, positions)

    NumEvents = 0
    print("Initial Infected ", Infected[NumEvents])
 
    while (SimTime < SimulationDuration and NumEvents < MaxNumEvents and Infected[NumEvents] > 0):

        Rate1 = Beta*Adj.dot(Nodes==2)*(Nodes==1)/Population
        

        Rate2 = Gamma * (Nodes==2)
        #Create matrix of rates
        
        Allprops=np.concatenate((Rate1, Rate2)) #Propensity for all events 
        TotalRate=sum(Rate1)+sum(Rate2) #Sum of all propensities
       # print(sum(Rate1))
       # print(sum(Rate2))
        
        TimeBetweenEvents = 1. / TotalRate
        NextTime = random.expovariate(TotalRate)
        NumEvents = NumEvents + 1
        SimTime = SimTime + NextTime

        SelectEvent = random.random()
        CumSum=np.cumsum(np.concatenate((Rate1, Rate2)))/TotalRate
        EventId=CumSum.searchsorted(SelectEvent)
        #Determine which Node and Which Reaction
        Reaction=EventId // Population # from zero
        Node = EventId % Population # from zero
   #     print(Nodes)
   #     print("Event id", EventId, "Reaction ", Reaction, "Node ", Node)
        if Reaction==0:  # Infected
            Infected.append(Infected[NumEvents-1]+1)
            Recovered.append(Recovered[NumEvents-1])
            Susceptible.append(Susceptible[NumEvents-1]-1)
            Nodes[Node]=2 
            Event = "Infect"
#            print(Event)
#            print(count(Infected), count(Recovered))
        else:
            #print("Num Events ", NumEvents)
            Infected.append(Infected[NumEvents-1]-1)
            Recovered.append(Recovered[NumEvents-1]+1)
            Susceptible.append(Susceptible[NumEvents-1])
            Nodes[Node]=3    
            Event = "Recover"
#            print (Event)
#            print(count(Infected), count(Recovered))
        
        Times.append(SimTime)

        if (NumEvents % 2 ==0): #
            create_graph(G, Population,Nodes, SimTime, positions)

                   
        if Recovered[NumEvents] > 30:
            outb = outb + 1
            rec = rec + Recovered[NumEvents]
            EndTime = EndTime + SimTime

#print(Nodes[NumEvents]) 
print(Infected[NumEvents])
print(Recovered[NumEvents])
print(Times[NumEvents])
print(NumEvents)
#Final Output
create_graph(G, Population,Nodes, SimTime, positions)

output=np.column_stack((Times,Infected,Susceptible,Recovered))
## convert your array into a dataframe
df = pd.DataFrame (output)

## save to xlsx file
filepath = 'output.csv'
df.to_csv(filepath, index=False)
plt.close()
plt.plot(Times,Infected, label='Infected')
plt.plot(Times,Recovered,label='Recovered')
plt.plot(Times,Susceptible, label='Susceptible')
plt.xlabel('Time (days)')
plt.ylabel('People')
plt.title('SIR Network Model')
plt.legend()
plt.show()

