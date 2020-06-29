import {elements, elementStrings} from "./elements";
import * as quotesList from "./modules/quotesList"
import * as mainElement from "./modules/mainElement"

elements.quotesListItems.forEach(el => el.addEventListener('click', e => {
    // hide the side nav with the quotes list
    quotesList.hide(function () {
        // display and populate the the main element with content
        mainElement.show();
        mainElement.populateFrom(el)
    });
}));

$(window).click(function (evt) {
    // if the click is outside of the main content, and not a quote list item,
    // hide the main content and display the sidebar
    if (evt.target.className !== elementStrings.quotesListItem) {
        mainElement.hide(quotesList.show);
    }
});

$(elements.mainContent).click(function (event) {
    event.stopPropagation();
});