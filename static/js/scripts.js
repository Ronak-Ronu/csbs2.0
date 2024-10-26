// Ensure this variable is defined at the top or within the scope of your script
const typedTextElement = document.getElementById('typed-text');

document.addEventListener('DOMContentLoaded', function() {
    // Your existing code for initialization
    const passageElement = document.getElementById('passage');
    
    if (passageElement) {
        console.log(passageElement.clientHeight);
    } else {
        console.error("Element with id 'passage' not found");
    }
});

let startTime;
let passageText = '';
let typingStarted = false;

document.getElementById('start-btn').addEventListener('click', async () => {
    const response = await fetch('/get_passage');
    const data = await response.json();
    
    // Make sure the passage is correctly assigned to the paragraph
    document.getElementById('passage').innerText = data.passage;
    passageText = data.passage; // Update passageText for comparison
    console.log(data);
    document.getElementById('typed-text').value = ''; // Clear text area
    typingStarted = false;
    document.getElementById('wpm-result').innerText = ''; // Clear result
});

document.getElementById('typed-text').addEventListener('input', () => {
    const typedText = document.getElementById('typed-text').value;
    
    if (!typingStarted) {
        startTime = new Date();
        typingStarted = true;
    }

    // Compare the typed text to the passage text progressively
    const correctText = passageText.slice(0, typedText.length);
    if (typedText === correctText) {
        document.getElementById('passage').style.color = 'green'; // Highlight correct typing
    } else {
        document.getElementById('passage').style.color = 'red'; // Highlight incorrect typing
        // Trigger the shake animation for incorrect typing
        typedTextElement.classList.add('shake');
        setTimeout(() => {
            typedTextElement.classList.remove('shake');
        }, 300); // Remove the shake effect after 300ms
    }

    if (typedText.trim() === passageText.trim()) {
        const endTime = new Date();
        const timeDiff = (endTime - startTime) / 1000 / 60; // Minutes
        const wordCount = passageText.split(' ').length;
        const wpm = Math.round(wordCount / timeDiff);

        document.getElementById('wpm-result').innerText = `Your speed: ${wpm} WPM`;

        // Save the result
        saveResult(wpm);
    }
});

async function saveResult(wpm) {
    const username = prompt('Enter your name:');
    try {
        const response = await fetch('/save_result', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username: username, wpm: wpm })
        });

        if (!response.ok) throw new Error('Error saving result');
        
        const data = await response.json();
        alert(data.message);
    } catch (error) {
        console.error(error);
        alert('There was an error saving your result. Please try again.');
    }
}
typedTextElement.addEventListener('input', () => {
    const typedText = typedTextElement.value;
    const correctText = passageText.slice(0, typedText.length);
    
    // Check if typing is detected and incorrect text triggers shake
    // console.log('Typed:', typedText);
    // console.log('Correct Text:', correctText);

    if (typedText !== correctText) {
        console.log('Shake triggered');
        typedTextElement.classList.add('shake');
        setTimeout(() => {
            typedTextElement.classList.remove('shake');
        }, 300); // Remove the shake effect after 300ms
    }
});
