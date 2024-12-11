# For API funcitons
import os
import json
import requests
import base64
import pytz

%%capture
!pip install python-dotenv

from dotenv import load_dotenv
from datetime import datetime

def my_date_time():
  #  Nov 1, 2024
    date_time_format = "%b %e, %I:%M %p"  
    current_time = datetime.now( pytz.timezone("Asia/Kolkata") )
    return current_time.strftime(date_time_format)

def upload_to_github(github_token, repo_owner, repo_name, file_path, commit_message, branch='main'):
    api_url = "https://api.github.com/repos/parth-f/Analyse-Health-and-Demographic-Data-to-identify-common-traits-leading-to-Heart-Disease/contents/Analyse_Health_and_Demogrphic_Data_to_identify_common_traits_leading_to_Heart_Disease_Practo_Certified.ipynb"

    # Checking if env variable already exist, if yes, replace it
    os.environ.pop('SecretKey.env', None)

    load_dotenv('/content/drive/MyDrive/Data/SecretKey.env')
    headers = {
        "Authorization": f"token {os.getenv('SecretKey')}",
        "Accept": "application/vnd.github.v3+json"
    }
  
    notebook_name = 'Analyse_Health_and_Demogrphic_Data_to_identify_common_traits_leading_to_Heart_Disease-Practo_Certified.ipynb'
    # Read notebook content
    notebook_path = f'/content/drive/MyDrive/Colab Notebooks/{notebook_name}'
  
    try:
        with open(notebook_path, 'r') as f:
            content = f.read()

        content_bytes = content.encode('utf-8')
        content_base64 = base64.b64encode(content_bytes).decode('utf-8')

        # Prepare data for GitHub API
        data = {
            "message": commit_message,
            "content": content_base64,
            "branch": branch
        }

        # Check for existing file to update
        try:
            response = requests.get(api_url, headers=headers)
            if response.status_code == 200:
                data['sha'] = response.json()['sha']
        except Exception as e:
            print(f"Error checking file: {e}")

        # Upload to GitHub
        response = requests.put(api_url, headers=headers, data=json.dumps(data))

        if response.status_code in [200, 201]:
            print(f"Successfully uploaded {notebook_name} to GitHub!")
            return True
        else:
            print(f"Upload failed. Status code: {response.status_code}")
            print(response.text)
            return False

    except FileNotFoundError:
        print(f"Error: Notebook not found at {notebook_path}")
        print("Checking available files in /content directory:")
        print(os.listdir('/content'))
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False
