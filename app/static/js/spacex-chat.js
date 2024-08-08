import '../node_modules/typeit/dist/index.umd.js';

import ax3Common from './helpers/common.js';
import { ax3GetCookie } from './helpers/cookies.js';

ax3Common(Alpine => {
    const videoBG = document.querySelector('.js-video-bg');
    const csrfToken = ax3GetCookie('csrftoken');

    Alpine.store('steps', {
        active: 1,
        bgVideoStatus: 'normal',
        showIntro: true,
        showChat: false,
        showTicket: false,
        loadingText: '',
        nextStep() {
            this.active++;
        },
        toggleVideo(play, zoom) {
            if (play) {
                videoBG.play();
            } else {
                videoBG.pause();
            }

            this.bgVideoStatus = zoom ? 'zoom' : 'normal';
        },
        loadChat() {
            this.nextStep();
            this.toggleVideo(false, true);
            this.showIntro = false;
            this.showChat = true;

            setTimeout(() => {
                Alpine.store('chat').initChat();
            }, 1000);
        },
        sendingData(loadingText) {
            this.toggleVideo(true, false);
            this.showChat = false;
            this.loadingText = loadingText;
        },
        resultData() {
            this.nextStep();
            this.toggleVideo(false, true);
            this.showChat = true;
            this.loadingText = '';
        },
        revealTicket() {
            this.sendingData('Processing your payment...');

            setTimeout(() => {
                this.nextStep();
                this.showTicket = true;
                this.showChat = true;
                this.toggleVideo(true, true);
                this.loadingText = '';
            }, 3000);
        },
    });

    Alpine.store('chat', {
        list: [],
        messages: [],
        blockInput: true,
        goBottom() {
            const chatContent = document.querySelector('.js-chat-content');
            setTimeout(() => {
                chatContent.scrollTop = chatContent.scrollHeight;
            }, 100);
        },
        newLine(text) {
            this.blockInput = true;

            this.list.push({
                id: this.list.length,
                is: 'person',
                name: 'Me',
                text: text,
            });

            this.messages.push({
                role: 'user',
                message: text,
            });

            htmx.ajax('POST', CHAT_URL, {
                source: '.js-form-chat',
                swap: 'none',
                indicator: false,
                boost: false,
                headers: {
                    'X-CSRFToken': csrfToken,
                },
                values: {
                    messages: JSON.stringify(this.messages),
                },
            });

            this.goBottom();
        },
        nextQuestion(text) {
            this.messages.push({
                role: 'assistant',
                message: text,
            });

            this.list.push({
                id: this.list.length,
                is: 'robot',
                name: 'Apollo',
                text: text,
            });

            this.goBottom();
        },
        animatedText(element, text) {
            const chatContent = document.querySelector('.js-chat-content');

            new TypeIt(element, {
                strings: text,
                speed: 50,
                cursor: false,
                afterStep: () => {
                    chatContent.scrollTop = chatContent.scrollHeight;
                },
                afterComplete: () => {
                    this.blockInput = false;
                },
            }).go();
        },
        initChat() {
            this.nextQuestion(START_QUESTION);
        },
    });

    htmx.on('htmx:afterRequest', event => {
        if (event.detail.elt.classList.contains('js-form-chat')) {
            if (event.detail.xhr.response.includes('next_question')) {
                const response = JSON.parse(event.detail.xhr.response);
                Alpine.store('chat').nextQuestion(response.next_question);
            } else {
                Alpine.store('steps').sendingData('Calculating your score...');

                setTimeout(() => {
                    document.querySelector('#response-content').outerHTML =
                        event.detail.xhr.response;
                }, 1000);

                setTimeout(() => {
                    Alpine.store('steps').resultData();
                }, 2000);
            }
        }
    });
});
