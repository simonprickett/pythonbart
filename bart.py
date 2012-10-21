import urllib2
from xml.dom.minidom import parseString

file = urllib2.urlopen('http://api.bart.gov/api/stn.aspx?cmd=stns&key=MW9S-E7SL-26DU-VV8V')
data = file.read()
file.close()

dom = parseString(data)
stations = dom.getElementsByTagName('stations')[0]
stationData = {}

for station in stations.getElementsByTagName('station'):
     stationAbbr = station.getElementsByTagName('abbr')[0].firstChild.nodeValue

     file = urllib2.urlopen('http://api.bart.gov/api/etd.aspx?cmd=etd&orig={stationAbbr}&key=MW9S-E7SL-26DU-VV8V'.format(stationAbbr = stationAbbr))
     data = file.read()
     file.close()

     dom = parseString(data)

     stationName = dom.getElementsByTagName('name')[0].firstChild.nodeValue
     print '********** DEPARTURES FROM {stationName} **********'.format(stationName = stationName)
     
     stationEtds = dom.getElementsByTagName('etd')
     stationDestinations = {}

     for etd in stationEtds:
         destination = etd.getElementsByTagName('destination')[0].firstChild.nodeValue
         print 'Destination: {destination}'.format(destination = destination) 

         stationDestinationDepartures = []
         
         for estimate in etd.getElementsByTagName('estimate'):
             stationDestinationDeparture = {}
             
             minutesToDeparture = estimate.getElementsByTagName('minutes')[0].firstChild.nodeValue
             if (minutesToDeparture == 'Leaving'):
                  minutesToDeparture = '0'
             platform = estimate.getElementsByTagName('platform')[0].firstChild.nodeValue
             numCars = estimate.getElementsByTagName('length')[0].firstChild.nodeValue
             lineColor = estimate.getElementsByTagName('color')[0].firstChild.nodeValue
             print '- {numCars} car {lineColor} line train leaves in {minutesToDeparture} minutes from platform {platform}.'.format(numCars = numCars, lineColor = lineColor, minutesToDeparture = minutesToDeparture, platform = platform)

             stationDestinationDeparture['platform'] = platform
             stationDestinationDeparture['numCars'] = numCars
             stationDestinationDeparture['lineColor'] = lineColor
             stationDestinationDeparture['minutesToDeparture'] = minutesToDeparture

             stationDestinationDepartures.append(stationDestinationDeparture)
             
         stationDestinations[destination] = stationDestinationDepartures
         
     stationData[stationAbbr] = stationDestinations
     
