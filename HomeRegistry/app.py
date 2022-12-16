import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

# Define and connect a new Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

################################################################################
# Contract Helper function:
# 1. Loads the contract once using cache
# 2. Connects to the contract using the contract address and ABI
################################################################################


@st.cache(allow_output_mutation=True)
def load_contract():

    # Load the contract ABI
    with open(Path('./contracts/compiled/home_registry_abi.json')) as f:
        contract_abi = json.load(f)

    # Set the contract address (this is the address of the deployed contract)
    contract_address = os.getenv("SMART_CONTRACT_ADDRESS")

    # Get the contract
    contract = w3.eth.contract(
        address=contract_address,
        abi=contract_abi
    )

    return contract


# Load the contract
contract = load_contract()


st.title("Home Appraisal System")
st.write("Choose an account to get started")
accounts = w3.eth.accounts
address = st.selectbox("Select Account", options=accounts)
st.markdown("---")

################################################################################
# Register New Artwork
################################################################################
st.markdown("## Register Your Home")

home_address = st.text_input("Enter address of the home")
sqt_ft = st.text_input("Enter total square footage")
bedrooms = st.text_input("Enter number of bedrooms")
bathrooms = st.text_input("Enter number of bathrooms")
home_value = st.text_input("Enter the initial appraisal amount")
zillow_link = st.text_input("Enter Zillow Link")
yearbuilt = st.text_input("Enter the Year built")
artwork_uri = st.text_input("Enter an Image of your Home")

if st.button("Register Home"):
    tx_hash = contract.functions.registerhome(
        address,
        home_address,
        sqt_ft,
        bedrooms,
        bathrooms,
        int(home_value),
        zillow_link,
        yearbuilt,
        artwork_uri
    ).transact({'from': address, 'gas': 1000000})
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    st.write("Transaction receipt mined:")
    st.write(dict(receipt))
st.markdown("---")


################################################################################
# Appraise Art
################################################################################
#st.markdown("## Appraise Artwork")
#tokens = contract.functions.totalSupply().call()
#token_id = st.selectbox("Choose an Art Token ID", list(range(tokens)))
#new_appraisal_value = st.text_input("Enter the new appraisal amount")
#report_uri = st.text_area("Enter notes about the appraisal")
#if st.button("Appraise Artwork"):

     # Use the token_id and the report_uri to record the appraisal
     #tx_hash = contract.functions.newAppraisal(
         #token_id,
         #int(new_appraisal_value),
         #report_uri
     #).transact({"from": w3.eth.accounts[0]})
     #receipt = w3.eth.waitForTransactionReceipt(tx_hash)
     #st.write(receipt)
     #st.markdown("---")

################################################################################
# Get Appraisals
################################################################################
st.markdown("## Get Home Registry Details")
art_token_id = st.number_input("Token ID", value=0, step=1)
if st.button("Get Details"):
    appraisal_filter = contract.events.home_summary.createFilter(
        fromBlock=0,
        argument_filters={"tokenId": art_token_id}
    )
    appraisals = appraisal_filter.get_all_entries()
    if appraisals:
        for appraisal in appraisals:
            report_dictionary = dict(appraisal)
            #st.markdown("### Appraisal Report Event Log")
            #st.write(report_dictionary)

            st.markdown("### Registry Details")
            #st.write(report_dictionary["args"])

            st.markdown("#### Home Address")
            st.write(report_dictionary["args"]["home_address"])

            st.markdown("#### Square Feet")
            st.write(report_dictionary["args"]["sqt_ft"])

            st.markdown("#### Number of Bedrooms")
            st.write(report_dictionary["args"]["bedrooms"])

            st.markdown("#### Number of Bathrooms")
            st.write(report_dictionary["args"]["bathrooms"])

            st.markdown("#### Home Value")
            st.write(report_dictionary["args"]["home_value"])

            st.markdown("#### Zillow Link")
            st.write(report_dictionary["args"]["zillow_link"])
         
            st.markdown("#### Year Built")
            st.write(report_dictionary["args"]["yearbuilt"])

            token_uri = contract.functions.tokenURI(art_token_id).call()
            #st.write(f"The tokenURI is {token_uri}")
            st.image(token_uri)
    else:
        st.write("This artwork has no new appraisals")
