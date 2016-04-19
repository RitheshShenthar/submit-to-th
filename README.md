# submit-to-th

##Introduction
[Treeherder](https://treeherder.mozilla.org) is a reporting dashboard for that allows users to see the results of automatic or manual builds from Mozilla checkins and their respective tests. <br>

The purpose of this tool is to enable the submission of a generic job run result from a machine(local PC/Mac/Jenkins machine) to an instance of Treeherder. This project contains set of scripts that can be customized or extended as per the needs of your implementation. 

There are essentially three kinds of instances of Treeherder to which you can submit data -<br>
1. Local (http://local.treeherder.mozilla.org) - This is when you download or fork the treeherder repository and start an instance on your PC/Mac/local machine. This is usually done to set up a local sandbox for testing purposes.<br>
2. Staging (https://treeherder.allizom.org) - This is a publicly available continuously running server maintained by the treeherder team which is used for pre-deployment tests. <br>
3. Production (https://treeherder.mozilla.org) - This is the publicly available production instance of treeherder against which you can only submit pre-tested legitimate test run results. <br>


##Requirements
It is assumed that you already have a MacOS or Linux development environment setup (Tool was developed on Mac OS X Yosemite). Posting to treeherder can be done via a treeherder python client or a node.js client; this tool only uses the python client. It is assumed that your development environment already has python 2.7.9+ already installed (2.7.9+ is required for authentication).

If you are planning on submitting data to a local instance(a must if you are testing) [Virtual Box] (https://www.virtualbox.org/)and [Vagrant](https://www.vagrantup.com/) are also required for the development environment. If you don’t have them installed, please refer to the hyperlinks on how to install them.

Note - If your submissions need to be done from a Jenkins machine, it will need the treeherder client module. Install this using ```pip install treeherder-client```. If you are installing the complete Treeherder package anyways to run a local instance, then treeherder-client gets installed as a part of it.


##Quickstart
The below steps will create a local instance of Treeherder, run a sample test script and log the result using the submission script. <br>
1. git clone https://github.com/RitheshShenthar/submit-to-th.git<br>
2. [Install](http://treeherder.readthedocs.org/installation.html) local instance of Treeherder. Verify that http://local.treeherder.mozilla.org/ is up and running and it that is ingesting pulse data i.e Treeherder is acquiring information about Mozilla checkins with revision ids.<br>
3. Create Hawk credentials using the following commands (after starting Treeherder as in Step (2) 

	~/treeherder$ vagrant ssh
	vagrant ~/treeherder $ ./manage.py create_credentials test-client-id treeherder@mozilla.com "Description"

4.Find a valid revision id against which we can submit a test result. To do this, look for a revision id that is already ingested in your local treeherder under repo "mozilla-inbound". (Since the default repo in our project is mozilla-inbound). eg:- f5f9a967030d

5.Under the submit-to-th folder, run the below command provided with =><br>
1) valid revision id for repository "mozilla-inbound" using ```--revision```. <br>
2) valid secret key obtained as output in step (3)


	./submission.py --repository=mozilla-inbound --test-type=functional --revision [FILL] --treeherder-url=http://local.treeherder.mozilla.org/ --treeherder-client-id=test-client-id --treeherder-secret=[FILL] --build-state=running treeherder_venv
	

6.Under the submit-to-th folder, run ```./testscript```<br>
7.Run the same command as in step (6) except with ```--build-state=completed```
8.Navigate to Treeherder UI and verify that result was logged. (Ensure that the correct Tier is selected as necessary in the dropdown.)

##Using the tool

Treeherder provides a library, called ```treeherder-client```, to support data submission to a treeherder service instance. The submit-to-th project internally uses this module to execute submissions.
Before you can submit data to treeherder, you will need at least this much information-<br>
1. Hawk credentials - You will need to [acquire API credentials](https://treeherder.readthedocs.org/common_tasks.html#managing-api-credentials) in order to authenticate your submissions. <br><b>Note-</b><br> For local instances, you can use the command in the link only once Treeherder instance is up. Also you will need to recreate the credentials every time you destroy and recreate the local instance.<br>
2. repository - you will need to know which repository you want to log results against.<br>
3. revision - you will need to know which revision of the above repository you want to log results against.<br>
 
 This tool can be customized to submit the results of any kind of job and any kind of repository. It contains python code that can help you submit data to Treeherder in two scenarios - 
 
 1) With S3 Logging.(Assuming S3 bucket is available for logging.)<br>
 ```./submit-to-th.py --repository=[mozilla-inbound] --test-type=[functional] --revision [FILL] --treeherder-url=[http://local.treeherder.mozilla.org/] --treeherder-client-id=[FILL] --treeherder-secret=[FILL] --build-state={running|completed}   treeherder_venv
```
The following os environment variables need to be set for this option or passed in through CLI-

	AWS_BUCKET                      
	AWS_ACCESS_KEY_ID
	AWS_SECRET_ACCESS_KEY
 2) Without S3 Logging.
 ```./submission.py --repository=[mozilla-inbound] --test-type=[functional] --revision [FILL] --treeherder-url=[http://local.treeherder.mozilla.org/] --treeherder-client-id=[FILL] --treeherder-secret=[FILL] --build-state={running|completed}   treeherder_venv
```


<b>Step 1</b><br>

Settings to create an initial submission before job is run -<br>
1. Script commandline params need to be modified as per your project- eg:-submission.py --repository=xxxx<br>
2. config.py - Settings in the config.py need to be modified to suit your project and job. See config.py for details<br>
3. We can add os environment variables with the below names or optionally pass them in the commandline. 

	TREEHERDER_CLIENT_ID
	TREEHERDER_URL
	TREEHERDER_SECRET
	AWS_BUCKET                      
	AWS_ACCESS_KEY_ID
	AWS_SECRET_ACCESS_KEY
The AWS variables are valid only with the submit-to-th.py file and not with submission.py. The 2 files are the same for the most part, with the difference that submission.py is meant for running on local sandboxes and submit-to-th.py is meant for running on Jenkins enabled machines with S3 credentials available.<br>
4. Set ```--build-state=running``` in the CLI command.

<b>Step 2</b><br>

Whatever job/test suite needs to be run, is run.(eg:-```testscript``` in our case)<br>
The criteria for writing compatible test jobs are-<br>
1. The job needs to create a simple file called ```retval.txt``` and store a "0" (on PASS) or "1" (on FAIL) in it and <b>nothing else</b>.  <br>Eg:- If a job has 100 tests and 1 has failed, the job should create a file ```retval.txt``` and in it store a job result of "1" indicating the failure and save only that integer in the file as a string(see ```testscript``` for reference)<br>
2. All logging needs to be done into a file called ```log_info.txt```.<br>
3. Both files need to be stored in the same folder/workspace as the submit-to-th. This is to enable visibility during Step 3.<br>

<b>Step 3</b><br>

Run the script commandline ./submission.py or ./submit-to-th with ```--build-state=completed``` in the CLI command.

<b> Step 4</b><br>

Verify that results are popping up on treeherder. Ensure correct Tier is checked in the Dropdown.

#Note:
If you want to further understand Treeherder and how to install it locally, please read these docs -<br>
 https://wiki.mozilla.org/EngineeringProductivity/Projects/Treeherder<br>
 http://treeherder.readthedocs.org/installation.html<br>
 Want to learn more or have any specific questions? Chat on IRC:#treeherder<br>
 
 
  






