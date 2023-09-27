from django.contrib import messages


# method to arrange data from request POST obj to python dictionary
def business_form_serializer(data):
    form = {}

    form['BusinessNm']             = data.get('BusinessNm')
    form['PayerRef']               = data.get('PayerRef')
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
    
    form['SigningAuthority'] = {}
    form['SigningAuthority']['Name'] = data.get('SigningAuthorityName')
    form['SigningAuthority']['Phone'] = data.get('SigningAuthorityPhone')
    form['SigningAuthority']['BusinessMemberType'] = data.get('BusinessMemberType')

    form['IsForeign']              = True if data.get('isForeign') else False

    address1                       = data.get('Address1')
    address2                       = data.get('Address2')
    city                           = data.get('City')

    if form['IsForeign']:

        form['ForeignAddress'] = {}
        form['ForeignAddress']['Address1']          = address1
        form['ForeignAddress']['Address2']          = address2
        form['ForeignAddress']['City']              = city
        form['ForeignAddress']['ProvinceOrStateNm'] = data.get('ProvinceOrStateNm')
        form['ForeignAddress']['Country']           = data.get('Country')
        form['ForeignAddress']['PostalCd']          = data.get('PostalCd')

    else:

        form['USAddress'] = {}
        form['USAddress']['Address1']               = address1
        form['USAddress']['Address2']               = address2
        form['USAddress']['City']                   = city
        form['USAddress']['State']                  = data.get('State')
        form['USAddress']['ZipCd']                  = data.get('ZipCd')
    
    return form

# this will show some error messages in web page if error occurs
def do_alerts(request, res_json):
    
    success = 'StatusCode' in res_json and res_json['StatusCode'] == 200
    if not success:
        
        msg_exist = 'StatusMessage' in res_json and res_json['StatusMessage']
        if msg_exist:
            messages.error(request, f'{res_json["StatusMessage"]}', extra_tags='danger')