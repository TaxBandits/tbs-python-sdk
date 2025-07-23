# built in packages
import json

def w2g_form_serializer(data, business:dict, submission_id:str='', record_id:str='') -> dict:

    IsForeign       =    bool(data.get('IsForeign'))

    address1        =    data.get('Address1')
    address2        =    data.get('Address2')
    city            =    data.get('City')

    state1          =   data.get('State1')

    return_data = {
        'SequenceId': data.get('SequenceId'),
        'IsPostal': bool(data.get('ReturnDataIsPostal')),
        'IsOnlineAccess': bool(data.get('ReturnDataIsOnlineAccess')),
        'Recipient': {
            'TINType': data.get('TINType'),
            'TIN': data.get('TIN'),
            'FirstPayeeNm': data.get('FirstPayeeNm'),
            'SecondPayeeNm': data.get('SecondPayeeNm'),
            'FirstNm': data.get('FirstNm'),
            'LastNm': data.get('LastNm'),
            'MiddleNm': data.get('MiddleNm'),
            'Suffix': data.get('Suffix'),
            'Email': data['Email'],
            'Fax': data.get('Fax'),
            'Phone': data.get('Phone'),
        },
        'W2GFormData': {
            'B1ReportableWinnings': data.get('B1ReportableWinnings') if data.get('B1ReportableWinnings') else 0,
            'B2DateWon': data.get('B2DateWon1'),
            'B3WagerType': data.get('B3WagerType'),
            'B4FedTaxWH': data.get('B4FedTaxWH') if data.get('B4FedTaxWH') else 0,
            'B5Txn': data.get('B5Txn'),
            'B6Race': data.get('B6Race'),
            'B7WinningsIdWagers': data.get('B7WinningsIdWagers') if data.get('B7WinningsIdWagers') else 0,
            'B8Cashier': data.get('B8Cashier'),
            'B10Window': data.get('B10Window') if data.get('B10Window') else 0,
            'B11FirstId': data.get('B11FirstId'),
            'B12SecondId': data.get('B12SecondId'),
            'States': 
                {
                    'StateCd': state1,
                    'StateIdNum': data.get('Payerstateno1'),
                    'StateWinnings': data.get('StateWinnings') if data.get('StateWinnings') else 0,
                    'StateWH': data.get('StateWH') if data.get('StateWH') else 0,
                    'LocalWinnings': data.get('LocalWinnings') if data.get('LocalWinnings') else 0,
                    'LocalWH': data.get('LocalWH') if data.get('LocalWH') else 0,
                    'LocalityNm': data.get('LocalityNm')
                }
            
        },
    }

    return_data['Recipient']['IsForeign'] = IsForeign
    if IsForeign:
        return_data['Recipient']['ForeignAddress'] = {
            'Address1': address1,
            'Address2': address2,
            'City': city,
            'ProvinceOrStateNm': data.get('ProvinceOrStateNm'),
            'Country': data.get('Country'),
            'PostalCd': data.get('PostalCd')
        }
    else:
        return_data['Recipient']['USAddress'] = {
            'Address1': address1,
            'Address2': address2,
            'City': city,
            'State': data.get('State'),
            'ZipCd': data.get('ZipCd')
        }

    form = {
        'SubmissionManifest': {
            'TaxYear': data.get('TaxYear'),
            'IsFederalFiling': bool(data.get('IsFederalFiling')),
            'IsStateFiling': bool(data.get('IsStateFiling')),
            'IsPostal': bool(data.get('IsPostal')),
            'IsOnlineAccess': bool(data.get('IsOnlineAccess')),
            # 'IsScheduleFiling': bool(data.get('IsScheduleFiling')),
            # 'ScheduleFiling': {
            #     'EfileDate': data.get('EfileDate')
            # }
        },
        'ReturnHeader': { 'Business': business },
        'ReturnData': [return_data]
    }

    if submission_id:
        form['SubmissionManifest']['SubmissionId'] = submission_id

    if record_id:
        form['ReturnData'][0]['RecordId'] = record_id

    return form
