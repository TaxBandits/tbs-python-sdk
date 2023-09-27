function remove_valid_options(selectTag){
    console.log('tr in remove_value_options', [selectTag]);

    Array.from(selectTag.options).forEach((opt_tag, idx)=>{
        console.log('opt_tag', [opt_tag], idx);
        if(idx){
            $(opt_tag).remove()
        }
    })
}

function set_options_to_selectTag(selectTag, labelObj, valueObj){

    Object.keys(labelObj).forEach(key=>{

        var label = labelObj[key]
        var value = valueObj ? valueObj[key] : label
        
        selectTag.options.add( new Option(label, value) );
    })
}

function find_key_by_value(object, value){
    return Object.keys(object).find(key => object[key] === value);
}

// let ajax_fun = (post_data, method, successCB) => {
//     var options = {
//         method: method,
//         headers: {
//             'Content-Type': 'application/json'
//         }
//     }
// }
