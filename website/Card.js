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

        const style = document.createElement('style');

        style.textContent = `
        /* https://codepen.io/jefflombard/pen/GqBzxe */
        .card {
            /* Card Sizing */
            font-family: Helvetica, sans-serif;
            font-weight: bolder;
            font-size: 22px;
            flex: 1;
            width: 8em;
            height: 10em;
            border-radius: .25in;

            /* Display Properties */
            margin: 10px;
        }

        .dark {
            /* Color information */
            border: 3px solid black;
            color: white;
            background: black;
        }

        .light {
            /* Color information */
            border: 3px solid black;
            color: black;
            background: white;
        }

        .text {
            /*font information*/
            padding-left: 7%;
            padding-right: 7%;
            word-wrap: break-word;
        }
        `;

        // Attach the created elements to the shadow dom
        shadow.appendChild(style);

        shadow.appendChild(wrapper);
        wrapper.appendChild(info);
    }
}