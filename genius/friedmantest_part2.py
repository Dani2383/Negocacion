from scipy import stats
import os
import numpy as np
import scikit_posthocs as sp
import csv
import statistics as st




if __name__ == '__main__':
    #Estructuras de datos utilizadas para guardar las utilidades
    BOA_1 = "boa-negotiator.boaframework.offeringstrategy.anac2010.Yushu"
    BOA_2 = "boa-negotiator.boaframework.offeringstrategy.anac2010.AgentK_Offering"
    agents = [BOA_1, BOA_2, "Boulware", "Conceder", "Bayesian"]
    utilitiesBoa1 = { BOA_1: [], BOA_2: [], "Boulware": [], "Conceder": [], "Bayesian": []}
    utilitiesBoa2 = {BOA_1: [], BOA_2: [], "Boulware": [], "Conceder": [], "Bayesian": []}
    utilitiesBoulware = {BOA_1: [], BOA_2: [], "Boulware": [], "Conceder": [], "Bayesian": []}
    utilitiesConceder = {BOA_1: [], BOA_2: [], "Boulware": [], "Conceder": [], "Bayesian": []}
    utilitiesBayesian = {BOA_1: [], BOA_2: [], "Boulware": [], "Conceder": [], "Bayesian": []}
    utilities = {BOA_1: utilitiesBoa1, BOA_2: utilitiesBoa2, 'Boulware': utilitiesBoulware, 'Conceder': utilitiesConceder, 'Bayesian': utilitiesBayesian}
    
    # Abrimos los archivos de dominio. Lo abiremos una vez por agente para poder iterar varias veces sobre cada uno
    
    dir = 'TestResults1/Part2/'
    for f in os.listdir(dir):
        file = os.path.join(dir, f)
        if os.path.isfile(file):

            #Estructuras de datos utilizadas para guardar las utilidades
            domainUtilitiesBoa1 = {BOA_1: [], BOA_2: [], "Boulware": [], "Conceder": [], "Bayesian": []}
            domainUtilitiesBoa2 = {BOA_1: [], BOA_2: [], "Boulware": [], "Conceder": [], "Bayesian": []}
            domainUtilitiesBoulware = {BOA_1: [], BOA_2: [], "Boulware": [], "Conceder": [], "Bayesian": []}
            domainUtilitiesConceder = {BOA_1: [], BOA_2: [], "Boulware": [], "Conceder": [], "Bayesian": []}
            domainUtilitiesBayesian = {BOA_1: [], BOA_2: [], "Boulware": [], "Conceder": [], "Bayesian": []}
            domainUtilities = {BOA_1: domainUtilitiesBoa1, BOA_2: domainUtilitiesBoa2, 'Boulware': domainUtilitiesBoulware, 'Conceder': domainUtilitiesConceder, 'Bayesian': domainUtilitiesBayesian}
            
            # Iteramos por los diferentes agentes, guardando las utilidades de todos ellos
            for agent in agents:
                with open(file) as csv_file:
                    
                    csv_reader = csv.reader(csv_file, delimiter=';')
                    for row in csv_reader:
                        if row[12].startswith(agent):
                            for agent2 in agents:
                                if row[13].startswith(agent2):
                                    domainUtilities[agent][agent2].append(float(row[14]))
                        elif row[13].startswith(agent):
                            if row[12].startswith(agent2):
                                    domainUtilities[agent][agent2].append(float(row[15]))
                            
            # Guardamos las utilidades en el diccionario general
            for agent in agents:
                for agent2 in agents:
                    utilities[agent][agent2].append(st.fmean(domainUtilities[agent][agent2]))


    boaUtilities1 = []
    boaUtilities2 = []
    boulwareUtilities = []
    concederUtilities = []
    bayesianUtilities = []

    for agent in agents:
        boaUtilities1.extend(utilities[BOA_1][agent])
    for agent in agents:
        boaUtilities2.extend(utilities[BOA_2][agent])
    for agent in agents:
        boulwareUtilities.extend(utilities["Boulware"][agent])
    for agent in agents:
        concederUtilities.extend(utilities["Conceder"][agent])
    for agent in agents:
        bayesianUtilities.extend(utilities["Bayesian"][agent])

    print("boa1 " + str(st.fmean(boaUtilities1)))
    print("boaUtilities2 " + str(st.fmean(boaUtilities2)))
    print("boulware " + str(st.fmean(boulwareUtilities)))
    print("conceder " + str(st.fmean(concederUtilities)))
    print("bayesian " + str(st.fmean(bayesianUtilities)))

    # Realizamos el test de friedman sobre los datos obtenidos
    print(stats.friedmanchisquare(boaUtilities1, boaUtilities2, boulwareUtilities, concederUtilities, bayesianUtilities))
    
    # Realizamos el test de nemenyi y guardamos la matriz de resultados en un archivo csv
    data = np.array([boaUtilities1, boaUtilities2, boulwareUtilities, concederUtilities, bayesianUtilities])
    dp = sp.posthoc_nemenyi_friedman(data.T)
    print(dp)
    dp.to_csv("dpTest.csv", index=False)