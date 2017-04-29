import luigi
from luigi.contrib.s3 import S3Client
from luigi.contrib.s3 import S3Target
from luigi.contrib.s3 import S3PathTask
from luigi.local_target import LocalTarget
from luigi import configuration
import boto3
from botocore.client import Config
from botocore.exceptions import ClientError
import FinalProject_DataDownload
import os


class DownLoadEconomicIndicatorsTask(luigi.Task):
    awsaccesskeyid = luigi.Parameter()
    awssecretaccesskey = luigi.Parameter()
    bucketName = luigi.Parameter()


    def run(self):
        # Logic For Download Data goes here
        print('=========================')
        print('Downloading Federal Bank Of Richmond Dataset to Local')
        print('=========================')
        df = FinalProject_DataDownload.driver()
        self.fileHandle = open('output.txt', 'w')
        self.fileHandle.close()
        print('=========================')
        print('Completed Downloading Federal Bank Of Richmond Dataset to Local')
        print('=========================')
        for each_row in df:
            indicator_name, state_name, new_df = each_row
            self.fileToUpload = state_name + '_' + indicator_name + '.csv'
            self.uploadFileToS3()
        self.fileToUpload = 'output.txt'
        self.uploadFileToS3()

    def output(self):
        return S3TargetExists(self.awsaccesskeyid, self.awssecretaccesskey, self.bucketName, 'output.txt')

    def uploadFileToS3(self):
        client = boto3.client(
            's3',
            aws_access_key_id=self.awsaccesskeyid,
            aws_secret_access_key=self.awssecretaccesskey,
            config=Config(signature_version='s3v4')
        )
        if client:
            print('========================')
            print('Uploading Data Files to S3 bucket')
            print('========================')
            client.upload_file(self.fileToUpload, self.bucketName, self.fileToUpload)



class PredictAndForecast(luigi.Task):
    awsaccesskeyid = luigi.Parameter()
    awssecretaccesskey = luigi.Parameter()
    bucketName = luigi.Parameter()
    taskFilepath = luigi.Parameter('PredictAndForcast.txt')

    def requires(self):
        return [DownLoadEconomicIndicatorsTask(self.awsaccesskeyid, self.awssecretaccesskey,self.bucketName)]

    def run(self):
        # Logic For Predict And Forecast Data goes here
        print('=========================')
        print('Start Reading Files and Performing ARMA Models')
        print('=========================')
        df = FinalProject_DataDownload.ReadFileAndExecuteModels()
        pathToOutputFiles = './OutputFiles'
        os.chdir(pathToOutputFiles)
        self.fileHandle = open('predictOutput.txt', 'w')
        self.fileHandle.close()
        print('=========================')
        print('Completed Downloading Predictions And Forecast files to Local')
        print('=========================')
        
        for (dirname, dirs, files) in os.walk('.'):
            for file_ in files:
                self.fileToUpload = file_
                self.uploadFileToS3()
        self.fileToUpload = 'predictOutput.txt'
        self.uploadFileToS3()


    def output(self):
        return S3TargetExists(self.awsaccesskeyid, self.awssecretaccesskey, self.bucketName, 'predictOutput.txt')

    def uploadFileToS3(self):
        client = boto3.client(
            's3',
            aws_access_key_id=self.awsaccesskeyid,
            aws_secret_access_key=self.awssecretaccesskey,
            config=Config(signature_version='s3v4')
        )
        if client:
            print('========================')
            print('Uploading Data Files to S3 bucket')
            print('========================')
            client.upload_file(self.fileToUpload, self.bucketName, self.fileToUpload)    


        

class S3TargetExists(luigi.Target):

    def __init__(self, aws_access_key_id, aws_secret_access_key, bucketName, fileName):
        self.aws_secret_access_key = aws_secret_access_key
        self.aws_access_key_id = aws_access_key_id
        self.bucketName = bucketName
        self.fileName = fileName   


    def exists(self):
        client = CreateBotoClient(self.aws_access_key_id,self.aws_secret_access_key).createClient()
        if client:
            try:
                print('===========================')
                print('Checking if bucket exists')
                print('===========================')
                client.head_bucket(Bucket=self.bucketName)
                print('===========================')
                print('Bucket found!')
                print('===========================')
            except ClientError as e:
                if e.response['Error']['Code'] == '403':
                    print('=====================')
                    print('Failed to make connection to S3')
                    print('=====================')
                    return True
                elif e.response['Error']['Code'] == '404':
                    print('======================')
                    print('Bucket Not Found On S3. Exiting program')
                    print('======================')
                    return True
            try:
                client.head_object(Bucket=self.bucketName, Key=self.fileName)
                print('======================')
                print('File Already Exists On S3 Bucket')
                print('======================')
                return True
            except ClientError as e:
                print("Received error:", e)
                print(e.response['Error']['Code'])
                if e.response['Error']['Code'] == '403':
                    print('=====================')
                    print('Failed to make connection to S3')
                    print('=====================')
                    return True
                elif e.response['Error']['Code'] == '404':
                    print('======================')
                    print('File Not Found On S3 Bucket')
                    print('======================')
                    return False
        else:
            print('======================')
            print('Unable to make a connection to S3')
            print('======================')
            return True

class CreateBotoClient():
    def __init__(self,aws_access_key_id, aws_secret_access_key):
        self.aws_secret_access_key = aws_secret_access_key
        self.aws_access_key_id = aws_access_key_id
    def createClient(self):

        try:
            client = boto3.client(
                's3',
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key,
                config=Config(signature_version='s3v4')
            )
            return client
        except ClientError as e:
            print('=====================')
            print('Failed to make connection to S3')
            print('=====================')
            return



