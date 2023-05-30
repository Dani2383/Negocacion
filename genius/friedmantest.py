from scipy import stats
import os
import numpy as np
import scikit_posthocs as sp
import csv
import statistics as st




if __name__ == '__main__':
    #Estructuras de datos utilizadas para guardar las utilidades
    agents = ["boa", "Boulware", "Conceder", "Bayesian"]
    utilitiesBoa = {'boa': [], "Boulware": [], "Conceder": [], "Bayesian": []}
    utilitiesBoulware = {'boa': [], "Boulware": [], "Conceder": [], "Bayesian": []}
    utilitiesConceder = {'boa': [], "Boulware": [], "Conceder": [], "Bayesian": []}
    utilitiesBayesian = {'boa': [], "Boulware": [], "Conceder": [], "Bayesian": []}
    utilities = {'boa': utilitiesBoa, 'Boulware': utilitiesBoulware, 'Conceder': utilitiesConceder, 'Bayesian': utilitiesBayesian}

    #Abrimos los archivos de dominio
    dir = 'TestResults1/'
    for f in os.listdir(dir):
        file = os.path.join(dir, f)
        if os.path.isfile(file):
            i = 0
            domainUtilitiesBoa = {'boa': [], "Boulware": [], "Conceder": [], "Bayesian": []}
            domainUtilitiesBoulware = {'boa': [], "Boulware": [], "Conceder": [], "Bayesian": []}
            domainUtilitiesConceder = {'boa': [], "Boulware": [], "Conceder": [], "Bayesian": []}
            domainUtilitiesBayesian = {'boa': [], "Boulware": [], "Conceder": [], "Bayesian": []}
            domainUtilities = {'boa': domainUtilitiesBoa, 'Boulware': domainUtilitiesBoulware, 'Conceder': domainUtilitiesConceder, 'Bayesian': domainUtilitiesBayesian}
            
            # Recorremos todos los agentes y guardamos las utilidades en el diccionario que toque
            # Distinguimos a que agente corresponde cada utilidad mirando los nombres en sus respectivas columnas
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


    boaUtilities = []
    boulwareUtilities = []
    concederUtilities = []
    bayesianUtilities = []

    for agent in agents:
        boaUtilities.extend(utilities["boa"][agent])
    for agent in agents:
        boulwareUtilities.extend(utilities["Boulware"][agent])
    for agent in agents:
        concederUtilities.extend(utilities["Conceder"][agent])
    for agent in agents:
        bayesianUtilities.extend(utilities["Bayesian"][agent])

    print("boa1 " + str(st.fmean(boaUtilities)))
    print("boulware " + str(st.fmean(boulwareUtilities)))
    print("conceder " + str(st.fmean(concederUtilities)))
    print("bayesian " + str(st.fmean(bayesianUtilities)))

    # Realizamos el test de friedman sobre los datos obtenidos
    print(stats.friedmanchisquare(boaUtilities, boulwareUtilities, concederUtilities, bayesianUtilities))
    
    # Realizamos el test de nemenyi y guardamos la matriz de resultados en un archivo csv
    data = np.array([boaUtilities, boulwareUtilities, concederUtilities, bayesianUtilities])
    dp = sp.posthoc_nemenyi_friedman(data.T)
    print(dp)
    dp.to_csv("dpTest.csv", index=False)