
## Introduction

The motivation for the present project is the problem of flight delays in the USA. It is a problem that has plagued this industry for some time.

> Flight delay is a serious and widespread problem in the United States. Increasing flight delays place a significant strain on the US air travel system and cost airlines, passengers, and society at many billions of dollars each year.[^1] 
[^1]: *Total Delay Impact Study: A Comprehensive Assessment of the Costs and Impacts of Flight Delays in the United States. Final Report October, 2010, page vii*

The occasion for the project was a competition held by *The Statistical Computing and Statistical Graphics* sections of the *American Statistical Association*, held in 2008. The data that has been made available were 'flight arrival and departure details for all commercial flights within the USA, from October 1987 to April 2008'. The competition focused on a graphical summary of the important features of the dataset and it provided a list of questions - possible approaches, but it left the definition vague so that teams would be free to try different approaches.

For our purposes here we define the question in this way: Can we predict flight delays? There is still ample space to try out different approaches. This question, could be coming from a start-up that wants to create a site/application, that could inform passengers on the possibility of their flight being delayed. Or a Federal Agency, in the hope to gain a better understanding of the problem.

In our short project we have managed to gain a better understanding of the relevant data, and build a preliminary model that can predict, reasonably well, one type of delay. In specific we can predict whether a flight will be delayed due to a late arriving aircraft. Our predictions are 98 percent accurate when we predict there will be no delay, but significantly less accurate when we predict there will be a delay. This characteristic might be because of the narrow character of our model, focusing on only one type of delay, and therefore we could view the result with a certain optimism; it will get better once we create a fuller model.

In our report we will follow the various phases of our project and we will briefly describe it in the following sections:

1. The data sources and our chosen architecture for it
2. Our first analysis and summary of the data
3. The modelling – features, model, results

For each section there is the equivalent Jupyter Notebook where one can thoroughly inspect the codebase of the project 


## Getting and storing the data

The data we are being handed over cover the range from 1987 to 2008. We chose to focus on a single year. We will capture all the seasonality that appears to be yearly, without complicating things too much.

We have downloaded four csv files. The largest file contains the flights for 2008 while the other three contain information on the airports, the planes, and the carriers. The last three are small in size with a couple of thousand of observations each. The flights file is more than 600MB uncompressed. Bear in mind that this is a single year, and we have 21 years of data. 

The flights file alone fits in RAM and could be used as it is. But it already becomes cumbersome to juggle through all the csv files, in case we could like to use pieces of information from the other ones. Besides, once we will try to get more data we will most probably run into memory issues.

The solution is to store the data in a database. We should use a relational database for a couple of reasons. They are more widespread and well documented with a lot of supportive material. The organisers of the competition have made the data available in a form that can immediately be used with such a system.
The specific DB system that we will use is SQLite. It is powerful enough for our purposes, while less complicated than other similar systems. 

For the specific details with respect the structure of the database, and the ways the data is modelled, please take a look at the two files with the details on the database (its documentation), as well as the one with the script to create the database.

This is the list of the variables in the flights csv – with which we will spend most of our time analysing:

1. 	Year 	1987-2008
2. 	Month 	1-12
3. 	DayofMonth 	1-31
4. 	DayOfWeek 	1 (Monday) - 7 (Sunday)
5. 	DepTime 	actual departure time (local, hhmm)
6. 	CRSDepTime 	scheduled departure time (local, hhmm)
7. 	ArrTime 	actual arrival time (local, hhmm)
8. 	CRSArrTime 	scheduled arrival time (local, hhmm)
9. 	UniqueCarrier 	unique carrier code
10. 	FlightNum 	flight number
11. 	TailNum 	plane tail number
12. 	ActualElapsedTime 	in minutes
13. 	CRSElapsedTime 	in minutes
14. 	AirTime 	in minutes
15. 	ArrDelay 	arrival delay, in minutes
16. 	DepDelay 	departure delay, in minutes
17. 	Origin 	origin IATA airport code
18. 	Dest 	destination IATA airport code
19. 	Distance 	in miles
20. 	TaxiIn 	taxi in time, in minutes
21. 	TaxiOut 	taxi out time in minutes
22. 	Cancelled 	was the flight cancelled?
23. 	CancellationCode 	reason for cancellation (A=carrier, B=weather, C=NAS, D=security)
24. 	Diverted 	1 = yes, 0 = no
25. 	CarrierDelay 	in minutes
26. 	WeatherDelay 	in minutes
27. 	NASDelay 	in minutes
28. 	SecurityDelay 	in minutes
29. 	LateAircraftDelay 	in minutes



Let us now pay some attention to the database we have set up.


There are four tables that correspond to the four kinds of csv files that we are given. One each for the flights, the carriers, the airports, and the planes.



The three tables, apart from flights, have immediate candidates for their primary keys. The flights table is a bit more complicated. No single column can be used to uniquely identify rows. We have created a rather long key, that we expect will provide uniqueness, even if we add more data.


The flights table is the one that is not in the 3rd normal form. Some of the non key columns have dependencies among them - origin, destination, carrier, flight number follow certain patterns. We choose though not to break down the table any further, since it will be used mostly for reading operations. Adding more tables would slow things down through the necessary joins, but will not make a difference on the validity of the data returned.


There are four automatically created auto-indexes, each for every table along the primary keys. For the flights table, that contains the vast majority of the observations we have added more indexes.


By building our database we have a source that is ready to be queried, we have a way to make permanent changes to the data, and we can add more data in the future if we wish to so. All in all, we are ready to proceed with our next steps.


## First insights in the data

We focus on the flights since this will be our main focus. In the Jupyter Notebook one can find the coding details for the discussion below.

Since we try to understand data, let us put them together in conceptual groups. This will help us to see the relations between the various columns.
First come the four columns that capture the date. 'FlightYear', 'FlightMonth', 'FlightDay', 'DayOfWeek' - this last encodes week days. 
Then come those that identify the infrastructure and the specific flights, namely 'UniqueCarrier', 'FlightNum', 'TailNum', 'Origin', 'Dest', 'Distance'. These are at the heart of the analysis and the identification of flights into many different groups, across airports, carriers, etc.
Then come the columns that capture time aspects of a flight in the various stages it goes through - from planning to the final arrival. There are two main distinctions: Departure vs Arrival, and planned(CRS) vs actual.   'DepTime', 'CRSDepTime', 'ArrTime', 'CRSArrTime', 'ActualElapsedTime', 'CRSElapsedTime', 'AirTime', 'ArrDelay', 'DepDelay',  'TaxiIn', 'TaxiOut'. All these go finally down to ArrDelay, that captures the arrival delays - which is out main interest here.
 The analysis of the delays  goes even further through the five columns 'CarrierDelay', 'WeatherDelay', 'NASDelay', 'SecurityDelay', 'LateAircraftDelay'. These break down the over all delay into the various categories.
Finally there are the columns that specifically deal with Cancelled and Diverted flights,  'Cancelled', 'CancellationCode', 'Diverted'.


####The rules data follows

The group that captures time exhibits specific relation between the columns that we should further scrutinise. These relations start with logical relations between the different stages of a flight.
The planned flight time, in minutes, is the difference between  the planned arrival and departure times.

(1) CRSActualElapsedTime = CRSArrTime – CRSDepTime

There is of course the actual counterpart, where the actual flight time, in minutes, is the difference between arrival and departure times

(2) ActualElapsedTime = ArrTime – DepTime

Delays are then defined as the difference between the planned and the actual 
times, both for departure and arrival

(3) DepDelay = DepTime - CRSDepTime 

(4) ArrDelay = ArrTime – CRSArrTime

Some of the above is being further broken down. Actual elapsed time, from the moment the plane leaves the gate to the moment it arrives at the gate, is being broken down as: 

(5) ActualElapsedTime = TaxiOut + AirTime + TaxiIn

while arrival delay is being broken down in five parts:

(6) ArrDelay = CarrierDelay + WeatherDelay + NASDelay + SecurityDelay + LateAircraftDelay

These are the obvious relation, yet there is a derived relation that plays a really important role in the flights table. By combining 1,2,3, and 4 we derive a non obvious 7th relation that not only holds mathematically, but also holds for all the rows in the flights table, with the exception of Diverted and Cancelled flights that do not have all the fields.

(7) (ArrDelay - DepDelay) = (ActualElapsedTime - CRSElapsedTime )

We should stress this point: all rows, with the mentioned exceptions, do follow the above formula. Note that this relation connects all the time related fields in the table and somehow provides an integrity check for each individual row; it is being applied to every row, over the whole table. 



####Data quality and cleaning

In general the dataset we work with is well curated. For almost all the columns, there are no missing values – only non applicable. For the columns that we could check, the values also seem meaningful. For example, for all Origin Destination pairs, the distance between them has been the same for all flights, or the dates do take valid values. In most cases we have found values that seem unrealistic, there might be good explanations. Let us see in more detail.

####Strange rows, with plausible explanations

When we first examine a column we check for empty values and the range these values have. It is not always trivial to decide whether an extreme value we observe in a column is valid or not. There are statistical tests to test for outliers, but in many cases things are more subtle.
Take for example ArrTime, that captures the time the plane is in the air. It ranges from 0 all the way to 1350 minutes (Month:5 Day:24 Carrier:HA Flight: 21 Plane:N580HA) or almost a whole day. Obviously a plane in a domestic flight that usually lasts a bit more than a couple of hours, could not have stayed than long in the air. Now imagine the plane had to make a forced landing for some reason, and stay grounded, before finally make it to the final destination. This does not count as a diverted flight, nor as a canceled one. There is no way to encode the information in an other way, apart from setting the delay to an impossible 1034 minutes and adjusting all the fields so that integrity is maintained, but getting the AirTime to 1350. Therefore we have an impossible value, which is still meaningful from the point of view of the integrity of the data, as they are maintained by the data owner.





#### Data description findings

Our findings replicate these of the literature and the presentations of the ASA competition. 
The variation of flights and delays along certain dimensions – yearly, weekly, with respect the Origin, or the Carrier - follow the patterns reported in the literature[^2].
[^2]: *These can be found collected as the input of phase1*

The data report contains a detailed list of these findings which can be traced in the corresponding Jupyter Notebooks.




## The modelling
In this section we will talk about the way we set up and evaluated the first preliminary model, in our effort to provide an answer to the question of what determines flight delays. Our approach is to divide the overall problem into smaller parts and try to solve the easier parts first. We will focus on one kind of delay, the LateAircraftDelay, for reasons we explain below. In specific we have framed the model in terms of a classification problem; we will try to predict whether LateAircraftDelay will be positive or not.

#### The main idea: some observations
There is an effect we have seen mentioned in the sources we have found, but also in the data we have analysed. This effect is the delay propagation.

>Delay propagation occurs when a delay at a flight stage causes a ripple effect in the subsequent stages of a flight. Delays propagate into and out of an airport. Arrival delays are tracked at the end of each flight leg traveled by the same aircraft identified by a tail number[^3].
[^3]: [Federal Aviation Administration: Delay Propagation](https://aspmhelp.faa.gov/index.php/Delay_Propagation#FAQ "Delay Propagation")

The main observation is that flights use planes. By switching the focus to planes we view flights as stops in the itinerary of a plane. Then a delay in one leg, might be propagated along the rest of the flights. This shift in focus will allow us to represent our data in a different way.

####the conceptual model 

At the beginning of the day a plane has a list of destinations that will fly to, and the schedule that should be followed. Departing from point A, arriving at point B, going through disembarkation and embarkation processes, and then departing for destination C (might be same as A in case of return flight). This is the schedule. From the point of view of destination C, we look back  to  B and we try to gauge whether there will be a delay, arriving at final destination C.



####the features that capture the concepts

We use certain features in order to capture the above concepts.

LateAircraftDelay - it is the target we want to explain. It is the what is reported for each flight

time_btwn_Arrivals - this does not appear directly in the final dataset, but participates in the computation of two other features. It is the time planned by the airline from the arrival at airport B, all the way to arriving at airport C. 

previous_ArrDelay_percent - this is the arrival delay at the previous destination, in our case destination B. 

avg_flight_time_percent - here we get to other end of time_btwn_Arrivals. The avg_flight_time measures the usual time a flight takes from point B to point C.  

utilisation_percent - this is metric of how busy airports are. it is the division of the daily flights to and from a specific airport for a given day over the maximum observed flights at this airport. 


####the modelling technique

As we have decided to set up a classification task, it is time to decide on the kind of the model to use. Our choice comes from the Decision Tree family of models. 
These models are simple to understand, they can handle different types of data, without the need for extensive data preparation, and  they can handle large datasets, among other advantages.
Their main two disadvantages are their sensitivity to data variations, since a small difference in the data, can lead to widely different tress, while unbounded trees might "learn the noise", and thus exhibit a low in sample error, but much greater out of sample error.
The solution for these two problems is to grow multiple uncorrelated trees, and combine their predictions into a single one. One of the algorithms that does so
is the Random Forest Classifier.


####Model estimation and results
In the python ecosystem, the scikit-learn library implements Decision Trees, and Random Forests,  using a version of the CART (Classification and Regression Trees) algorithm. 
We have run a grid search, using some combinations parameter values for the algorithm. We have not performed an exhaustive search and we got the best parameter set to use with the algorithm.

Let us not take a look at the results.

The Random Forest Classifier has a feature importance metric that captures how much a feature has helped decrease the impurity of the classification. For our model the previous Arrival delay, is the single most important feature with about 75 percent of the importance. The airport utilisation is almost 0, while the rest 25 goes to the average flight time.

Yet, how good the results are? We have to be careful since we have a model with strongly imbalanced classes. The LateAircraftDelay is True in around 10 percent of the flights, therefore even a random guess that a flight will not be delayed due to this reason would be correct in 90 percent of the cases. Therefore we report the confusion matrix of the model along with a confusion matrix for a random guess. The matrix splits our test data into four compartments, which are, clockwise, predicted and true negative - A, predictive positive and true negative -B, predicted and true positive -C , and finally predicted negative and true positive -D. We also provide the classification report that computes certain statistics out the confusion matrix. Let us see in greater detail.

Is our model any good? Yes it is. Compared to the random guess, the model has higher True Negatives and  True Positives (A and  C), while at the same time lower False Negatives and False Positives (D and B). Therefore we now we have captured some of the true processes with our model. Note that the proportional reduction in the False Negatives (D) was much larger than the reduction in the False Positives (B). There might be a good reason for that. Recall that LateAircraftDealy is only one of the delay causes. It is probable, that when an airplane is late for the previous destination and wouldn't make it on time for the current one - and therefore our model predicts that LateAircraftDelay will be greater than 0 - still get a LateAircraftDelay equal to zero, if another delay cause steps in. For example, because of bad weather that aircraft is not allowed to take off from the previous destination. In that case LateAircraftDelay will be zero, and WeatherDelay will be positive.

In summary, we can say we have a good result. With a simple, preliminary model, we have captured part of the delay causes, and there is evidence our models can improve.


## Conclusions and next steps

We have started out with the desire to be able to predict aircraft delays. Our path took us into learning new things about the data itself and the way it is modelled, and we verified the previous results about delays found in the literature. 

With the observation that delays tend to propagate, we switch the focus from the individual flights to planes and their itineraries. In this way we managed to set up an train a model that is quite good in predicting when there will be no delay due a late aircraft, while it is not that accurate when predicting a delay. Still, it is much better than a random guess. This is good enough result for our first iteration of the project.


####Next steps
What should we then do next? Well, there are four different dimensions that we work in. Starting with the last part we worked with we identify what could we do next:

1 - we could spend more time on the model and re-examine the choices we made at that level. For example, in the decision tree family, there are other models available - see the AdaBoost, etc.  We mights have reasons to believe that a different algorithm could perform better.

2 - we could improve the quality of the features trying to reduce noise, spot outliers, etc. During the clean – summarise - validate phase of our project, we have spotted some anomalies with the data. At first we have not intervened because we could see that some times seemingly erroneous data was simply codifying information that could not have been recorded otherwise. We could revisit these cases and make choices and possibly find others too. What is for sure is that by spending time on feature quality we could improve the classification results.

3 - by taking a step even further, we could re-think the metrics we have constructed in our effort to capture the concepts in our initial model. For example, we have not included as a separate feature, that actual time a plane has to spent for the boarding procedures from the time it lands to the previous effort, to the time it becomes ready to depart again. In view also of the low importance of the airport utilisation, it could be more profitable to pay more attention to these processes 

4 - finally, we could go all the way back to our initial model and change it - slightly or completely. In any case, since we have concentrated on part of the delay causes, we will eventually get there. For example, we could change focus from planes to flights and try guess the connections flights have. Airlines frequently sell flight routes that have multiple legs, and get passengers and their luggage from one plane to another. Delays in one flight, will create delays in another, but these will, most probably, show up as CarrierDelay. 
There are two ways to approach the matter. Either we keep the model we have and try to make to incorporate new aspects - and features, or we can explore an orthogonal direction and start anew, hoping that we will merge the different concepts at a later stage.

The decision for the next steps has of-course to be taken along the rest of the stakeholders.

### Appendix


#### The software used and the corresponding versions:

- conda 4.6.11
- Python 3.7.3
- sqlite3 3.27.2
- numpy 1.16.2
- pandas 0.24.2
- matplotlib 3.0.3
- seaborn 0.9.0
- scikit-learn 0.20.3


#### Content list for the project

phase1 

output:

- intro to the project - intial question and motivation
- a report on the possible data to be used
- list of material with information on the subject matter of the airline industry and delays

phase2

input:

- the raw data
 
output:

- the database populated with the raw data
- the documantation for the database
- the script for creating the database
- the overall report for that phase
- the Jupyter Notebook with the all the relevant code

phase3

input:

- the database itself

output:

- the detailed data report
- the Jupyter Notebook with the all the relevant code

phase4

input:

- the database itself

output:

- the data for the model building
- the trained model
- the grid search results ( the results for mulitple trained models and the best parameters)
- the modelling report
- two Jupyter Notebooks one with the model preparation and another with model training

phase5

input:

- in a sense, all the above

output:

- this very project report for iteration 1


