## Data analysis of mobile health application usage.

This repository contains the code for my project.


###  Folder Description

#### scraping-code

This folder contains the code that I used to scrape mobile health related application data on appstore (for ios apps) and playstore (for android apps). 

For ios, the scraping was done alphabetically and by category (Medical and Health & Fitness categories). Appstore catalog the applications in alphabetical order as well as in categories. Selenium and Beautifulsoup python libraries were used to scrape this data.

For android apps, the application catalog on playstore is not easy to scrape all data so very few medical related apps are currently scraped on playstore. Due to time constraint for this project, the android application usage might not be analysed.

#### ios

This folder consists of the ios application data that was scraped based on category and the first alphabet of the application name.


#### android

This folder consists of the android application data scraped so far and categorised into fitness and medical.


##### jupyter

This folder consists of the code used for cleaning the dataset. It will consist of other code for feature engineering, visualization etc. The cleaned dataset has been saved into a file and can be found in this folder.


### Features extracted

The features extracted for ios are listed below:

- Application name
- Size
- Age rating
- Languages
- Price
- In App purchases
- Average Rating
- Total count of ratings
- Privacy data collected by the application
- Application link
- Number of versions
- Last Version Date
- First Version Date
- Application Type