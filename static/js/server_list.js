const socket = io.connect('http://localhost:5000');
socket.emit('trigger server list refresh');
// socket.emit('trigger server list refresh', {'serverName': 'csgo'});
socket.on('server list refresh', serverList => {
    console.log('server list refresh', serverList);
    const serverListElement = document.querySelector('#server-list');
    serverListElement.innerHTML = '';
    serverList.forEach(server => { 
        const serverElement = document.createElement('div');
        serverElement.classList.add('server-item'); 
        serverElement.textContent = server['serverName'] + ' (' + server['status'] + ')';
        serverListElement.append(serverElement);
    });
});

document.querySelector('#btn-create-server').addEventListener('click', () => {
    window.location.href = '/create';
});