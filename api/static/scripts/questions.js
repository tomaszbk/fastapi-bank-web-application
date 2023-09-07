// script.js

// Define the questions
const questions = [
    "Do you like Python?",
    "Do you hate C#?",
    "Are you doing the TP with Python?",
    "Do you support Hitler?"
];

// Set up initial question index
let currentQuestionIndex = 0;

// Get necessary elements
const questionElement = document.getElementById("question");
const yesButton = document.getElementById("yes-btn");
const noButton = document.getElementById("no-btn");
const responseElement = document.getElementById("response");

// Function to handle button clicks
function handleButtonClick(answer) {
    // Check if the answer is "No"
    if (answer === "No") {
        responseElement.textContent = "Sorry, you don't share our company's values.";
    } else {
        // Check if there are more questions
        if (currentQuestionIndex < questions.length - 1) {
            currentQuestionIndex++;
            showNextQuestion();
        } else {
            responseElement.textContent = "Congratulations! You answered all the questions!";
        }
    }
}

// Function to show the next question
function showNextQuestion() {
    questionElement.textContent = questions[currentQuestionIndex];
    responseElement.textContent = "";
}

// Add event listeners to the buttons
yesButton.addEventListener("click", () => handleButtonClick("Yes"));
noButton.addEventListener("click", () => handleButtonClick("No"));

// Show the first question
showNextQuestion();
