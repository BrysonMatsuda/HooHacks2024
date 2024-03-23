var socket = io();
var mediaRecorder;
var isRecording = false;

document.getElementById('recordButton').addEventListener('click', function () {
    if (!isRecording) {
        navigator.mediaDevices.getUserMedia({ audio: true })
            .then(stream => {
                mediaRecorder = new MediaRecorder(stream);
                var chunks = []; // Array to store recorded audio chunks

                mediaRecorder.ondataavailable = event => {
                    chunks.push(event.data); // Push each chunk to the array
                };

                mediaRecorder.onstop = () => {
                    // Concatenate all audio chunks into a single Blob
                    var audioBlob = new Blob(chunks, { type: 'audio/wav' });

                    // Reset chunks array for the next recording
                    chunks = [];

                    // Send the Blob to the server
                    socket.emit('audio_chunk', audioBlob);

                    // Reset the recording button text and flag
                    isRecording = false;
                    document.getElementById('recordButton').innerText = 'Start Recording';
                };

                // Start recording
                mediaRecorder.start();

                // Update button text and flag
                isRecording = true;
                document.getElementById('recordButton').innerText = 'Stop Recording';
            })
            .catch(error => {
                console.error('Error accessing microphone:', error);
            });
    } else {
        // Stop recording
        mediaRecorder.stop();
        socket.emit('recording_stopped')
    }
});
