import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
from typing import Any, List
import PyPDF2
import re 


from pinata import pin_file_to_ipfs, pin_json_to_ipfs, convert_data_to_json

st.set_page_config(
    page_title="Ethereum Title Records",
    page_icon=":house:",
    layout="wide",
    initial_sidebar_state="expanded"
)
load_dotenv("env.txt")

# Define and connect a new Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

contract_address = os.getenv("SMART_CONTRACT_ADDRESS")

to_address = "0x102637329333A6aE92F418Cd48E34f67960283dd"

# KryptoJobs2Go Candidate Information

# Database of KryptoJobs2Go candidates including their name, digital address, rating and hourly cost per Ether.
# A single Ether is currently valued at $1,500
options_database = {
    "Upload Title to IFPS": [
        "IFPS is a decentralized server platform were your title will be searchable, however the title will only be saved on a select number of nodes.",
        0.20,
    ],
    "Upload Title Blockchain": [
        "This will save the title directly to the Ethereum blockchain, this is irreversable and a copy will remain on the ledger forever.",
        0.33,
    ],
    
}

# A list of the TitleUpload options 
options = ["Upload Title to IFPS", "Upload Title Blockchain"]


################################################################################
# Load_Contract Function
################################################################################


@st.cache_resource()
def load_contract():

    # Load the contract ABI
    with open(Path('./contracts/compiled/titleregistry_abi.json')) as f:
        contract_abi = json.load(f)



    # Get the contract
    contract = w3.eth.contract(
        address=contract_address,
        abi=contract_abi
    )

    return contract


# Load the contract
contract = load_contract()

################################################################################
# Helper functions to pin files and json to Pinata
################################################################################


def pin_title(title_name, title_file):
    # Pin the file to IPFS with Pinata
    r = pin_file_to_ipfs(title_file.getvalue())
    ipfs_file_hash = r
    # Build a token metadata file for the artwork
    token_json = {
        "name": title_name,
        "image": ipfs_file_hash
    }
    json_data = convert_data_to_json(token_json)

    # Pin the json to IPFS with Pinata
    json_ipfs_hash = pin_json_to_ipfs(json_data)

    return json_ipfs_hash, token_json


def pin_sale_report(report_content):
    json_report = convert_data_to_json(report_content)
    report_ipfs_hash = pin_json_to_ipfs(json_report)
    return report_ipfs_hash
 
# def pay_for_service(amount, pdf_data):
#     # Convert the PDF data to hexadecimal format
#     hex_data = pdf_to_hex(pdf_data)

#     # Define the contract function call data
#     data = {"amount": amount, "pdfData": hex_data}

#     # Send a POST request to the Solidity contract endpoint
#     response = requests.post("0x34d50B1A0796185D8Fd1f69D4f42784b6a1f0BDA", data=json.dumps(data))

#     # Check if the request was successful
#     if response.status_code == 200:
#         result = response.json()
#         return result
#     else:
#         return {"error": "Failed to call contract function"}


# if st.button("Send Transaction"):

st.title("Title Registry- Record Sale System")
st.write("Choose an account to get started")
accounts = w3.eth.accounts
address = st.selectbox("Select Account", options=accounts)
st.markdown("---")

################################################################################
# Register New Title
################################################################################


st.markdown("## Register New Title")
title_name = st.text_input("Enter the name of the title (Address recomended)")
owner_name = st.text_input("Enter the owner's name")
initial_sale_value = st.text_input("Enter the initial sale amount")

# Use the Streamlit `file_uploader` function create the list of digital image file types(jpg, jpeg, or png) that will be uploaded to Pinata.
uploaded_file = st.file_uploader("Upload Title", type=["jpg", "jpeg", "png", "pdf"])
upload_options = st.selectbox("Select an Option", options)

if upload_options == "Upload Title to IFPS":
    choice = options_database[upload_options][0]
    choice_cost = options_database[upload_options][1]

    value = 0
    data = 0
    estimated_gas = w3.eth.estimate_gas({
        "from": address,
        "to": to_address,
        "value": value,
        "data": data,
    })
    transaction_value_IFPS = estimated_gas * 20

    
    st.write("## Option Types, and Cost")
    st.write(choice)
    st.write(transaction_value_IFPS)

    if uploaded_file is not None and initial_sale_value != "" and  st.button("Register Title"):
        transaction_IFPS = {
            "from": address,
            "to": to_address,
            "value": transaction_value_IFPS,
        }
        tx_hash = w3.eth.send_transaction(transaction_IFPS)
        st.write(tx_hash)
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        receipt_dict = dict(receipt)
        st.write(receipt_dict)

        if receipt_dict.get("status") == 1:
        

            title_ipfs_hash, token_json = pin_title(title_name, uploaded_file)

            title_uri = f"ipfs://{title_ipfs_hash}"

            tx_hash_NFT = contract.functions.registerTitle(
                address,
                title_name,
                owner_name,
                int(initial_sale_value),
                title_uri,
                token_json['image']
            ).transact({'from': address, 'gas': 1000000})
            receipt = w3.eth.wait_for_transaction_receipt(tx_hash_NFT)
            st.write("Transaction receipt mined:")
            st.write(dict(receipt))
            st.write("You can view the pinned metadata file with the following IPFS Gateway Link")
            st.markdown(f"[Title IPFS Gateway Link](https://ipfs.io/ipfs/{title_ipfs_hash})")
            st.markdown(f"[Title IPFS Image Link](https://ipfs.io/ipfs/{token_json['image']})")


if upload_options == "Upload Title Blockchain":
    choice = options_database[upload_options][0]
    choice_cost = options_database[upload_options][1]

    value = 0
    # file_bytes = uploaded_file.read()
    bytes_string = uploaded_file.read()
    # data = file_bytes.hex()
    print(bytes_string)
    st.write("## Option Types, and Cost")
    st.write(choice)
    if bytes_string is not None and uploaded_file is not None and initial_sale_value != "":
        estimated_gas = w3.eth.estimate_gas({
            'from': address,
            'to': to_address,
            "value": 0,
            'data': bytes_string, # The data field should be the hex string
            # Add other necessary transaction fields
        })
        transaction_value_BLOC = estimated_gas * 2 
        st.write(transaction_value_BLOC)

        if st.button("Register Title"):
            tx_hash = contract.functions.payForService(
                amount=transaction_value_BLOC, 
                pdfData=bytes_string
            ).transact({'from': address, 'value': 0, 'gas': 10031156})
            receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
            receipt_dict = dict(receipt)
            st.write(receipt_dict)

st.markdown("---")


################################################################################
# Record New Sale
################################################################################
st.markdown("## Record Sale")
tokens = contract.functions.totalSupply().call()
token_id = st.selectbox("Choose an Title Token ID", list(range(tokens)))
new_sale_value = st.text_input("Enter the new sale amount")
sale_report_content = st.text_area("Enter details for the Sale Report")

if st.button("Record Sale"):

    # Make a call to the contract to get the image uri
    image_uri = str(contract.functions.imageUri(token_id).call())
    
    # Use Pinata to pin an appraisal report for the report content
    sale_report_ipfs_hash =  pin_sale_report(sale_report_content+image_uri)

    # Copy and save the URI to this report for later use as the smart contract’s `reportURI` parameter.
    report_uri = f"ipfs://{sale_report_ipfs_hash}"

    tx_hash = contract.functions.newSale(
        token_id,
        int(new_sale_value),
        report_uri,
        image_uri

    ).transact({"from": w3.eth.accounts[0]})
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    st.write(receipt)
st.markdown("---")

################################################################################
# Get Appraisals
################################################################################
st.markdown("## Get the sale report history")
title_token_id = st.number_input("Title ID", value=0, step=1)
if st.button("Get Sale Reports"):
    sale_filter = contract.events.Sale.create_filter(
        fromBlock=0, argument_filters={"tokenId": title_token_id}
    )
    reports = sale_filter.get_all_entries()
    if reports:
        for report in reports:
            report_dictionary = dict(report)
            st.markdown("### Sales Report Event Log")
            st.write(report_dictionary)
            st.markdown("### Pinata IPFS Report URI")
            report_uri = report_dictionary["args"]["reportURI"]
            report_ipfs_hash = report_uri[7:]
            image_uri = report_dictionary["args"]["titleJson"]
            st.markdown(
                f"The report is located at the following URI: "
                f"{report_uri}"
            )
            st.write("You can also view the report URI with the following ipfs gateway link")
            st.markdown(f"[IPFS Gateway Link](https://ipfs.io/ipfs/{report_ipfs_hash})")
            st.markdown("### Sale Event Details")
            st.write(report_dictionary["args"])
            st.image(f'https://ipfs.io/ipfs/{image_uri}')
    else:
        st.write("This title has no new sale reports")



