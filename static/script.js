var socket = io();
var mediaRecorder;
var isRecording = false;
var chunks = []; // Array to store recorded audio chunks

document.getElementById('recordButton').addEventListener('click', function () {
    response_text = document.getElementById('textPlaceholder')
    if (!isRecording) {
        navigator.mediaDevices.getUserMedia({ audio: true })
            .then(stream => {
                mediaRecorder = new MediaRecorder(stream);

                mediaRecorder.ondataavailable = event => {
                    chunks.push(event.data); // Push each chunk to the array
                };

                mediaRecorder.onstop = () => {
                    var audioBlob = new Blob(chunks, { type: 'audio/webm' });

                    // Prepare FormData
                    var formData = new FormData();
                    formData.append('audio_data', audioBlob, 'recording.webm');

                    // Send the audio file to the server using fetch API
                    fetch('/upload_audio', {
                        method: 'POST',
                        body: formData,
                    }).then(response => {
                        return response.text();
                    }).then(text => {
                        console.log('Server response:', text);
                        response_text.innerText = "You said: " + text;
                    }).catch(error => {
                        console.error('Error sending audio to server:', error);
                    });

                    chunks = [];
                    isRecording = false;
                    document.getElementById('recordButton').innerText = 'Start Recording';

                    if (mediaRecorder.stream) {
                        mediaRecorder.stream.getTracks().forEach(track => track.stop());
                    }
                };

                mediaRecorder.start();

                isRecording = true;
                document.getElementById('recordButton').innerText = 'Stop Recording';
            })
            .catch(error => {
                console.error('Error accessing microphone:', error);
            });
    } else {
        mediaRecorder.stop();
        document.getElementById('recordButton').innerText = 'Start Recording';
    }
});

socket.on('connect_error', (error) => {
    console.error('Socket connection error:', error);
});

socket.on('connect_timeout', () => {
    console.error('Socket connection timeout.');
});
