# Cloud Nonce Discovery System 
This is the source code of the developed Cloud Nonce Discovery System that uses horizontal scaling on Amazon Web Services for an embarrassingly parallelisable Blockchain Proof-of-Work task. It is for the COMSM0010 Cloud Computing coursework (comsm0010_CW).   

## Dependencies Needed 
* Python 3 
* Boto3 
* awscli  

## Deployment Process 

1. Install all the dependencied listed above. 

2. Create a AWS account and place the credentials from account details into the `~/.aws/credentials`    
  ```shell    
  aws_access_key_id= Yourawsaccesskeyid    
  aws_secret_access_key= Yourawssecretaccesskey    
  ``` 

3. Create a new security group that enables SSH connection based on your current ip address and change the security group name within the `cloudCompute.py` script to your security group name:    
  ```shell    
  SecurityGroupIds= ['YourSecurityGroups']    
  ``` 
4. Create a key pair and store the secret key file somewhere safe on your local system, and change the key name when creating instances and key name path when creating SSH client within the `cloudCompute.py` script to your own private key name path:    
  ```shell    
  key = paramiko.RSAKey.from_private_key_file('PATH/YourKey.pem')    
  ``` 
5. Run the `$ python3 cloudCompute.py` command and enter the paramters prompted, an example is given below:     
  ```shell    
  $ python3 cloudCompute.py    
  Enter the number of option: 1 Direct | 2 Indirect: 1    
  Enter number of instances: 10    
  Enter number of leading zeros bits: 24    
  Enter time limit in seconds: 1200    
  ########## CND Started ##########    
  Launching 10 instances...    
  Difficulty level is set to 24 leading zero bits    
  Time limit is set to 1200 seconds    
  Instance No. 0 is now running with ID:...    
  ...    
  Instance No. 9 is now running with ID:...    
  -------- Below From The Cloud --------    
  My name is instance No.5, and I found the golden nonce!    
  Block Data:  COMSM0010cloud    
  Golden Nonce Found:  2149189591    
  Block Data And Nonce: COMSM0010cloud2149189591    
  Hash Value in Hex:  0000004313f4c2a25cee9839bb14b35785a2406d6414311b1902c81640aa4b58    
  Compute Time:  0:01:16.952668    
  -------- Above From The Cloud --------    
  Total Time:  0:02:31.234354    
  ########## CND Finished ##########    
  ``` 
