import requests
import streamlit as st

def pagerank(domain, api_key):

    try:
        endpoint = "https://openpagerank.com/api/v1.0/getPageRank"
        headers = {"API-OPR": api_key}
        params = {"domains[]": domain}

        response = requests.get(endpoint, headers=headers, params=params)

        if response.status_code == 200:
            data = response.json()
            return data['response'][0]['page_rank_integer']
        else:
            st.write(f"Error: {response.status_code}, {response.text}")
            return -1  # Return -1 in case of an error

    except Exception as e:
        st.write(f"Exception occurred while fetching page rank: {e}")
        return -1
