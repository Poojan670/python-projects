import json

import openpyxl


def excel_config():
    """
    Excel Config for openpyxl excel config
    :return excel & sheet:
    """
    excel = openpyxl.Workbook()
    sheet = excel.active
    sheet.title = f"Recruiting Agencies Nepal"
    sheet.append(
        ['SN', 'permission_no', 'name', 'address', "contact_no", "status"]
    )

    return excel, sheet


"""
GET JSON DATA USING

url = "https://srv.dofe.gov.np/Services/DofeWebService.svc/GetApprovedRaList"
response = requests.post(url, data={"offset": 1,
                                    "limit": 1487,
                                    "permissionNo": "",
                                    "name": "",
                                    "statusID": 0})

"""

excel, sheet = excel_config()

f = open("data.json", "r")
json_data = json.load(f)
data = json_data.get("d")
for dat in data:
    SN = dat.get("RowNum")
    permission_no = dat.get("PermissionNo")
    name = dat.get("Name")
    address = dat.get("Address")
    contact_no = dat.get("Telephone")
    status = dat.get("StatusName")
    print(SN, permission_no, name, address, contact_no, status)
    sheet.append([SN, permission_no, name, address, contact_no, status])
excel.save("Recruiting Agencies Nepal.xlsx")

print("Successfully scrapped")
