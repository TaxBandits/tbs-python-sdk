# method to arrange data from request POST obj to python dictionary
def business_form_serializer(data) -> dict:
    form = {}

    form['BusinessNm']             = data.get('BusinessNm')
    form['PayerRef']               = data.get('PayerRef')
    form['FirstNm']             = data.get('FirstNm')
    form['MiddleNm']             = data.get('MiddleNm')
    form['LastNm']             = data.get('LastNm')
    form['Suffix']             = data.get('Suffix')
    form['TradeNm']                = data.get('TradeNm')
    form['IsEIN']                  = True if data.get('IsEIN') else False
    form['EINorSSN']               = data.get('EINorSSN')
    form['Email']                  = data.get('Email')
    form['ContactNm']              = data.get('ContactNm')
    form['Phone']                  = data.get('Phone')
    form['PhoneExtn']              = data.get('PhoneExtn')
    form['Fax']                    = data.get('Fax')
    form['BusinessType']           = data.get('BusinessType')
    form['KindOfEmployer']         = data.get('KindOfEmployer')
    form['KindOfPayer']            = data.get('KindOfPayer')
    form['IsBusinessTerminated']   = False
    
    form['SigningAuthority'] = {
        'Name': data.get('SigningAuthorityName'),
        'Phone': data.get('SigningAuthorityPhone'),
        'BusinessMemberType': data.get('BusinessMemberType')
    }

    form['IsForeign']              = bool(data.get('isForeign'))

    address1                       = data.get('Address1')
    address2                       = data.get('Address2')
    city                           = data.get('City')

    if form['IsForeign']:

        form['ForeignAddress'] = {
            'Address1': address1,
            'Address2': address2,
            'City': city,
            'ProvinceOrStateNm': data.get('ProvinceOrStateNm'),
            'Country': data.get('Country'),
            'PostalCd': data.get('PostalCd')
        }

    else:

        form['USAddress'] = {
            'Address1': address1,
            'Address2': address2,
            'City': city,
            'State': data.get('State'),
            'ZipCd': data.get('ZipCd')
        }
    
    return form
