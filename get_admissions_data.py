#!/bin/bash


from requests import get

def get_data(url):
    response = get(endpoint, timeout=10)
    
    if response.status_code >= 400:
        raise RuntimeError(f'Request failed: { response.text }')
        
    return response.text
    

if __name__ == '__main__':
    endpoint = (
        'https://api.coronavirus.data.gov.uk/v1/data?'
        'filters=areaType=nhsRegion&'
        'structure={"name":"areaName","date":"date","hospitalCases":"hospitalCases"}&'
        'format=csv'
    )
    
    data = get_data(endpoint)
    print(data)
    with open("data/r_admissions.csv","w") as f:
        f.write(data)
        f.close()


