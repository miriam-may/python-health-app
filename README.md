# Health App in Python - start as console, end with a gui?

I've created this little thing which started life as a console application. I am trying to write it also as a GUI application with PyQt6.

I tried writing this as a C# .NET WPF app, but writing for Windows can be a nightmare so I also thought I'd try it in Python for simplicity's sake. 

It uses SQLite 3 locally to store information.

Some icons by Yusuke Kamiyamane. Licensed under a Creative Commons Attribution 3.0 License.


## Features

- Accept a symptom name, rating, and any notes
- Store the symptom name rating, and notes on a local SQLite DB with two tables - parent table for the symptom name, child table for the ongoing ratings and notes
- Offer to show the user a list of their previously entered symptoms
- Cascading delete for the ratings and notes so that when a user chooses to delete a symptom by its name, all its corresponding data is deleted
- Check whether a symptom exists before adding (if so, only add to the child table) and deleting (if the symptom does not exist, inform the user and do not proceed)
- Ouput a .txt file with a brief history that the user can show their doctor (this is still in the very early stages)
- Calculate whether given symptoms are getting worse or not by comparing the averages of the first 50% of the symptom's recent ratings with the second 50%


## Planned Improvements - short term

- Make the output .txt file easier to read and "prettier"
- Rewrite as GUI instead of console app using PySimpleGUI for added user-friendliness   
- <b>(Changed my mind - now using PyQt6, not PySimpleGui)</b>
- Add extra error management for edge cases with SQL queries

## Planned Improvements - long term

- Possibly rewrite as web app for accessibility using Python web framework
- If so, add user authentication (strong password protected access) as health information is sensitive
- Possibly, instead of a .txt output, create a separate "doctor's dashboard" where the user can put info they want their health professional to see that is separate from their personal dashboard (to protect a user's privacy)