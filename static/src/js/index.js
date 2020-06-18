import { elements } from "./views/base";
import * as sideNavItem from "./views/sideNavItem"

elements.quotesListItems.forEach(el => el.addEventListener('click', e => {
    $(elements.quotesList).addClass('d-none');
    sideNavItem.populateMain(el)
}));