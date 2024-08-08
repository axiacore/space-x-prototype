import '../../node_modules/htmx.org/dist/htmx.min.js';
import Alpine from '../../node_modules/alpinejs/dist/module.esm.js';

function ax3Common(callback = undefined) {
    if (callback) callback(Alpine);
    if (!window.Alpine) {
        window.Alpine = Alpine;
        Alpine.start();
    }

    const CLIENT_ERROR_STATUS_CODE = '4';
    const SERVER_ERROR_STATUS_CODE = '5';

    window.htmx.on('htmx:responseError', event => {
        const xhr = event.detail.xhr;
        const initialNumberStatus = xhr.status.toString().charAt(0);

        if (initialNumberStatus === CLIENT_ERROR_STATUS_CODE) {
            alert(`Client error ${xhr.status}: ${xhr.responseURL}`);
            window.location.reload();
        } else if (initialNumberStatus === SERVER_ERROR_STATUS_CODE) {
            alert(`Server error ${xhr.status}: ${xhr.responseURL}`);
            window.location.reload();
        }
    });
}

export default ax3Common;
