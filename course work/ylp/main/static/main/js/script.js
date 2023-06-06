function dropdown(){
    const dropdown_menu = document.getElementById("dropdown-menu");
    if (dropdown_menu.style.display === "none"){
        dropdown_menu.style.display = "block";
    }
    else{
        dropdown_menu.style.display = "none";
    }
}

window.onclick = function (event){
    if (!event.target.matches('.menubtn')) {
        const menu = document.getElementById('dropdown-menu');
        menu.style.display = 'none';

    }
}

function filters(){
    const _for = document.getElementsByName("for");
    const types = document.getElementsByName("type");
    const groups = document.getElementsByName("group");
    const country = document.getElementsByName("country");
    let url = "http://127.0.0.1:8000/main/container/";
    let item_for = '';
    let item_group = '';
    let item_types = '';
    let item_country = '';
    let item_price_from = document.getElementsByName("price-from")[0].value;
    let item_price_to = document.getElementsByName("price-to")[0].value;
    let params = '';
    for (let i = 0; i < _for.length; i++){
        if (_for[i].checked) {
            item_for += _for[i].value + ';';
        }
    }
    for (let i = 0; i < groups.length; i++){
        if (groups[i].checked) {
            item_group += groups[i].value + ';';
        }
    }
    for (let i = 0; i < types.length; i++){
        if (types[i].checked) {
            item_types += types[i].value + ';';
        }
    }
    for (let i = 0; i < country.length; i++){
        if (country[i].checked) {
            item_country += country[i].value + ';';
        }
    }
    if (item_for.length){
        item_for = 'for=' + item_for.slice(0, -1) + '&';
        params = params + item_for;
    }
    if (item_group.length){
        item_group = 'group=' + item_group.slice(0, -1) + '&';
        params = params + item_group;
    }
    if (item_types.length){
        item_types = 'type=' + item_types.slice(0, -1) + '&';
        params = params + item_types;
    }
    if (item_country.length){
        item_country = 'country=' + item_country.slice(0, -1) + '&';
        params = params + item_country;
    }
    if (item_price_from.length){
        item_price_from = 'price-from=' + item_price_from + '&'
        params = params + item_price_from;
    }
    if (item_price_to.length){
        item_price_to = 'price-to=' + item_price_to;
        params = params + item_price_to + '&';
    }
    if (params.length){
        params = '?' + params
        params = params.slice(0, -1)
    }
    url = url + params
    window.location.replace(url)
}

function sort(elem){
    let url_string = window.location.href
    let url = new URL(url_string)
    const sorting = elem.value
    url.searchParams.set('sort', sorting)
    window.location.replace(url)
}

function previous_photo(){
    let url = new URL(window.location.href)
    let photo_num = url.searchParams.get('photo')
    if (!photo_num){
        photo_num = 1
    }
    else {
        photo_num = parseInt(photo_num)
    }
    if (photo_num > 0){
        photo_num -= 1
    }
    url.searchParams.set('photo', photo_num.toString())
    window.location.replace(url)
}

function next_photo(len){
    let url = new URL(window.location.href)
    let photo_num = url.searchParams.get('photo')
    if (!photo_num){
        photo_num = 0
    }
    else {
        photo_num = parseInt(photo_num)
    }
    if (photo_num < len - 1){
        photo_num += 1
    }
    url.searchParams.set('photo', photo_num.toString())
    window.location.replace(url)
}