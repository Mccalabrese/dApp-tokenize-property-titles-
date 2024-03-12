# dApp Tokenize Property Titles
## Deployment Instructions
**1. This was deployed using a Ganache local testnet, you must use Ganache CLI, NOT GUI. Ensure that your Ganache testnet is set to the London hardfork. See the image below:**
![image](https://github.com/Mccalabrese/dApp-tokenize-property-titles-/blob/d62eb7f0e47163effd8f0a67e1c98a639dd4c715/images/Ganache%20CLI.png)

**2. Connect your Ganache testnet to Metamask. See image below:**
![image](https://github.com/Mccalabrese/dApp-tokenize-property-titles-/blob/d62eb7f0e47163effd8f0a67e1c98a639dd4c715/images/Connect%20MetaMask%20to%20Ganache.png)

**3. Compile the contract, TitleRegistry.sol (located in contracts) in Remix IDE using solidity 0.8.24 and the EMV Version london:**
![image](https://github.com/Mccalabrese/dApp-tokenize-property-titles-/blob/d62eb7f0e47163effd8f0a67e1c98a639dd4c715/images/Compile%20Contract.png)

**4. Deploy the contract in Remix IDE:**
![image](https://github.com/Mccalabrese/dApp-tokenize-property-titles-/blob/d62eb7f0e47163effd8f0a67e1c98a639dd4c715/images/Deploy%20Contract.png)


**5. Deploy the streamlit app (app.py):**
![image](https://github.com/Mccalabrese/dApp-tokenize-property-titles-/blob/d62eb7f0e47163effd8f0a67e1c98a639dd4c715/images/Deploy%20app.png)


## Using the Application
![image](https://github.com/Mccalabrese/dApp-tokenize-property-titles-/blob/d62eb7f0e47163effd8f0a67e1c98a639dd4c715/images/Streamlit%20Home.png)


### Register a new title to IFPS
![image](https://github.com/Mccalabrese/dApp-tokenize-property-titles-/blob/d62eb7f0e47163effd8f0a67e1c98a639dd4c715/images/Register%20to%20IFPS.png)


![image](https://github.com/Mccalabrese/dApp-tokenize-property-titles-/blob/d62eb7f0e47163effd8f0a67e1c98a639dd4c715/images/IFPS%20Reciept%201.png)


![image](https://github.com/Mccalabrese/dApp-tokenize-property-titles-/blob/d62eb7f0e47163effd8f0a67e1c98a639dd4c715/images/IFPS%20Reciept%202.png)

#### Record a new sale of a previously uploaded IFPS Title
![image](https://github.com/Mccalabrese/dApp-tokenize-property-titles-/blob/d62eb7f0e47163effd8f0a67e1c98a639dd4c715/images/Record%20Sale%20Reciept.png)


#### View Sales Report History for IFPS Saved Titles
![image](https://github.com/Mccalabrese/dApp-tokenize-property-titles-/blob/d62eb7f0e47163effd8f0a67e1c98a639dd4c715/images/Sales%20Report%20History%201.png)


![image](https://github.com/Mccalabrese/dApp-tokenize-property-titles-/blob/d62eb7f0e47163effd8f0a67e1c98a639dd4c715/images/Sales%20Report%20History%202.png)


### Register Title data directly to the blockchain

**1. Enter title data and upload the PDF of the title, then in the selector box select "Direct to Blockchain"**
![image](https://github.com/Mccalabrese/dApp-tokenize-property-titles-/blob/d62eb7f0e47163effd8f0a67e1c98a639dd4c715/images/Register%20to%20Blockchain.png)

**2. Streamlit will provide a reciept of your transaction**
![image](https://github.com/Mccalabrese/dApp-tokenize-property-titles-/blob/d62eb7f0e47163effd8f0a67e1c98a639dd4c715/images/Upload%20to%20Blockchain%20Reciept.png)

**3. Your terminal running app.py is set to print the bytes data of your pdf, return to your terminal to view your pdf data**
![image](https://github.com/Mccalabrese/dApp-tokenize-property-titles-/blob/d62eb7f0e47163effd8f0a67e1c98a639dd4c715/images/PDF%20Byte%20Data.png)
