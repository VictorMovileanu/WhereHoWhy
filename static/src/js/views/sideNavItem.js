import {elements} from "./base";

export const populateMain = function (el) {
    const markup = `
        <div class="main-content fadein">
            ${el.innerHTML}
        </div>
    `;

    if (elements.main.children.length) {
        elements.main.childNodes.forEach(el => {
            $(el).removeClass("fadein");
            $(el).addClass("fadeout")
        });
        setTimeout(() => {
            elements.main.innerHTML = markup;
        }, 1200)
    } else {
        elements.main.innerHTML = markup;
    }
};