import os
import PyPDF2


# pdf_path = "Special Warranty.pdf"

# with open(pdf_path, 'rb') as pdf_file:
#     file_bytes = pdf_file.read()

# # print(file_bytes)
# hex_data = file_bytes.hex()
# # print(type(hex_data))
# # print(hex_data)

data = "hello"
hex_string = data.encode("utf-8").hex()
print(hex_string)
   