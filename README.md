# submit-to-th
 Note - If you want to understand Treeherder and how to install it locally, please read these docs -
 https://wiki.mozilla.org/EngineeringProductivity/Projects/Treeherder
 http://treeherder.readthedocs.org/installation.html

 This folder contains python code that can help you submit data to Treeherder in two ways -
 1) Submit the results of a test script run locally on your Linux/Mac to an instance of Treeherder. (The instance can be locally running using Vagrant/Treeherder.)
 2) Submit Jenkins results to an instance of Treeherder.
 
 python submission.py --repository=mozilla-inbound --test-type=functional --revision [FILL] --treeherder-url=http://local.treeherder.mozilla.org/ --treeherder-client-id=[FILL] --treeherder-secret=[FILL] --build-state=running x 
 In order for the above command to work, you would need to provide-
 1) a valid repository found on treeherder.
 2) a revision which has already been ingested(see docs) by Treeherder.
 3) Correct treeherder url/credentials
 4) correct config.py details 
 5) a retval.txt file should be generated through a testscript/Jenkins runs. (This file just contains a 0 or 1)
 6) Logs need to be saved as log_info.txt
 The treeherder client id and secret will be recreated everytime you attempt a vagrant destroy and vagrant up.
 The testscript creates a file called retval.txt which contains a 1 or 0 to indicate Fail/Pass. Any tests that hope to utilize these submission scripts will also need to create the retval.txt file and save the result of their job run. For ex: If 100 tests have run and 1 has failed, the test script should create a job result of 1 indicating the failure and save only that integer in retval.txt as a string(see test script for an example), and the log file can be passed into Treeherder using the S3 servers. 


