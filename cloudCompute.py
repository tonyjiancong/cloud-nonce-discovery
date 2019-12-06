import boto3
import paramiko
import sys
import time
import datetime
import threading
import signal
import logging

ec2 = boto3.client('ec2', region_name='us-east-1')

# command line inputs
if len(sys.argv) != 1:
    print("Please do not add any arguments")
    exit()

def getNumberOfInstances(difficultyLevel, timeDesired):

    correlationConstant = 0.56

    numberOfInstances = int(round(difficultyLevel / (timeDesired * correlationConstant)))

    if (numberOfInstances > 30):
        print("Number of instances exceeded limit, set to 30.")
        numberOfInstances = 30
    elif (numberOfInstances < 1):
        numberOfInstances = 1

    return numberOfInstances

option = input("Enter the number of option: 1 Direct | 2 Indirect: ")

if option == '1':
    numberOfVMs = int(input("Enter number of instances: "))
    if (numberOfVMs > 30):
        print("Number of instances exceeded limit, set to 30.")
        numberOfVMs = 30
    elif (numberOfVMs < 1):
        numberOfVMs = 1
    difficultyLevel = int(input("Enter number of leading zeros bits: "))
    timeLimit = int(input("Enter time limit in seconds: "))
elif option == '2':
    difficultyLevel = int(input("Enter number of leading zeros bits: "))
    timeLimit = int(input("Enter time limit in seconds: "))
    timeDesired = int(input("Enter desired running time in minutes: "))
    numberOfVMs = getNumberOfInstances(difficultyLevel, timeDesired)
    print("According to the algorithm, {} instances is the best option. ".format(numberOfVMs))
else:
    print("Please enter 1 or 2")
    exit()

# def putInBucket():
#     try:
#         response = s3.Object("cloudcomputing29321", "proofOfWork.py").put(Body=open("proofOfWork.py", 'rb'))
#     except Exception as error:
#         print (error)

def createInstances():
    try:
        response = ec2.run_instances(
            ImageId='ami-04b9e92b5572fa0d1',
            MinCount=1,
            MaxCount=numberOfVMs,
            InstanceType='t2.micro',
            KeyName='mykey',
            # UserData = userData,
            SecurityGroupIds=['sg-09ddb818a01b0e36d']
        )
    except ClientError as e :
        logging.error(e)
        return None
    instances = response['Instances']
    instanceIds = list(map(lambda x: x['InstanceId'], instances))
    return instanceIds


def terminateInstances(instanceIds):
    try:
        ec2.terminate_instances(InstanceIds=instanceIds)
    except ClientError as e :
        logging.error(e)
        return None

def getRunningInstances(instanceIds):
    try:
        time.sleep(30)
        while 1:
            response = ec2.describe_instances(InstanceIds=[instanceIds])
            instance = response['Reservations'][0]['Instances'][0]
            if instance['State']['Name'] == 'running':
                time.sleep(30)
                return instance
            else:
                time.sleep(10)
    except ClientError as e :
        logging.error(e)
        return None

def timeout_handler(signum, frame):
    if signum or frame:
            pass
    print("### Time Has Exceeded {} Seconds, All Instances Terminated. ###".format(timeLimit))
    exit()


def distributedCloudCompute(computeParameters):
    # input
    index, difficulty, max_instances, instance_id = computeParameters
    instance = getRunningInstances(instance_id)
    print('Instance No.', index, 'is now running with ID:', instance_id)
    # ssh
    ssh = paramiko.SSHClient()
    key = paramiko.RSAKey.from_private_key_file('/Users/tony/Downloads/mykey.pem')
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=instance['PublicIpAddress'], username='ubuntu', pkey=key)

    sftp = ssh.open_sftp()
    sftp.put('proofOfWork.py', 'proofOfWork.py')

    commandString = "python3 proofOfWork.py -d " + str(difficulty) + " -i " + str(index) + " -n " + str(max_instances)

    stdin, stdout, stderr = ssh.exec_command(commandString)
    outlines = stdout.readlines()
    errlines = stderr.readlines()
    for line in outlines:
        print(line)
    for line in errlines:
        print(line)

    ssh.close()
    return


def main():
    print("########## CND Started ##########")
    print("Launching {} instances...".format(numberOfVMs))
    print("Difficulty level is set to {} leading zero bits".format(difficultyLevel))
    print("Time limit is set to {} seconds".format(timeLimit))
    startTime = datetime.datetime.now()
    original_handler = signal.signal(signal.SIGALRM, timeout_handler)
    # putInBucket()
    instanceList = createInstances()
    computeParameters = [(instanceList.index(instanceIds), difficultyLevel, 
        len(instanceList), instanceIds) for instanceIds in instanceList]
    try: 
        signal.alarm(timeLimit)
        threads = []
        for i in range(numberOfVMs):
            t = threading.Thread(target=distributedCloudCompute, args=(computeParameters[i],))
            threads.append(t)
            t.setDaemon(True)
            t.start()

        flag = 1
        while flag == 1:
            time.sleep(1)
            for t in threads:
                if not t.isAlive():
                    flag = 0
                    break

        terminateInstances(instanceList)
        endTime = datetime.datetime.now()
        print('Total Time: ', endTime - startTime)
        print('########## CND Finished ##########')
        exit()

    except KeyboardInterrupt:
        terminateInstances(instanceList)
        print("\n### Emergencey Stop and All Instances Terminated. ###")
        exit()

    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, original_handler)
        terminateInstances(instanceList)



if __name__ == '__main__':
    main()