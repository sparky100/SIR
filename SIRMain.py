import numpy as np
import matplotlib.pyplot as plt
import random

#
# Stocahastic SIR model k asdxcv cvx 
#
# Deterministic
# 2 - 80 - 79
# 3 - 94  - 94
# 4 - 98.6 - 98 Test dfdsf


SimulationDuration = 120  # assume rates in days
MaxNumEvents = 10000
MaxRuns = 200
RecoveryPeriod = 5  # 5 days to recover
InitialInfected = 1

# Scenarios  - #Dictionary of scenarios, population, country name, Ro, RecoveryPeriod

scenarios = [{"Country": "Scotland", "Population": 100, "R0": 2, "RecoveryPeriod": 5},
             {"Country": "Denmark", "Population": 100, "R0": 3, "RecoveryPeriod": 5},
             {"Country": "test", "Population": 100, "R0": 4, "RecoveryPeriod": 5}
             ]

for scenario in scenarios:

    Population = scenario["Population"]
    Country = scenario["Country"]
    RecoveryPeriod = scenario["RecoveryPeriod"]
    R0 = scenario["R0"]
    Beta = R0 / RecoveryPeriod
    Gamma = 1. / RecoveryPeriod
    InitialInfected = 1
    outb = 0
    rec = 0
    peak = 0
    EndTime: int = 0

    print("Scenario- Country", Country, "Beta ", Beta, "Gamma ", Gamma)

    for run in range(1, MaxRuns):
        # Zero Arrays

        Infected = np.zeros([MaxRuns, MaxNumEvents])
        Susceptible = np.zeros([MaxRuns, MaxNumEvents])
        Recovered = np.zeros([MaxRuns, MaxNumEvents])
        SimTime = np.zeros([MaxRuns, MaxNumEvents])

        Susceptible[run, 0] = Population
        Recovered[run, 0] = 0
        Infected[run, 0] = InitialInfected
        SimTime[run, 0] = 0
        NumEvents = 0

 
        while (SimTime[run, NumEvents] < SimulationDuration and NumEvents < MaxNumEvents and Infected[
            run, NumEvents] > 0):

            Rate1 = (Beta * Susceptible[run, NumEvents] * Infected[run, NumEvents]) / Population
            Rate2 = Gamma * Infected[run, NumEvents]
            TotalRate = (Rate1 + Rate2)
            TimeBetweenEvents = 1. / TotalRate
            NextTime = random.expovariate(TotalRate)
            NumEvents = NumEvents + 1
            SimTime[run, NumEvents] = SimTime[run, NumEvents - 1] + NextTime

            SelectEvent = random.random()

            if SelectEvent < (Rate1 / TotalRate):  # Infected
                Infected[run, NumEvents] = Infected[run, NumEvents - 1] + 1
                Susceptible[run, NumEvents] = Susceptible[run, NumEvents - 1] - 1
                Recovered[run, NumEvents] = Recovered[run, NumEvents - 1]
                Event = "Infect"
            else:
                Infected[run, NumEvents] = Infected[run, NumEvents - 1] - 1
                Recovered[run, NumEvents] = Recovered[run, NumEvents - 1] + 1
                Susceptible[run, NumEvents] = Susceptible[run, NumEvents - 1]
                Event = "Recover"

                REff = (Susceptible / Population) * (Beta / Gamma)

        # print("Time", SimTime[run, NumEvents], "Select Event ", SelectEvent, "Event", NumEvents, "Type", Event,"Susceptibles",Susceptible[run,NumEvents], "Recovered", Recovered[run, NumEvents])
        if Recovered[run, NumEvents] > 30:
            outb = outb + 1
            rec = rec + Recovered[run, NumEvents]
            peak = peak + np.max(Infected[0:MaxNumEvents])
            EndTime = EndTime + SimTime[run, NumEvents]
    #         peaktime = peaktime + np.where(Infected[0:MaxNumEvents] == np.max(Infected[0:MaxNumEvents]))
    #         plt.plot(SimTime[run, 0:NumEvents] , Infected[run , 0:NumEvents])

    if outb > 0:
        OutbreakProbability = (outb / MaxRuns)
        AverageTotalInfected = rec / outb
        peak = peak / outb
        EndTime = EndTime / outb
    # plt.show()
    else:
        OutbreakProbability = 0

    print("R0", R0, "Average Duration", EndTime ,"Outbreaks", outb, "Simulations", MaxRuns, "Outbreak Probability",
          OutbreakProbability, "Avg Infected", AverageTotalInfected, "Peak", peak)
