import sys
from xml.dom import minidom
import random
import os
import xml.etree.ElementTree as ET

testMode = True


#Funcion que crea y almacena los agentes mediante randomSearch
def createRepo():
    #Cogemos todos los datos de boarepository
    for t in biddingStrategies:
        bidStrategiesList.append(t.getAttribute('classpath'))

    for t in acceptanceConditions:
        accConditionsList.append(t.getAttribute('classpath'))

    for t in opponentmodels:
        opModelsList.append(t.getAttribute('classpath'))

    for t in omstrategies:
        omStrategisList.append(t.getAttribute('classpath'))



    #Creamos 40 iteraciones de agentes aleatorios y realizamos 100 iteraciones como mucho para evitar paralizar el programa
    partiesSelected = []
    iterations = 0
    while len(partiesSelected) < 40 and iterations < 100:
        auxParty = {
            "biddingStrategy": random.choice(bidStrategiesList),
            "acceptanceStrategy": random.choice(accConditionsList),
            "opponentModel": random.choice(opModelsList),
            "omStrategy": random.choice(omStrategisList)
        }
        if auxParty not in partiesSelected:
            partiesSelected.append(auxParty)
        iterations += 1

    #Los metemos en boapartyrepo.xml

    doc = minidom.parseString("<boaPartiesList/>")
    root = doc.documentElement
    partyNumber = 0
    for element in partiesSelected:
        party = doc.createElement("boaparties")
        party.setAttribute("partyName", "party" + str(partyNumber))
        party.appendChild(doc.createElement("properties"))

        biddingSt = doc.createElement("biddingStrategy")
        elementStrat = element["biddingStrategy"]
        if elementStrat in biddingParameters:
            for par in biddingParameters[elementStrat]:
                parameter = doc.createElement("parameters")
                parameter.setAttribute("name", str(par))
                parameter.setAttribute("value", str(biddingParameters[elementStrat][par]))
                biddingSt.appendChild(parameter)
        item = doc.createElement("item")
        item.setAttribute("classpath", element["biddingStrategy"])
        biddingSt.appendChild(item)
        party.appendChild(biddingSt)

        acceptSt = doc.createElement("acceptanceStrategy")
        elementStrat = element["acceptanceStrategy"]
        if elementStrat in acceptanceParameters:
            for par in acceptanceParameters[elementStrat]:
                parameter = doc.createElement("parameters")
                parameter.setAttribute("name", str(par))
                parameter.setAttribute("value", str(acceptanceParameters[elementStrat][par]))
                acceptSt.appendChild(parameter)
        item = doc.createElement("item")
        item.setAttribute("classpath", element["acceptanceStrategy"])
        acceptSt.appendChild(item)
        party.appendChild(acceptSt)

        opMod = doc.createElement("opponentModel")
        elementStrat = element["opponentModel"]
        if elementStrat in opModParameters:
            for par in opModParameters[elementStrat]:
                parameter = doc.createElement("parameters")
                parameter.setAttribute("name", str(par))
                parameter.setAttribute("value", str(opModParameters[elementStrat][par]))
                opMod.appendChild(parameter)
        item = doc.createElement("item")
        item.setAttribute("classpath", element["opponentModel"])
        opMod.appendChild(item)
        party.appendChild(opMod)

        omStat = doc.createElement("omStrategy")
        elementStrat = element["omStrategy"]
        if elementStrat in opModStratParameters:
            for par in opModStratParameters[elementStrat]:
                parameter = doc.createElement("parameters")
                parameter.setAttribute("name", str(par))
                parameter.setAttribute("value", str(opModStratParameters[elementStrat][par]))
                omStat.appendChild(parameter)
        item = doc.createElement("item")
        item.setAttribute("classpath", elementStrat)
        omStat.appendChild(item)
        party.appendChild(omStat)


        root.appendChild(party)
        partyNumber += 1

        with open("boapartyrepo.xml", "w") as f:
            f.write(doc.toprettyxml())

    return partiesSelected

#Funcion que lanza los diferentes torneos
def LaunchTournaments(party, domains, opponents):

    for domain in domains:
        for opponent in opponents:
            xmlTournament = minidom.parse("tournament.xml")
            partyRepItems = xmlTournament.getElementsByTagName("partyRepItems")[0]
            opponentParty = xmlTournament.createElement("party")
            opponentParty.setAttribute("classPath", opponent)
            
            partyRepItems.appendChild(opponentParty)
            partyRepItems.appendChild(party)

            partyProfileItems = xmlTournament.getElementsByTagName("partyProfileItems")[0]
            item1 = xmlTournament.createElement("item")
            item1.setAttribute("url", domain[0])
            item2 = xmlTournament.createElement("item")
            item2.setAttribute("url", domain[1])

            partyProfileItems.appendChild(item1)
            partyProfileItems.appendChild(item2)

            with open("tournament1.xml", "w") as f:
                 f.write(xmlTournament.toxml())
            logName = "" + party.getAttribute("partyName") + "_" + opponentParty.getAttribute("classPath") + "_" + domain[0][domain[0].rfind("/"):-1]
            if(not testMode):
                command = "java -cp genius-9.1.13.jar genius.cli.Runner tournament1.xml Results/" + logName
            else:
                command = "java -cp genius-9.1.13.jar genius.cli.Runner tournament1.xml TestResults/" + logName
            os.system('cmd /c' + command)

if __name__ == '__main__':

    #Almacenamos los parametros necesarios para algunos de los componentes. En caso de usar esos componentes se añadiran los parametros
    biddingParameters = {
        "negotiator.boaframework.offeringstrategy.other.TimeDependent_Offering": {"e": 1, "k": 0, "max": 0.99, "min": 0},
        "negotiator.boaframework.offeringstrategy.IAMHaggler_Test_Offering": {"s": 100, "r": 36},
        "negotiator.boaframework.offeringstrategy.anac2010.IAMCrazyHaggler_Offering": {"b": 0.9},
        "negotiator.boaframework.offeringstrategy.other.GeniusTimeDependent_Offering": {"k": 0, "min": 0, "e": 1, "max": 0.99}

    }

    acceptanceParameters = {
        "negotiator.boaframework.acceptanceconditions.other.AC_Next": {"a": 1, "b": 0},
        "negotiator.boaframework.acceptanceconditions.other.AC_Gap": {"c": 0.01},
        "negotiator.boaframework.acceptanceconditions.other.AC_Time": {"t": 0.99},
        "negotiator.boaframework.acceptanceconditions.other.AC_CombiV4": {"b": 0, "e": 0.8, "d": 0, "a": 1, "c": 1},
        "negotiator.boaframework.acceptanceconditions.other.AC_CombiV3": {"c": 0.95, "t": 0.99, "a": 1, "b": 0},
        "negotiator.boaframework.acceptanceconditions.other.AC_CombiV2": {"c": 0.8, "a": 1, "t": 0.99, "b": 0, "d": 0.95},
        "negotiator.boaframework.acceptanceconditions.other.AC_CombiMaxInWindow": {"t": 0.98},
        "negotiator.boaframework.acceptanceconditions.other.AC_Const": {"c": 0.9},
        "negotiator.boaframework.acceptanceconditions.other.AC_Previous": {"a": 1, "b": 0},
        "negotiator.boaframework.acceptanceconditions.anac2012.AC_TheNegotiatorReloaded": {"bd": 0, "t": 0.99, "ad": 1.05, "a": 1, "b": 0, "c": 0.98}

    }

    opModParameters = {
        "negotiator.boaframework.opponentmodel.IAMhagglerBayesianModel": {"u": 0, "b": 1},
        "negotiator.boaframework.opponentmodel.BayesianModel": {"m": 0}
    }

    opModStratParameters = {
    "negotiator.boaframework.omstrategy.BestBid": {"t": 1.1},
    "negotiator.boaframework.omstrategy.NullStrategy": {"t": 1.1},
    "negotiator.boaframework.omstrategy.OfferBestN": {"n": 3.0, "t": 1.1},
}

    if not testMode: 
        #Creamos los 40 agentes
        data = sys.argv[1]
        xmldoc = minidom.parse(data)
        biddingStrategies = xmldoc.getElementsByTagName('biddingstrategy')
        acceptanceConditions = xmldoc.getElementsByTagName('acceptancecondition')
        opponentmodels = xmldoc.getElementsByTagName('opponentmodel')
        omstrategies = xmldoc.getElementsByTagName('omstrategy')

        bidStrategiesList = []
        accConditionsList = []
        opModelsList = []
        omStrategisList = []
        partiesSelected = []
        partiesSelected = createRepo()
        domains = [("file:etc/templates/ANAC2015/group1-university/University_util1.xml", "file:etc/templates/ANAC2015/group1-university/University_util2.xml"),
                ("file:etc/templates/anac/y2011/Laptop/laptop_buyer_utility.xml", "file:etc/templates/anac/y2011/Laptop/laptop_seller_utility.xml"),
                ("file:etc/templates/ANAC2016/parsCat/profile1.xml", "file:etc/templates/ANAC2016/parsCat/profile2.xml")]
        opponents = ["agents.anac.y2018.agreeableagent2018.AgreeableAgent2018", "agents.anac.y2017.ponpokoagent.PonPokoAgent", "agents.anac.y2016.caduceus.Caduceus"]

    else: 
        #Si estamos en testMode quiere decir que ya tenemos una party ganadora. Lanzaremos torneos solo con ella
        domains = [("file:etc/templates/ANAC2015/group7-movie/movie-profile1.xml", "file:etc/templates/ANAC2015/group7-movie/movie-profile2.xml"),
                    ("file:etc/templates/partydomain/party1_utility.xml", "file:etc/templates/partydomain/party2_utility.xml"),
                    ("file:etc/templates/ANAC2016/Maxoops/WindFarm_util1.xml", "file:etc/templates/ANAC2016/Maxoops/WindFarm_util2.xml")]
        opponents = ["agents.TimeDependentAgentBoulware", "agents.TimeDependentAgentConceder", "agents.BayesianAgent"]
        winnerParty = "party0"

    xmlBoaParties = minidom.parse("boapartyrepo.xml")

    boaParties = xmlBoaParties.getElementsByTagName('boaparties')
    
    #En caso de estar en modo test tan solo lanzaremos
    for party in boaParties:
        if(testMode and party.getAttribute("partyName") != winnerParty): break
        party.tagName = "boaparty"
        LaunchTournaments(party, domains, opponents)



