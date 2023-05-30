import os
import csv
import statistics as st
from scipy import stats
import numpy as np
import scikit_posthocs as sp
import pandas


numParties = 40
opponents = ["agents.anac.y2018.agreeableagent2018.AgreeableAgent2018", "agents.anac.y2017.ponpokoagent.PonPokoAgent"]

if __name__ == "__main__":
    utilities = {}
    meanUtilities = {}
    
    for i in range(numParties):
        party = 'party' + str(i)
        utilParty = []

        # Abrimos todos los archivos generados con resultados y obtenemos las utilidades de nuestros agentes
        # Sabemos la columna en la que se situa su utilidad dependiendo de en la que este el nombre de
        # nuestro agente
        for opponent in opponents:
            dir = 'Results/' + party + '_' + opponent + '_'
            for f in os.listdir(dir):
                file = os.path.join(dir, f)
                if os.path.isfile(file):
                    with open(file) as csv_file:
                        csv_reader = csv.reader(csv_file, delimiter=';')
                        rowNum = 0
                        utilTournament = []
                        for row in csv_reader:
                            if rowNum < 2: rowNum += 1
                            else:
                                rowNum += 1
                                if row[12].startswith('boa-'):
                                    utilTournament.append(float(row[14]))
                                else: utilTournament.append(float(row[15]))
                        utilParty.append(st.fmean(utilTournament))
        utilities[party] = utilParty



    # Ordenamos las utilidades de nuestros agentes por orden de mayor a menor utilidad. Obtenemos
    # el mejor resultado con la party0
    for party in utilities.keys():
        meanUtilities[party] = st.fmean(utilities[party])
    sortedParties = dict(sorted(meanUtilities.items(), key=lambda x:x[1], reverse=True))
    print(sortedParties)
    