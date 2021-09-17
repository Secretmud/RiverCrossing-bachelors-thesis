import paths from "./paths.js";
const path_anchor = document.getElementById("anchor");
const content = document.getElementById("content"); 
function render() {
    for (let i = 0; i < Object.keys(paths).length; i++) {
        const dataContent = [paths[i].id,
                             paths[i].location,
                             paths[i].name];
        var div = document.createElement("div");
        div.classList.add("link");
        div.innerHTML = `
        <button id="${dataContent[0]}" name="${dataContent[1]}">${dataContent[2]}</button>
        `;
        div.addEventListener('click', () => {
            console.log(`HEI! ${dataContent[1]}`)
            content.src = dataContent[1];

        });
        path_anchor.appendChild(div);
    }
}


window.onload = function() {
    render();
}
