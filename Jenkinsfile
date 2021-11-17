@Library(value="d3b-center/d3b-flywheel-warehousing", changelog=false) _
pipeline {
   stage_name_1 = "Installing requirements"
   stage_name_2 = "Copying secrets file from AWS"
   stage_name_3 = "Scouring Flywheel"
   script_1 = "pip3 install -r requirements.txt"
   script_2 = "aws s3 cp [path-to-secrets-file] ."
   script_3 = "python3 scour_flywheel.py"
}