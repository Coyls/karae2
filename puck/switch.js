var noble = require('@abandonware/noble');
const WebSocket = require('ws');

// List of allowed devices
const devices = [
  "d2:7e:fe:88:e2:a3"
];
// last advertising data received
var lastAdvertising = {
};

const ws = new WebSocket("ws://localhost:8000");

const protocolGenerator = (key, value) => {
  return `/${key}:${value}`
}


ws.addEventListener('open', function (event) {
  ws.send(protocolGenerator("name","switch"));
});

function onDeviceChanged(addr, data) {
  console.log("Device ",addr,"changed data",JSON.stringify(data));
  ws.send(protocolGenerator("switch", "1"));
}

function onDiscovery(peripheral) {
  // do we know this device?
  if (devices.indexOf(peripheral.address)<0) return;
  // does it have manufacturer data with Espruino/Puck.js's UUID
  if (!peripheral.advertisement.manufacturerData ||
      peripheral.advertisement.manufacturerData[0]!=0x90 ||
      peripheral.advertisement.manufacturerData[1]!=0x05) return;
  // get just our data
  var data = peripheral.advertisement.manufacturerData.slice(2);
  // check for changed services
  if (lastAdvertising[peripheral.address] != data.toString())
    onDeviceChanged(peripheral.address, data);
  lastAdvertising[peripheral.address] = data;
}

noble.on('stateChange',  function(state) {
  if (state!="poweredOn") return;
  console.log("Starting scan...");
  noble.startScanning([], true);
});
noble.on('discover', onDiscovery);
noble.on('scanStart', function() { console.log("Scanning started."); });
noble.on('scanStop', function() { console.log("Scanning stopped.");});