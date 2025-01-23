import boto3

def get_parameter(param_name):
    ssm = boto3.client('ssm')
    try:
        response = ssm.get_parameter(Name=param_name, WithDecryption=True)
        return response['Parameter']['Value']
    except Exception as e:
        print(f"Error getting {param_name}: {e}")
        return None

# Test all parameters
params = [
    '/DATABASE_EXCEL_PATH',
    '/GOOGLE_APPLICATION_CREDENTIALS',
    '/OPENAI_API_KEY',
    '/ROBOTNAME'
]

for param in params:
    value = get_parameter(param)
    print(f"{param}: {'[SUCCESS]' if value else '[FAILED]'}")