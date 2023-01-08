# oc-process-discovery
A process discovery tool working on object-centric event logs extracted from SAP ERP. It was developed in the "Process Discovery Using Python" lab at RWTH. 

# Manual setup: Python venv
This project uses Python 3.9.13

1. Create virtual environment. For example with `python -m venv venv`
2. Activate virtual environment. For example with `source venv/bin/activate` or `venv\Scripts\activate.ps1` 
3. Install dependencies with `pip install -r requirements.txt --use-deprecated=legacy-resolver `
4. add /environment/.env file with content from .env.development
5. Run project / index.py
   1. in vs code: use the configuration stored in launch.json file
   2. in pycharm: use the configuration stored in .idea/runConfigurations/oc_process_discovery.xml file

# Docker setup
Note: Because SAPnwRFC is Plattform depencent and can't be shared in this repository due to lizensing, Extraction directly from SAP systems is yet not possible in Docker.
1. Check if pyrfc is commented out in requiremnts.txt
2. execute `docker build -t ocpaapp .`
3. run image


