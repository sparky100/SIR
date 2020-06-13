import numpy as np
import matplotlib.pyplot as plt
import random
import pandas as pd
import networkx as nx
#
# Stocahastic SIR model
#
# Deterministic
# 2 - 80 - 79
# 3 - 94  - 94
# 4 - 98.6 - 98 Test dfdsf


#Set up graph
G = nx.Graph()

SimulationDuration = 120  # assume rates in days
MaxNumEvents = 10000
MaxRuns = 200
RecoveryPeriod = 5  # 5 days to recover
InitialInfected = 5

# Scenarios  - #Dictionary of scenarios, population, country name, Ro, RecoveryPeriod

scenarios = [{"Country": "Scotland", "Population": 1000, "R0": 2, "RecoveryPeriod": 5}]
            

for scenario in scenarios:

    Population = scenario["Population"]
    Country = scenario["Country"]
    RecoveryPeriod = scenario["RecoveryPeriod"]
    R0 = scenario["R0"]
    Beta = R0 / RecoveryPeriod
    Gamma = 1. / RecoveryPeriod
    outb = 0
    rec = 0
    peak = 0
    EndTime: int = 0

    print("Scenario- Country", Country, "Beta ", Beta, "Gamma ", Gamma)

    Adj = np.random.randint (2, size = (Population,Population))  # creates random adjaceny matrix
    Adj = Adj.T * Adj # Creates Symmetric Matrix => not uni directional relationship    for run in range(1, MaxRuns):
        # Zero Arrays

    Adj.fill(1)
    
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
    
    G = nx.from_numpy_matrix(Adj) 

    SimTime = Times[0]
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
            #print(Event)
            #print(Infected)
        else:
            #print("Num Events ", NumEvents)
            Infected.append(Infected[NumEvents-1]-1)
            Recovered.append(Recovered[NumEvents-1]+1)
            Susceptible.append(Susceptible[NumEvents-1])
            Nodes[Node]=3    
            Event = "Recover"
            #print (Event)
            #print(Recovered)
        
        Times.append(SimTime)
                   
        if Recovered[NumEvents] > 30:
            outb = outb + 1
            rec = rec + Recovered[NumEvents]
            EndTime = EndTime + SimTime

#print(Nodes) 
#print(Infected)
#print(Times)
output=np.array([Times, Infected, Susceptible, Recovered])
## convert your array into a dataframe
df = pd.DataFrame (output)

## save to xlsx file
filepath = 'output.csv'
df.to_csv(filepath, index=False)
plt.plot(Times,Infected, label='Infected')
plt.plot(Times,Recovered,label='Recovered')
plt.plot(Times,Susceptible, label='Susceptible')
plt.xlabel('Time (days)')
plt.ylabel('People')
plt.title('SIR Network Model')
plt.legend()
plt.show()
    
 