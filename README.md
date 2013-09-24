To use laboraty in the Loft
-------------------

- add the git repository to requirements
- run pip
- run syncdb to add the laboratory models
- add 'laboratory' to intalled apps
- include laboratory urls if you want the study editing tools
- add_to_builtins('quiz.templatetags.laboratory')  # for discourse tags to work

To use the study tags in you templates, see example/templates/home.html



To run the example example...
-------------------
Prerequisites for Mac OS:
Make sure you have the XCode development environment and the Development Command Line Tools.  They can be downloaded from https://developer.apple.com/downloads/index.action, you need Xcode 4.6 or higher, and "Command Line Tools" for your version of your OS.

Prerequisites for Linux:
Make sure you have python 2.6 or higher installed (it should be).  You can check by running "python" and looking at the first line.  Also make sure you have python-setuptools by seeing if the command "easy_install" is available.  If that command fails to run, try going to http://pypi.python.org/pypi/setuptools

Step 1:
Make sure you have pip and virtualenv installed by doing:

  > sudo easy_install pip virtualenv
  ...
  Finished processing dependencies for virtualenv

Step 2:
In the project root, create a python virtual environment named "env".

  > virtualenv env
  New python executable in env/bin/python
  Installing setuptools............done.
  Installing pip...............done.


Step 3:
Install the project requirements.  Make sure you see "Successfully installed ..." at the end.  Otherwise check troubleshooting, below.

  > env/bin/pip install -r requirements.txt
  ...
  Successfully installed Django
  Cleaning up...

Step 4:

  > ./manage.py syncdb
  Ceating tables ...
  ...
  Would you like to create one now? (yes/no):

It will ask you to create a user, go ahead and create one for yourself.  That user will only be local to *your* machine so don't expect it to be anywhere else.  If this fails, or you want to create a user later see "Creating An Admin User Via The Command Line", below.  Also, there is by default a user with email "admin@designforamerica.com" and password "pass".


Step 6:
  
  > ./manage.py runserver
  ...
  Development server is running at http://127.0.0.1:8000/
  Quit the server with CONTROL-C.

This will start up the server, running.  Visit http://127.0.0.1:8000/ in your browser now.
Changes you make should automatically up


Step 7:
If you load up the test fixtures, you can login with:
  user: admin
  pass: admin


Run tests
------
./manage.py test laboratory



Use Laboratory!
---------------
1. Create a study in the admin interface
2. Create some groups in the admin interface
3. Add tags to your page to show/hide content for different groups, (see example/templates/home.html for example, e.g.,:

  <p>Everyone in 'Study 1' should see this:</p> 
  {% study 'Study 1'  %}
      <p>Hi Study 1 participant!</p>
  {% endstudy %}
  
  <p>Everyone in 'Study 1,' 'Group A' should see this:</p>  
  {% study 'Study 1' 'Group A' %}
      <p>Hi Group A participant!</p>
  {% endstudy %}

  <p>Everyone in 'Study 1,' 'Group B' should see this:</p>
  {% study 'Study 1' 'Group B' %}
     <p>Hi Group B participant!</p>
  {% endstudy %}                

  <p>Everyone NOT in 'Study 1' should see this:</p>
  {% study 'Study 1' 'NA' %}
     <p>Hi person not in Study 1!</p>
  {% endstudy %}

  <p>This is what happens if you are logged in and the study doesn't exist:</p>
  {% study 'Study Foobar' %}
     <p>There will be an error message here</p>
  {% endstudy %}




