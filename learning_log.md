# LEARNING LOG
This is a learning log for the project: todolist_app. It contains the notes for the programming skills I will be developing as I build this project, including the problems that I have come across, and how I resolved them.

## ⚠️ IMPORTANT NOTE ⚠️
I have used Artificial Intelligence (AI) to help me build this project, in following ways:
- To write boilerplate/repeated code, without making any design structure changes
- To help me understand the problems better, in-case I am unable to get a clear picture of it
- Help me draft solutions by recommendations, ask questions to it about the decisions I plan to make and review it

The main objective of this project is to learn how to integrate different systems efficiently, and to learn to build and learn with AI, and not about letting AI do all the work instead.

## NOTES:
### PROBLEM 1: Data communication problem [Date: Unknown]
**Problem**: The application needed to create and access seperate data directory for each authenticated user, and for that the user had to log in to the application interface. Firstly, I had to divide the interface responsibilites (one for the userlogin or registeration, and another one for todolist). The first issue was whenever the user was registering to the database, the data did not get stored, and the function did not log the error/failure to save the newly created data.

**Solution**: The method which was responsible to save the data expected a wrapper which would contain data along with the key for it, for example; {"data": TheActualData, ....}. But, the function was given the actual data instead. So, I changed that and then the method saved the data as intended.

**takeaway**: It is important to keep the design of functions and methods consistent with one another to have efficient data flow across the application.