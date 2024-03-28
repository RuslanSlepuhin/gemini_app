import pandas as pd

async def excel_compose_dict(data, fields) -> dict:
    report_excel_dict = {}
    for user in data:
        for field in fields:
            if not report_excel_dict.get(field):
                report_excel_dict[field] = []
            report_excel_dict[field].append(user[field])
    return report_excel_dict

async def write_to_excel(report_excel_dict, path) -> str:
    df = pd.DataFrame(
        report_excel_dict
        # {
        #     'id': user_excel_data['id'],
        #     'access_hash': user_excel_data['access_hash'],
        #     'username': user_excel_data['username'],
        #     'first_name': user_excel_data['first_name'],
        #     'last_name': user_excel_data['last_name'],
        #     'mutual_contact': user_excel_data['mutual_contact'],
        #     'phone': user_excel_data['phone'],
        #     'sending_report': user_excel_data['sending_report'] if user_excel_data.get("sending_report") else ["-" for i in range(0, len(user_excel_data['id']))]
        # }
    )

    df.to_excel(path, sheet_name='Sheet1')
    print(f'\nExcel was writting')
    return path
