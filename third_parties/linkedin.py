import os
import requests
from dotenv import load_dotenv
import json





def scrape_linkedin_profile(linkedin_profile_url:str, mock:bool = False):
    """ scrape infromation from Linkedin profiles,
    Manually scrape the infromation from the linkedin profile"""

    if mock:
        with open("./mock_response.txt") as f:
            response = f.read()
            data = json.loads(response)
    else:
        api_endpoint = "https://nubela.co/proxycurl/api/v2/linkedin"
        header_dic ={"Authorization": f"Bearer {os.getenv('PROXYCURL_API_KEY')}"}
        response = requests.get(api_endpoint, 
                                 params={"url": linkedin_profile_url},
                                 headers=header_dic,
                                 timeout=10) 
        data = response.json()
    
    # remove empty keys and redundant fields in json object
    data = {
        k: v 
        for k, v in data.items() 
        if v not in(None, "", [], {})
        and k not in ["people_also_viewed", "certifications"]
   }
    if data.get("groups"):
        for group_dict in data.get("groups"):
            group_dict.pop("profile_pic_url")

    return data


if __name__ == "__main__":
    load_dotenv()
    print(scrape_linkedin_profile("https://www.linkedin.com/in/chrisgroks/", mock=True))
    