const dgram = require('dgram');
const express = require('express');
const app = express();
const bodyParser = require('body-parser');
const yaml = require('js-yaml');
const fs = require('fs');

const web_server_port = 3000
const logging_server_local_port = 3001

const control_server_local_port = 3002
const control_server_remote_port = 4002

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

const version = process.env.npm_package_version
console.log(version)

// UDP Log Server
let log_buffer = []
const max_logs = 200

const logging_server = dgram.createSocket('udp4');
logging_server.on('message', (msg) => {
  log_buffer.unshift(JSON.parse(msg.toString('utf-8')))
  if (log_buffer.length > max_logs)
    log_buffer.pop()
});
logging_server.bind(logging_server_local_port);

// UDP port for receiving commands
control_data = {}
const control_server = dgram.createSocket('udp4');
control_server.on('message', (msg) => {
  msg = JSON.parse(msg.toString('utf-8'))
  for (key in msg) {
    control_data[key] = msg[key]
  }
});
control_server.bind(control_server_local_port);


// UDP client for sending commands
const command_client = dgram.createSocket('udp4')

// Web server
app.use(bodyParser.json()); // for parsing application/json
app.use(express.static(__dirname));

app.get('/logs', function (req, res) {
  res.send(log_buffer)
});

app.post('/logs_clear', function (req, res) {
  log_buffer = [];
  res.send('done');
});

app.get('/control', function(req, res) {
  res.send(control_data)
});

app.post('/control', function (req, res) {
  const msg = new Buffer(JSON.stringify(req.body))
  command_client.send(msg, 0, msg.length, control_server_remote_port,
      'localhost', (err, bytes) => {
    if (err) {
      console.log(err)
      res.status(500).send(err);
    } else {
      res.send('done')
    }
  });
});

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
    //server.send(JSON.stringify(req.body), udp_port_out, sender_ip);
  }
  res.send();
});

app.listen(web_server_port, function () {
    console.log('HTTP server on port ' + web_server_port);
});
