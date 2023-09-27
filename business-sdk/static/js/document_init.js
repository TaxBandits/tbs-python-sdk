$(()=>{
    console.log('tr in ready');

    setTimeout(()=>{
        message_remover()
    }, 6000);
})

function message_remover(){
    console.log('tr in message_remover');

    message_tags = document.getElementsByClassName('django-messages')

    if(message_tags){
        Array.from(message_tags).forEach(mt=>{
            if(mt){
                mt.classList.remove('show')
            }
        })
    }
}


function assign_constants(){
    console.log('tr in assign_constants');
    selectBusinessType = document.getElementById('selectBusinessType')

    set_options_to_selectTag(
        selectBusinessType, 
        businessType, 
        businessTypeShorts
    )


    selectKindOfEmployer = document.getElementById('selectKindOfEmployer')

    set_options_to_selectTag(
        selectKindOfEmployer, 
        kindOfEmployer
    )


    selectKindOfPayer = document.getElementById('selectKindOfPayer')

    set_options_to_selectTag(
        selectKindOfPayer, 
        kindOfPayer
    )


    selectState = document.getElementById('selectState')

    set_options_to_selectTag(
        selectState, 
        states,
        statesShort
    )

    selectCountry = document.getElementById('selectCountry')

    set_options_to_selectTag(
        selectCountry, 
        countries,
        countryShorts
    )

}