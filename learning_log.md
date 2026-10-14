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
**Problem**: Firstly, I had to divide the interface responsibilites (one for the userlogin or registeration, and another one for todolist). The first issue was whenever the user was registering to the database, the data did not get stored, and the function did not log the error/failure to save the newly created data.

**Solution**: The method which was responsible to save the data expected a wrapper which would contain data along with the key for it, for example; {"data": TheActualData, ....}. But, the function was given the actual data instead. So, I changed that and then the method saved the data as intended.

**takeaway**: It is important to keep the design of functions and methods consistent with one another to have efficient data flow across the application.

### PROBLEM 2: Creating user-specific data directory
**Problem**: The application had to create user-specific data directories which the application would access during the runtime of the application for the authenticated user. I struggled with creating the data manager object for the lists manager, as it needed the user to be authenticated first, as I was unable to understand where and how to initialise this data manager object.

**Solution**: I first tried to modify the variable which was supposed to hold the data manager object, but I had already imported it to the main, as it needed to be used for intialisation of the list_management class after authentication of the user. I consulted AI for suggestions/improvements, and it recommended me to replace the variable with a function that returns the data manager object after authentication of the user. After the user is authenticated, the function is called within the function that initialises list manager (loading the data to operate on/creating directory and datapaths), and the storage object can be used directly there.

**takeaway**: 
- Importing an object or variable from another module does not automatically create a new instance or dynamically update a previously imported reference when the original module reassigns that variable.
- Objects that depend on user authentication should be initialized only after the authenticated user is known. A function can create and return the appropriate data manager when needed, rather than relying on an object instantiated prematurely at module level.
- Using functions to initialize and return objects when required can make the application lifecycle easier to manage and prevent dependencies from being initialized before their required data is available.