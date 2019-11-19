# News Tracker

## Concept
An application that allows a user to keep track of current events by saving news articles fetched from the NEWS API. The app will allow the user to go back to topics after the news cycle has moved on.

## User Stories
A user should be able to log in and see an option to create a current event topic to follow. 

Once the topic is created, the user should be able to search the News Api based on query strings such as keywords in title, in body, and date of publication.

A user should be able to select articles they find relevant and have that article stored in that topic's data table.

A user should be able to search the same topic over again to find updated articles. 

A user should be able to add their own notes to each topic.

A user should be able to update their topic collections by adding and removing content.

A user should be able to remove topics.

## Database structure
Many Users
     User >> many Topics -- each topic has user Id
                  Topic >> many articles -- each Article has Topic Id
                                Articles will come from News API

## Stretch Goals
Pull in other apis like price of comodities if topic is related.

Make it look pretty.

Authentication.

JSON Web Tokens