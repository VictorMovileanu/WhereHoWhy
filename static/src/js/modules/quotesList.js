import {elements} from "../elements";

export const hide = function (callback) {
    $(elements.quotesList).addClass('fadeout');
    $(elements.quotesList).removeClass('fadein');
    setTimeout(() => {
        callback();
    }, 1200)
};

export const show = function () {
    $(elements.quotesList).addClass('fadein');
    $(elements.quotesList).removeClass('fadeout');
};
