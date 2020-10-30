
var net = require('net')
var sock 

var server = net.createServer(function(socket) {
	sock = socket
	request = {}
	request.method = 'RPC'
	sock.write(JSON.stringify(request));
	sock.pipe(sock);
	sock.on('data', function(data) {
		console.log('Received: ' + data);
	});
});

console.log('start listen...')
server.listen(10000, '127.0.0.1');

