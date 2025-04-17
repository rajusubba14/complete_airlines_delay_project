
import sagemaker
from sagemaker.model import Model
from time import gmtime, strftime

role = "arn:aws:iam::225989361602:role/service-role/AmazonSageMaker-ExecutionRole-20250406T095913"
sess = sagemaker.Session()
region = "us-east-1"
image_uri = "225989361602.dkr.ecr.us-east-1.amazonaws.com/aws_airline_delay_project:amd64_v12"  # Corrected image URI
model_data = "s3://mlprojects-raju/airlinesdelay/model/model.tar.gz"  # This must be a tar.gz archive containing model.joblib

# Create a unique model name
timestamp = strftime("%Y-%m-%d-%H-%M-%S", gmtime())
model_name = f"airlinesdelay-model-{timestamp}"
endpoint_name = f"airlines-endpoint-{timestamp}"

# Create and deploy the model
model = Model(
    name=model_name,
    image_uri=image_uri,
    model_data=model_data,
    role=role,
    sagemaker_session=sagemaker.Session()
)

predictor = model.deploy(
    initial_instance_count=1,
    instance_type="ml.m5.2xlarge",  # You can choose a smaller instance if needed
    endpoint_name=endpoint_name
)

print("✅ Deployed to endpoint:", predictor.endpoint_name)