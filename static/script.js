let socket = io();

function startRecording() {
    console.log("Start recording...");
    socket.emit('speech_request', { audioData: "Your captured audio data here" });
    socket.on('speech_response', function (data) {
        console.log("Received text:", data.text);
    });
}