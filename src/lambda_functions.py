import boto3
import json
from os import path
from utils import Utils

LAMBDA_ACCESS_POLICY_ARN='arn:aws:iam::865881670086:policy/LambdaS3AccessPolicy'
LAMBDA_ROLE = 'Lambda_Execution_Role'
LAMBDA_ROLE_ARN = 'arn:aws:iam::865881670086:role/Lambda_Execution_Role'
LAMBDA_TIMEOUT = 10
LAMBDA_MEMORY = 128
NODEJS_810_RUNTIME = 'nodejs8.10'
PYTHON_36_RUNTIME = 'python3.6'
PYTHON_LAMBDA_NAME = 'PythonLambdaFuntion'
NODEJS_LAMBDA_NAME = 'NodeJsLambdaFunction'

LAMBDA_HANDLER = 'lambda_function.handler'

def lambda_client():
    aws_lambda = boto3.client('lambda',region_name='us-east-2')
    """ :type : pyboto3.lambda"""
    return aws_lambda


def iam_client():
    iam  = boto3.client('iam')
    """ :type : pyboto3.iam """
    return iam

def create_access_policy_for_lambda():
    s3_access_policy_document = {
        "Version" : "2012-10-17",
        "Statement":[
            {
                "Effect": "Allow",
                "Action": [
                    "s3:*",
                    "logs:CreateLogGroup",
                    "logs:CreateLogStream",
                    "logs:PutLogEvents"

                ],
                
                "Resource":"*"

            }
        ]

    }

    return iam_client().create_policy(
        PolicyName='LambdaS3AccessPolicy',
        PolicyDocument=json.dumps(s3_access_policy_document),
        Description='Allows Lambda Function to access S3 resources'
    )

def create_execution_role_for_lambda():
    lambda_execution_assumption_role = {
        "Version":"2012-10-17",
        "Statement":[
            {
                "Effect":"Allow",
                "Principal":{
                    "Service": "lambda.amazonaws.com"
                },
                "Action": "sts:AssumeRole"
             }
        ]
    }
    return iam_client().create_role(
        RoleName=LAMBDA_ROLE,
        AssumeRolePolicyDocument=json.dumps(lambda_execution_assumption_role),
        Description = "Gives necessary permissions for Lambda to be executed"
    )


def attach_access_policy_to_execution_role():
    return iam_client().attach_role_policy(
        RoleName=LAMBDA_ROLE,
        PolicyArn=LAMBDA_ACCESS_POLICY_ARN
    )


def deploy_lambda_funtion(funtion_name, runtime, handler, role_arn, source_folder):
    
    folder_path = path.join(path.dirname(path.abspath(__file__)), source_folder)
    zip_file = Utils.make_zip_file_bytes(path=folder_path)

    return lambda_client().create_function(
        FunctionName=funtion_name,
        Runtime=runtime,
        Role=role_arn,
        Handler=handler,
        Code={
            'ZipFile': zip_file
        },
        Timeout=LAMBDA_TIMEOUT,
        MemorySize=LAMBDA_MEMORY,
        Publish=False

    )

def invoke_lambda_function(function_name):
    return lambda_client().invoke(FunctionName=function_name)


def update_environment_variables_to_lambda(function_name,variables):
    return lambda_client().update_function_configuration(
        FunctionName=function_name,
        Environment=variables
    )

def update_lambda_function_code(function_name, source_folder ):
    folder_path = path.join(path.dirname(path.abspath(__file__)), source_folder)
    zip_file = Utils.make_zip_file_bytes(path=folder_path)
    return lambda_client().update_function_code(
        FunctionName=function_name,
        ZipFile=zip_file
    )

def publish_a_new_version(function_name):
    return lambda_client().publish_version(
        FunctionName=function_name
    )

def create_alias_for_new_version(function_name, alias_name, version):
    return lambda_client().create_alias(
        FunctionName=function_name,
        Name=alias_name,
        FunctionVersion=version,
        Description="This is the "+ alias_name + "alias for a version"     
    )

def invoke_lambda_with_alias(function_name,alias_name):
    return lambda_client().invoke(
        FunctionName=function_name,
        Qualifier=alias_name
    )

def get_function_details(function_name):
    return lambda_client().get_function(FunctionName=function_name)

def get_all_fucntion():
    return lambda_client().list_functions()


def update_function_execution_memory(function_name,new_memory_size):
    return lambda_client().update_function_configuration(
        FunctionName=function_name,
        MemorySize=new_memory_size
    )

def delete_lambda_function(function_name):
    return lambda_client().delete_function(FunctionName=function_name)

if __name__ == '__main__':
    #print(create_access_policy_for_lambda())

    #print(create_execution_role_for_lambda())
    #print(attach_access_policy_to_execution_role())
    #print(deploy_lambda_funtion(PYTHON_LAMBDA_NAME,PYTHON_36_RUNTIME,LAMBDA_HANDLER,LAMBDA_ROLE_ARN,'python_lambda'))
    #print(deploy_lambda_funtion(NODEJS_LAMBDA_NAME,NODEJS_810_RUNTIME,LAMBDA_HANDLER,LAMBDA_ROLE_ARN,'nodejs_lambda'))
    # response = invoke_lambda_function(PYTHON_LAMBDA_NAME)
    # dict = response['Payload'].read().decode()

    # print(type(dict))
    # a = json.loads(dict)
    # print(type(a))

    # for i,j in a.items():
    #     print(j)


    # env_variables = {
    #     'Variables':{
    #         'ENV_VAR_TEST': 'This is an environment variables'
    #     }

    # }
    # print(update_environment_variables_to_lambda(PYTHON_LAMBDA_NAME,env_variables))
    #print(update_lambda_function_code(PYTHON_LAMBDA_NAME, 'python_lambda'))
    # response = invoke_lambda_function(PYTHON_LAMBDA_NAME)
    # dict = response['Payload'].read().decode()
    # print(dict)

    #print(publish_a_new_version(PYTHON_LAMBDA_NAME))
    #print(create_alias_for_new_version(PYTHON_LAMBDA_NAME,'PROD','1'))
    # response=invoke_lambda_with_alias(PYTHON_LAMBDA_NAME,'PROD')
    # dict=response['Payload'].read().decode()
    # print(dict)
    #print(get_function_details(PYTHON_LAMBDA_NAME))
    #print(get_all_fucntion())
    #(update_function_execution_memory(PYTHON_LAMBDA_NAME,256))
    print(delete_lambda_function(NODEJS_LAMBDA_NAME))
