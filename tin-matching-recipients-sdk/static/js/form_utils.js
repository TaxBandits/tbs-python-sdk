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
        document.getElementById(selectTagId).value = value
    }
}

function remove_valid_options(selectTagId){

    var selectTag = document.getElementById(selectTagId)

    Array.from(selectTag.options).forEach((opt_tag, idx)=>{
        console.log('opt_tag', [opt_tag], idx);
        if(idx){
            $(opt_tag).remove()
        }
    })
}