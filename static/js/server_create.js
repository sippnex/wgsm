const socket = io.connect('http://localhost:5000');

document.querySelector('#form-action-cancel').addEventListener('click', () => {
    window.location.href = '/list';
});

document.querySelector('#form-action-submit').addEventListener('click', () => {
    socket.emit('action server create', {'serverName': document.querySelector('#form-control-server-name').value});
    window.location.href = '/list';
});