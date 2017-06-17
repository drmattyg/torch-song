const dgram = require('dgram');
const server = dgram.createSocket('udp4');
const express = require('express');
const app = express();
const bodyParser = require('body-parser');
const net = require('net');
const yaml = require('js-yaml');
const fs = require('fs');

const readYAML = function(filename, cb) {
  fs.readFile(filename, 'utf8', function(err, file) {
    if (err) {
      cb(err)
    }
    else {
      cb(null, yaml.safeLoad(file));
    }
  });
};

const writeYAML = function(filename, obj, cb) {
  fs.writeFile(filename, yaml.safeDump(obj), function(err) {
    cb(err)
  });
};


const logging_server = net.createServer((socket) => {
  socket.on('data', (data) => {
    console.log(data.toString('utf8'))
  });

});
logging_server.listen(4000, 'localhost');

const version = process.env.npm_package_version
console.log(version)

var dbw_state = {}
const udp_port_in = 11301;
const udp_port_out = 11300;
const http_port = 3000;

var sender_ip;

// UDP
server.on('error', (err) => {
    console.log(`server error:\n${err.stack}`);
      server.close();
});

server.on('message', (msg, rinfo) => {
  sender_ip = rinfo.address;
  dbw_state = JSON.parse(msg.toString());
});

server.on('listening', () => {
  var address = server.address();
  console.log(`server listening ${address.address}:${address.port}`);
});

server.bind(udp_port_in);


// Web server
app.use(bodyParser.json()); // for parsing application/json
app.use(express.static(__dirname));

app.get('/default-yaml', function (req, res) {
  readYAML('../conf/default.yml', function(err, yaml) {
    if (err) {
      console.log(err);
      res.status(404).send('Not found');
    } else {
      res.send(yaml);
    }
  });
});

app.get('/default-mod-yaml', function (req, res) {
  readYAML('../conf/default-mod.yml', function(err, yaml) {
    if (err) {
      readYAML('../conf/default.yml', function(err, default_yaml) {
        if (err) {
          console.log(err);
          res.status(404).send('Not found');
        } else {
          res.send(default_yaml);
        }
      });
    } else {
      res.send(yaml);
    }
  });
});

app.post('/default-mod-yaml', function (req, res) {
  writeYAML('../conf/default-mod.yml', req.body, function(err) {
    if (err) {
      console.log(err);
      res.status(500).send(err);
    } else {
      res.send('done');
    }
  });
});


// Send state
app.post('/post', function(req, res) {
  if (sender_ip) {
    server.send(JSON.stringify(req.body), udp_port_out, sender_ip);
  }
  res.send();
});

app.listen(http_port, function () {
    console.log('HTTP server on port ' + http_port);
});
