# Nordic Tweet
** by Josh Embury**

### Overview
This program is used to obtain real-time grooming conditions from the web and to post this information on Twitter.
Project is hosted on AWS with EC2.
View the automated Twitter posts at https://twitter.com/MeissnerNordic

### Motivation
As an avid cross-country skier, it is imperative to understand the latest grooming conditions at the local Nordic center.
This information helps to inform what time the trails will be ready to ski, what to expect for snow quality, and what wax to use.
In order to avoid having to go to a website to check whether trails have been groomed, this Python script has been created to scrape
the latest data from the Nordic center's website, and to post this information to Twitter.
<br>
This program is designed to obtain data for a specific Nordic center, but can easily be modified to scrape data for cross-country
 trails in a different location.

### Features
<ul>
    <li>Web scraping data using BeautifulSoup4</li>
    <li>Build in Python using Tweepy library</li>
    <li>Automated tweets via the Twitter API</li>
    <li>Deployed on the cloud</li>
    <li>Hosted on AWS EC2</li>
</ul>
