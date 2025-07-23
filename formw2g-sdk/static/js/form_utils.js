function set_options_to_selectTag(selectTagId, labelObj, valueObj){

    var selectTag = document.getElementById(selectTagId)

    Object.keys(labelObj).forEach(key=>{

        var label = labelObj[key]
        var value = valueObj ? valueObj[key] : label
        
        selectTag.options.add( new Option(label, value) );
    })
}

function select_option_for_selectTag(selectTagId, value){
    if(value){
        setTimeout(()=>{
            document.getElementById(selectTagId).value = value
        }, select_option_time)
    }
}

function remove_valid_options(selectTagId){

    var selectTag = document.getElementById(selectTagId)

    Array.from(selectTag.options).forEach((opt_tag, idx)=>{
        if(idx){
            $(opt_tag).remove()
        }
    })
}

function twoWayBindForSameNameInputs(form_id, input_tag){
    
    var name_val = $(input_tag).attr('name')
    var input_tags = $('#'+form_id).find('[name="'+name_val+'"]')

    input_tags.val(input_tag.value)

}

function setValueInInput(form_id, name_val, value){
    $('#'+form_id).find('[name="'+name_val+'"]').val(value)
}