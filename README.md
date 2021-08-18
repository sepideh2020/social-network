# social_network
Before running the project please first install the required packages which are in req.txt  with the below command:

 pip install -r req.txt
For runnung the project run the commandas below:
 python manage.py migrate
 python manage.py makemigrations
 python manage.py runserver
In this project, a Social network website like Twitter and Instagram was developed. Each user can make an account for themselves (Each user's email or Phone will be their username based on their choice, which should be used for logging in). After Signing up, the user can choose whether the activation code is sent to their email or Phone number. 

Users can search among other users ( searching field is auto-complete), the released date of each post is shown in the database, and how long is passed from sharing date is shown next to each post ( one hour, one day and ...). The number of likes and comments is shown under each post, and also, users' friends can write comments under each post. Posts of each user can be seen in their profile. On the main page, posts of other users who are the user-friend are shown, and also user can see their friends on the main page and the number of their friends. Users can edit their posts and delete comments under their posts.  Each user can edit the information of their profile.

![Capture](https://user-images.githubusercontent.com/22345837/129878835-774fcfb7-0dd9-44de-b067-db43866100e5.PNG)











