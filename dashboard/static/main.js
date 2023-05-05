let urls = document.querySelector('#urls');
let name_val = document.querySelector('#first_name');
let namee = document.querySelector('#namee');
let photos = document.querySelector('.photos');

name_val.onkeyup = () => {
    namee.textContent = name_val.value;
}
urls.onkeyup = () => {
    photos.innerHTML = ''
    let url = urls.value;
    let links = url.split('/*/');
    links.forEach(link => {
        let xd = document.createElement('img');
        xd.src = link;
        photos.appendChild(xd);
    });
    console.log(links)
}