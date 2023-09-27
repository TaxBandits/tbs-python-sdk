$(()=>{
    console.log('tr in ready');
    setTimeout(() => {
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

