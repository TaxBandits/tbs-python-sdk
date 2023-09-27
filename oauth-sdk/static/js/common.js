let copy_text_to_clipboard = (id, callBack) => {

    var textTag = document.getElementById(id)
    console.log('textTag', textTag);
    var text = textTag.innerText

    var elem = document.createElement("textarea");
    document.body.appendChild(elem);
    elem.value = text;
    elem.select();

    try {
        var copiedOrNot = document.execCommand('copy');
        callBack(copiedOrNot)
    } catch (err) {
        console.log('Oops, unable to copy');
    }

    document.body.removeChild(elem);

}