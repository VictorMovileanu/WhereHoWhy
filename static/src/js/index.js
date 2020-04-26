import { elements } from "./views/base";
import * as sideNavItem from "./views/sideNavItem"

elements.sideNavItems.forEach(el => el.addEventListener('click', e => {
    sideNavItem.populateMain(el)
}));