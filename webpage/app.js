/*jshint esversion: 9 */

/** @type {string} */
const HAT_SERVICE_UUID = '8d8bbe55-f9c9-4436-8541-c26ea243dbae';
/** @type {string} */
const HAT_CHAR_UUID_WRITE = '05839cfc-5d02-4daa-80d9-82303b98f7fc';
const ENC = new TextEncoder(); // always utf-8

async function connectToDevice() {
  try {
    console.groupCollapsed('BLE');
    console.info('Requesting Bluetooth Device...');
    const device = await navigator.bluetooth.requestDevice({
      filters: [{ name: 'sound-hat' }],
      optionalServices: [HAT_SERVICE_UUID]
    });
    console.info(device);

    console.info('Connecting to GATT Server...');
    const server = await device.gatt.connect();
    console.info(server);

    const primaryService = await server.getPrimaryService(HAT_SERVICE_UUID);
    console.info(primaryService);

    // https://googlechrome.github.io/samples/web-bluetooth/discover-services-and-characteristics.html
    primaryService.getCharacteristics().then(characteristics => {
      console.info('Service: ' + primaryService.uuid);
      console.groupCollapsed();
      characteristics.forEach(characteristic => {
        console.log('Characteristic: ' + characteristic.uuid + ' ' + Object.entries(characteristic.properties)
          .filter(([key, value]) => value === true)
          .map(([key, value]) => key.toUpperCase())
          .join(', '));
      });
      console.groupEnd();
    });
    console.groupEnd();

    return primaryService.getCharacteristic(HAT_CHAR_UUID_WRITE);
  } catch (error) {
    console.error('Error:', error);
  } finally {
    console.info('connectToDevice:finally');
  }
}

async function sendMessage(writeableCharacteristic, message) {
  const encodedMessage = ENC.encode(message);
  console.info("About to write info", encodedMessage);
  const response = await writeableCharacteristic.writeValueWithResponse(encodedMessage);
  console.info("Finished writeValueWithResponse", response);
}

if (await navigator.bluetooth.getAvailability()) {
  console.info("This device supports Bluetooth! Adding click events.");
  document.getElementById("ble-start").addEventListener('click', async () => {
    const lightController = await connectToDevice();
    console.info("Got the writeable characteristic", lightController);

    document.getElementById("light-on").addEventListener('click', async () => {
      await sendMessage(lightController, 'l:on');
    });
    document.getElementById("light-off").addEventListener('click', async () => {
      await sendMessage(lightController, 'l:off');
    });
  });
} else {
  alert("Bluetooth is not supported");
  console.error("Bluetooth is not supported");
}


