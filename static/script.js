var socket = io();
var mediaRecorder;
var isRecording = false;

document.getElementById('recordButton').addEventListener('click', function () {
    if (!isRecording) {
        navigator.mediaDevices.getUserMedia({ audio: true })
            .then(stream => {
                mediaRecorder = new MediaRecorder(stream);

                mediaRecorder.start();
                isRecording = true;
                document.getElementById('recordButton').innerText = 'Stop Recording';

                mediaRecorder.ondataavailable = event => {
                    if (isRecording) {
                        event.data.arrayBuffer().then(buffer => socket.emit('audio_chunk', buffer));
                    }
                };
            });
    } else {
        mediaRecorder.stop();
        isRecording = false;
        document.getElementById('recordButton').innerText = 'Start Recording';
        socket.emit('recording_stopped');
    }
});