function ax3GetCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = decodeURIComponent(document.cookie).split(';');
        for (const item of cookies) {
            const cookie = item.trim();
            if (cookie.substring(0, name.length + 1) === `${name}=`) {
                cookieValue = cookie.substring(name.length + 1);
                break;
            }
        }
    }
    return cookieValue;
}

function ax3SetCookie(name, value, days) {
    let expires = '';
    if (days) {
        const date = new Date();
        date.setTime(date.getTime() + days * 24 * 60 * 60 * 1000);
        expires = `;·expires=${date.toUTCString()}`;
    }
    document.cookie = `${name}=${value}${expires}; path=/`;
}

export { ax3GetCookie, ax3SetCookie };
