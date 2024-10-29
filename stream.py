import pandas as pd
from features.get_domain_age import get_root_domain, get_domain_creation_date, days_passed_since
from features.get_page_rank import pagerank
from features.get_CAstatus import is_free_certificate
from features.get_domain_validity import get_validity_period
from src.get_domain import get_domain
from features.get_securitystatus import has_protective_statuses
from features.get_securitystatus2 import has_strong_security_headers
from features.get_catchingInfo_compressedinfo import check_caching_and_compression
import joblib
import pickle
import streamlit as st
from logger.logs import logger_info
from email_sender import sendmail

model = joblib.load('ocsvm_model.h5')
with open('scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

def map_boolean(value):
    if value is True:
        return 1
    elif value is None:
        return -1
    else:
        return 0

def map_security_status(security_list):
    if isinstance(security_list, list):
        return [map_boolean(i) for i in security_list]
    return -1

def main():
    st.title("URL Legitimacy Tracker")

    api_key = st.text_input('Enter your API Key for PageRank:',  type="password")
    sender_email = st.text_area("Enter the email id:")
    password = st.text_input('Enter your email password:',  type="password")

    user_input = st.text_area("Enter the URL:")
    if st.button("Enter") and user_input:
        try:
            url = user_input
            domain_age = days_passed_since(get_domain_creation_date(get_root_domain(url)))
            page_rank = pagerank(get_domain(url),api_key)
            is_free = is_free_certificate(url)
            validation_period = get_validity_period(url)
            has_protective_status = has_protective_statuses(url)
            has_strong_security = has_strong_security_headers(url)
            caching, compressed = check_caching_and_compression(url)

            data = pd.DataFrame({
                'Domain Age': [domain_age],
                'Page Rank': [page_rank],
                'Is Free': [is_free],
                'Validation Period': [validation_period],
                'Has Protective Status': [has_protective_status],
                'Has Strong Security': [has_strong_security],  # list value
                'Caching': [caching],
                'Compressed': [compressed],
            })
            print(data)

            data['Is Free'] = data['Is Free'].apply(map_boolean)
            data['Has Protective Status'] = data['Has Protective Status'].apply(map_boolean)
            data['Caching'] = data['Caching'].apply(map_boolean)
            data['Compressed'] = data['Compressed'].apply(map_boolean)
            data['Has Strong Security'] = data['Has Strong Security'].apply(map_security_status)  # Apply mapping to each element in the list

            data.fillna(-1, inplace=True)
            st.write(data)

            print(data)

            data_scaled = scaler.transform(data)
            prediction = model.predict(data_scaled)

            if prediction[0] == -1:
                outcome_message = 'The URL is predicted to be suspicious.'
            else:
                outcome_message = 'The URL is predicted to be safe.'

            st.write(outcome_message)

            logger_info(f"Outcome for URL {url} is {outcome_message}")
            sendmail(sender_email,"diti.b@acviss.com", url, f'Outcome for {url} is ---> {outcome_message}',password)

        except Exception as e:
            st.write(f"Error processing the URL: {e}")
    # else:
    #     st.write("Please upload a valid keys.yaml file to proceed.")


if __name__ == "__main__":
    main()
