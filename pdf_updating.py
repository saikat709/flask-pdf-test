from pypdf import PdfReader, PdfWriter
from io import BytesIO


def populate_form_info(info):

    buffer = BytesIO()

    input_pdf = "f1040.pdf"
    # output_pdf = "f1040_filled.pdf"

    reader = PdfReader(input_pdf)
    writer = PdfWriter()
    writer.append(reader)

    page = writer.pages[0]

    writer.update_page_form_field_values(
        page,
        {
            "f1_01[0]": "January",
            "f1_02[0]": "February",
            "f1_03[0]": "24",
            "f1_04[0]": info.first_name or "N/A",
            "f1_05[0]": info.last_name or "N/A",
            "f1_06[0]": info.social_security_number or "000-00-0000",
            "f1_07[0]": info.spouse_first_name or "N/A",
            "f1_08[0]": info.spouse_last_name or "N/A",
            "f1_09[0]": info.spouse_social_security_number or "000-00-0000",
            "f1_10[0]": info.home_address or "N/A",
            "f1_11[0]": info.apt_no or "Apt 4B",
            "f1_12[0]": info.town or "Springfield",
            "f1_13[0]": info.state or "IL",
            "f1_14[0]": info.zip_code or "62704",
            "f1_15[0]": info.foreign_country_name or "Canada",
            "f1_16[0]": info.foreign_province or "Ontario",
            "f1_17[0]": info.foreign_postal_code or "K1A 0B1",

            "c1_1[0]": "/1" if info.presidential_election_campaign else "/Off", 
            "c1_2[0]": "/1" if info.presidential_election_campaign_spouse else "/Off",
        },
        auto_regenerate=True,
    )

    writer.write(buffer)
    buffer.seek(0)

    # with open(output_pdf, "wb") as f:
        # writer.write(f)
    # print(f"Filled PDF saved to {output_pdf}")

    return buffer



# checkbox_updates = {}

# for name, field in fields.items():
#     if field.get("/FT") == "/Btn":
#         on_val = get_checkbox_on_value(field)
#         print(f"Checkbox field: {name}, On value: {on_val}")
#         checkbox_updates[name] = on_val

# now apply to some page (first page is usually fine)
# writer.update_page_form_field_values(
#     writer.pages[0],
#     {
#         "c1_1[0]": "/0",
#     },
#     auto_regenerate=True,
# )

# make viewers render it
# acroform = writer._root_object.get("/AcroForm")
# if acroform is not None:
#     acroform.update({"/NeedAppearances": True})



def print_form_fields():
    input_pdf = "f1040.pdf"
    reader = PdfReader(input_pdf)

    # dictionary = reader.get_form_text_fields()
    # for field, value in dictionary.items():
        # print(f"Text Field: {field}, Value: {value}\n")

    for name, field in reader.get_fields().items():
        field_type = field.get("/FT")
        if field_type == "/Btn":
            print(f"Checkbox Field: {name}, Value: {field.get('/V')}, States: {field.get('/_States_')}")
        if field_type == "/Tx":
            print(f"Text Field: {name}, Value: {field.get('/V')}")
        

# if __name__ == "__main__":
#     # print_form_fields()
#     populate_form_info({})