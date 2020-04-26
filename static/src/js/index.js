import { elements } from "./views/base";

elements.sideNavItems.forEach(el => el.addEventListener('click', e => {
    console.log("Hello Item!")
}));