var socket = io();
var mediaRecorder;
var isRecording = false;
var chunks = []; // Array to store recorded audio chunks

document.getElementById('recordButton').addEventListener('click', function () {
    if (!isRecording) {
        navigator.mediaDevices.getUserMedia({ audio: true })
            .then(stream => {
                mediaRecorder = new MediaRecorder(stream);

                mediaRecorder.ondataavailable = event => {
                    chunks.push(event.data); // Push each chunk to the array
                };

                mediaRecorder.onstop = () => {
                    // Create a new Blob with all the audio chunks
                    var audioBlob = new Blob(chunks, { type: 'audio/webm' });

                    // Create a URL for the Blob
                    var audioUrl = URL.createObjectURL(audioBlob);

                    // Create a new audio element
                    var audioElement = document.createElement('audio');
                    audioElement.src = audioUrl;
                    audioElement.controls = true;

                    // Append the audio element to the document
                    document.body.appendChild(audioElement);

                    // Reset chunks array for the next recording
                    chunks = [];

                    // Reset the recording button text and flag
                    isRecording = false;
                    document.getElementById('recordButton').innerText = 'Start Recording';

                    // Notify the server that recording has stopped
                    socket.emit('recording_stopped');
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

        // Reset the recording button text
        document.getElementById('recordButton').innerText = 'Start Recording';

        // Notify the server that recording has stopped
        socket.emit('recording_stopped');
    }
});

socket.on('connect_error', (error) => {
    console.error('Socket connection error:', error);
});

socket.on('connect_timeout', () => {
    console.error('Socket connection timeout.');
});
