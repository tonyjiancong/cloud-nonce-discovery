import argparse
import hashlib
import string
import sys
import datetime
import random
# import boto3


parser = argparse.ArgumentParser(description='Proof of ork')
parser.add_argument('-d', '--difficulty', type=int, required=True)
parser.add_argument('-i', '--index', type=int, required=True)
parser.add_argument('-n', '--number', type=int, required=True)


blockData = "COMSM0010cloud"

# s3 = boto3.resource("s3")


def getBlockAndNonce(inputBlock, nonce):
    return inputBlock+str(nonce)


def getSHA256(blockAndNonce):
    return hashlib.sha256(blockAndNonce.encode('ascii')).hexdigest()


def main(args):
    
    startTime = datetime.datetime.now()

    nonceRange = 4294967296

    startValue = args.index * int((nonceRange/args.number))
    endValue = (args.index+1) * int((nonceRange/args.number))

    inputBlock = blockData

    for nonce in range(startValue, endValue):
        # print(nonce)
        blockAndNonce = str(getBlockAndNonce(inputBlock, nonce))
        # SHA256 twice
        hashValue = getSHA256(getSHA256(blockAndNonce))
        hashValueInBits = bin(int(hashValue, 16))[2:].zfill(256)
        if hashValueInBits[0:args.difficulty] == '0'*args.difficulty:
            endTime = datetime.datetime.now()
            print("\n-------- Below From The Cloud --------")
            print("My name is instance No.{}, and I found the golden nonce!".format(args.index))
            print("Block Data: ", inputBlock)
            print("Golden Nonce Found: ", nonce)
            print("Block Data And Nonce:", blockAndNonce)
            print("Hash Value in Hex: ", hashValue)
            print("Hash Value in Bits: ", hashValueInBits)
            print("Compute Time: ", endTime-startTime)
            print("-------- Above From The Cloud --------")
            exit()
    exit()


if __name__ == '__main__':
    main(parser.parse_args())