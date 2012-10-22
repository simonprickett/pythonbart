import urllib2
from xml.dom.minidom import parseString

file = urllib2.urlopen('http://api.bart.gov/api/stn.aspx?cmd=stns&key=MW9S-E7SL-26DU-VV8V')
data = file.read()
file.close()

dom = parseString(data)
stations = dom.getElementsByTagName('stations')[0]
stationData = {}

print 'Begin reading data from SF BART API, please wait!'

for station in stations.getElementsByTagName('station'):
     stationAbbr = station.getElementsByTagName('abbr')[0].firstChild.nodeValue

     file = urllib2.urlopen('http://api.bart.gov/api/etd.aspx?cmd=etd&orig={stationAbbr}&key=MW9S-E7SL-26DU-VV8V'.format(stationAbbr = stationAbbr))
     data = file.read()
     file.close()

     dom = parseString(data)

     stationName = dom.getElementsByTagName('name')[0].firstChild.nodeValue
     
     stationEtds = dom.getElementsByTagName('etd')
     stationDestinations = {}

     for etd in stationEtds:
         destination = etd.getElementsByTagName('destination')[0].firstChild.nodeValue

         stationDestinationDepartures = []
         
         for estimate in etd.getElementsByTagName('estimate'):
             stationDestinationDeparture = {}
             
             minutesToDeparture = estimate.getElementsByTagName('minutes')[0].firstChild.nodeValue
             if (minutesToDeparture == 'Leaving'):
                  minutesToDeparture = '0'
             platform = estimate.getElementsByTagName('platform')[0].firstChild.nodeValue
             numCars = estimate.getElementsByTagName('length')[0].firstChild.nodeValue
             lineColor = estimate.getElementsByTagName('color')[0].firstChild.nodeValue

             stationDestinationDeparture['platform'] = platform
             stationDestinationDeparture['numCars'] = numCars
             stationDestinationDeparture['lineColor'] = lineColor
             stationDestinationDeparture['minutesToDeparture'] = minutesToDeparture

             stationDestinationDepartures.append(stationDestinationDeparture)
             
         stationDestinations[destination] = stationDestinationDepartures
         
     stationData[stationName] = stationDestinations

print 'Done reading data from SF BART API'
print ''

for stationName in stationData.keys():
     stationDestinations = stationData[stationName]
     print '********** DEPARTURES FROM {stationName} **********'.format(stationName= stationName)
     
     for stationDestination in stationDestinations.keys():
          print stationDestination

          for departure in stationDestinations[stationDestination]:
               print '- {numCars} car {lineColor} line train leaves in {minutesToDeparture} minutes from platform {platform}.'.format(numCars = departure['numCars'], lineColor = departure['lineColor'], minutesToDeparture = departure['minutesToDeparture'], platform = departure['platform'])

     
