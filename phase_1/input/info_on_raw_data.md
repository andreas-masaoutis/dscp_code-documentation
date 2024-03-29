﻿[Data and descriptions found here](http://stat-computing.org/dataexpo/2009/the-data.html)

The data comes originally from [RITA ](http://www.transtats.bts.gov/OT_Delay/OT_DelayCause1.asp) where it is described in detail. You can download the data there, or from the bzipped csv files listed below. These files have derivable variables removed, are packaged in yearly chunks and have been more heavily compressed than the originals.
Data range from 1987 to 2008

Variable description:

1. Year 	1987-2008
2. Month 	1-12
3. DayofMonth 	1-31
4. DayOfWeek 	1 (Monday) - 7 (Sunday)
5. DepTime 	actual departure time (local, hhmm)
6. CRSDepTime 	scheduled departure time (local, hhmm)
7. ArrTime 	actual arrival time (local, hhmm)
8. CRSArrTime 	scheduled arrival time (local, hhmm)
9. UniqueCarrier 	unique carrier code
10. FlightNum 	flight number
11. TailNum 	plane tail number
12. ActualElapsedTime 	in minutes
13. CRSElapsedTime 	in minutes
14. AirTime 	in minutes
15. ArrDelay 	arrival delay, in minutes
16. DepDelay 	departure delay, in minutes
17. Origin 	origin IATA airport code
18. Dest 	destination IATA airport code
19. Distance 	in miles
20. TaxiIn 	taxi in time, in minutes
21. TaxiOut 	taxi out time in minutes
22. Cancelled 	was the flight cancelled?
23. CancellationCode 	reason for cancellation (A=carrier, B=weather, C=NAS, D=security)
24. Diverted 	1 = yes, 0 = no
25. CarrierDelay 	in minutes
26. WeatherDelay 	in minutes
27. NASDelay 	in minutes
28. SecurityDelay 	in minutes
29. LateAircraftDelay 	in minutes


[Supplemental data](http://stat-computing.org/dataexpo/2009/supplemental-data.html)


Airports
airports.csv describes the locations of US airports, with the fields:
iata: the international airport abbreviation code
name of the airport
city and country in which airport is located.
lat and long: the latitude and longitude of the airport
This majority of this data comes from the FAA, but a few extra airports (mainly military bases and US protectorates) were collected from other web sources by Ryan Hafen and Hadley Wickham.


Carrier codes
Listing of carrier codes with full names: carriers.csv


Planes
You can find out information about individual planes by googling the tail number or by looking it up in the FAA database. plane-data.csv is a csv file produced from the (some of) the data on that page.


Weather
Meteorological data is available from (among many others) NOAA and weather underground. The call sign for airport weather stations can be constructed by adding K to the airport code, e.g. KORD, KLAX, KSEA.

