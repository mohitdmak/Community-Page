# Bits Community Page
A community page for bits, made to learn and implement the oauth2 api,
along with sqllite3 db and deploying via wsgi.

## Head here [link](https://mohitdmak.pythonanywhere.com/).

Login through your google acount, and complete your profile upon registration.
Upload your profile pic, and answer/ask your questions.

### To replicate:
1> Fork, Clone and create a virtual environment after installing from pip.
2> Ensure the python script version is above 3.8 with pip3
3> Install dependancies from req.txt.
4> The project will require a secret key for django and api keys for oauth2 for gmail verification.
5> Also a host email id and password needs to be validated to use for forwarding auto generated mails via smtp port.
6> Run tests for changes made. [ test.py under same dir as settings.py ]
7> Run on port 8000 of local machine by manage.py file.

#### Note:
Function-based views will probably be changed later as django v3 now supports asynchronous requests (not based on js) by using the 'async' method.
This will let users upvote/downvote and save posts without redirection.
