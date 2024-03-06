import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
from typing import Any, List

from pinata import pin_file_to_ipfs, pin_json_to_ipfs, convert_data_to_json

load_dotenv("env.txt")

# Define and connect a new Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

contract_address = os.getenv("SMART_CONTRACT_ADDRESS")

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


def get_option():
    """Display the database of TitleUpload information."""
    db_list = list(options_database.values())

    for option in range(len(options)):
        st.write("More Info: ", db_list[option][0])
        st.write("Cost of upload in Ether: ", db_list[option][1], "eth")
        st.text(" \n")


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
    ipfs_file_hash = pin_file_to_ipfs(title_file.getvalue())

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
file = st.file_uploader("Upload Title", type=["jpg", "jpeg", "png", "pdf"])

upload_options = st.selectbox("Select an Option", options)

if upload_options == "Upload Title to IFPS":
    choice = options_database[upload_options][0]
    choice_cost = options_database[upload_options][1]

    to_address = "0x56c31FF8a66e7aDCF370Fa0eA723056E61d55Bc6"
    value = 0
    data = 0
    estimated_gas = w3.eth.estimateGas({
        "from": address,
        "to": to_address,
        "value": value,
        "data": data,
    })
    transaction_value_IFPS = estimated_gas * 20

    
    st.write("## Option Types, and Cost")
    st.write(choice)
    st.write(transaction_value_IFPS)

    if st.button("Register Title"):
        transaction_IFPS = {
            "from": address,
            "to": to_address,
            "value": transaction_value_IFPS,
        }
        tx_hash = w3.eth.sendTransaction(transaction_IFPS)
        st.write(tx_hash)
        receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        receipt_dict = dict(receipt)
        st.write(receipt_dict)

        if receipt_dict.get("status") == 1:
        

            title_ipfs_hash, token_json = pin_title(title_name, file)

            title_uri = f"ipfs://{title_ipfs_hash}"

            tx_hash_NFT = contract.functions.registerTitle(
                address,
                title_name,
                owner_name,
                int(initial_sale_value),
                title_uri,
                token_json['image']
            ).transact({'from': address, 'gas': 1000000})
            receipt = w3.eth.waitForTransactionReceipt(tx_hash_NFT)
            st.write("Transaction receipt mined:")
            st.write(dict(receipt))
            st.write("You can view the pinned metadata file with the following IPFS Gateway Link")
            st.markdown(f"[Title IPFS Gateway Link](https://ipfs.io/ipfs/{title_ipfs_hash})")
            st.markdown(f"[Title IPFS Image Link](https://ipfs.io/ipfs/{token_json['image']})")


if upload_options == "Upload Title Blockchain":
    choice = options_database[upload_options][0]
    choice_cost = options_database[upload_options][1]

    to_address = "0x56c31FF8a66e7aDCF370Fa0eA723056E61d55Bc6"
    value = 0
    data = 0
    estimated_gas = w3.eth.estimateGas({
        "from": address,
        "to": to_address,
        "value": value,
        "data": data,
    })
    transaction_value_BLOC = estimated_gas * 2 
    
    
    st.write("## Option Types, and Cost")
    st.write(choice)
    st.write(transaction_value_BLOC)

    if st.button("Register Title"):
        transaction_BLOC = {
            "from": address,
            "to": to_address,
            "value": transaction_value_BLOC,
            "data": data,
        }
        tx_hash = w3.eth.sendTransaction(transaction_BLOC)
        st.write(tx_hash)
        receipt = w3.eth.waitForTransactionReceipt(tx_hash)
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
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    st.write(receipt)
st.markdown("---")

################################################################################
# Get Appraisals
################################################################################
st.markdown("## Get the sale report history")
title_token_id = st.number_input("Title ID", value=0, step=1)
if st.button("Get Sale Reports"):
    sale_filter = contract.events.Sale.createFilter(
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



