import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

def get_parameter(name):
    try:
        # Specify the region explicitly
        ssm = boto3.client('ssm', region_name='eu-north-1')  # Replace with your region
        response = ssm.get_parameter(Name=name, WithDecryption=True)
        return response['Parameter']['Value']
    except (NoCredentialsError, PartialCredentialsError):
        print(f"Error getting {name}: Unable to locate credentials")
        return "[FAILED]"
    except Exception as e:
        print(f"Error getting {name}: {str(e)}")
        return "[FAILED]"

if __name__ == "__main__":
    parameters = [
        "/DATABASE_EXCEL_PATH",
        "/GOOGLE_APPLICATION_CREDENTIALS",
        "/OPENAI_API_KEY",
        "/ROBOTNAME"
    ]

    for param in parameters:
        value = get_parameter(param)
        print(f"{param}: {value}")