# built in packages
import json


# method to arrange the requests json string to format as per our need
def tin_match_request_form_serializer(data, business_id) -> dict:
    
    array_of_data = data.get('ArrayOfData')
    tin_request_data = json.loads(array_of_data)

    ret_dict = {
        "TINMatchingDetails": {
            "Business": {
                "BusinessId": business_id,
                "TIN": None
            }
        }
    }

    recipient_list = []
    for rdata in tin_request_data:

        recipient_list.append({
            "SequenceId": rdata.get('seqId'),
            "RecipientId": None,
            "Name": rdata.get('name'),
            "TINType": rdata.get('tinType'),
            "TIN": rdata.get('tinValue')
        })

    ret_dict["TINMatchingDetails"]["Recipients"] = recipient_list

    return ret_dict