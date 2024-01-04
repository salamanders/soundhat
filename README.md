Goal: A rpi pico that shows lights depending on what sounds a nearby phone is hearing.

To do this, connect from the phone to the pico over Web Bluetooth API, and send sound data 
(or maybe do a FFT on the phone then control the lights.)

Writeup: https://docs.google.com/document/d/1X-AS-IZy4wcI4Rrj5N0C0mMkiRyhzIJiDVzRC08NEgA/edit?usp=sharing

# Notes
* https://developer.mozilla.org/en-US/docs/Web/API/Web_Bluetooth_API
* https://developer.mozilla.org/en-US/docs/Web/API/AnalyserNode
* https://www.espruino.com/About+Bluetooth+LE#128-bit-uuids
