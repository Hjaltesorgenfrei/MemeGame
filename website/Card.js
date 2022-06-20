// Create a class for the element
export class Card extends HTMLElement {
    constructor(text) {
        // Always call super first in constructor
        super();
        // Create a shadow root
        const shadow = this.attachShadow({ mode: 'open' });

        // Create spans
        const wrapper = document.createElement('div');
        wrapper.setAttribute('class', 'light card');

        const info = document.createElement('p');
        info.setAttribute('class', 'text');

        // Take attribute content and put it inside the info span
        text = text ?? this.getAttribute('data-text');
        info.textContent = text;

        const style = document.createElement('link');
        style.setAttribute('rel', 'stylesheet');
        style.setAttribute('href', './style.css');

        // Attach the created elements to the shadow dom
        shadow.appendChild(style);

        shadow.appendChild(wrapper);
        wrapper.appendChild(info);
    }
}