@Library(value="kids-first/aws-infra-jenkins-shared-libraries", changelog=false) _
simple_pipeline {
   cron_schedule = "H 9 * * 1-5"
   notifyMe = "<@U01FZG0PDGU>,<@U027B7RMBH9>"
   stage_name_1 = "Installing requirements"
   stage_name_2 = "Copying secrets file from AWS"
   stage_name_3 = "Sourcing environment variables"
   stage_name_4 = "Scour"
   script_1 = "pip3 install -r requirements.txt"
   script_2 = "aws s3 cp s3://d3b-684194535433-us-east-1-service-secrets/d3b-flywheel-warehousing/app.secrets ."
   script_3 = "chmod +x ./app.secrets"
   script_4 = "sh ./app.secrets"
}
