@Library(value="kids-first/aws-infra-jenkins-shared-libraries", changelog=false) _
pipeline {
   stage_name_1 = "Installing requirements"
   stage_name_2 = "Copying secrets file from AWS"
   stage_name_3 = "Sourcing environment variables"
   stage_name_4 = "Scouring Flywheel"
   script_1 = "pip3 install -r requirements.txt"
   script_2 = "aws s3 cp s3://d3b-684194535433-us-east-1-service-secrets/d3b-flywheel-warehousing/app.secrets ."
   script_3 = "./app.secrets"
   script_4 = "python3 scour_flywheel.py"
}