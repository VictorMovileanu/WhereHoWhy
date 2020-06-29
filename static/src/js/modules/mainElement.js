import {elements} from "../elements";

export const show = function () {
    $(elements.main).addClass('show');
};


export const populateFrom = function (el) {
    const markup = `
        <div class="main-content fadein">
            ${el.innerHTML}
        </div>
    `;

    elements.main.innerHTML = markup;
};

export const hide = function (callback) {
    if (elements.main.children.length) {
        elements.main.childNodes.forEach(el => {
            $(el).removeClass("fadein");
            $(el).addClass("fadeout")
        });
    }
    setTimeout(() => {
        elements.main.innerHTML = null;
        $(elements.main).removeClass('show');
        callback();
    }, 1200)
};