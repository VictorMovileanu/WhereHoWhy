import {elements} from "./base";

export const populateMain = function (el) {
    const markup = `
        <div class="main-content fadein">
            ${el.innerHTML}
        </div>
    `;
};