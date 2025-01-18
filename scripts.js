// Smooth Scroll Navigation
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});

// Background Animation (change colors over time)
function changeBackground() {
    const colors = ['#1e2a47', '#2c3e50', '#34495e', '#5f6a77', '#4e5d6c'];
    let index = 0;
    setInterval(() => {
        document.body.style.backgroundColor = colors[index];
        index = (index + 1) % colors.length;
    }, 3000); // Change every 3 seconds
}

// Start background animation on page load
window.onload = changeBackground;

// Form Validation for Contact Page
document.querySelector("form").addEventListener("submit", function(e) {
    let name = document.querySelector("#name").value;
    let email = document.querySelector("#email").value;
    let message = document.querySelector("#message").value;

    if (!name || !email || !message) {
        e.preventDefault();
        alert("All fields must be filled out.");
    } else {
        alert("Your message has been sent!");
    }
});

// Show the modal when the page loads
window.onload = () => {
    document.getElementById('specialModal').style.display = 'flex';
};

// Close the modal when the user clicks the "Close" button
document.getElementById('closeModal').addEventListener('click', () => {
    document.getElementById('specialModal').style.display = 'none';
});

// DOM content loaded event
document.addEventListener("DOMContentLoaded", () => {
    // Handle contact form submission
    const contactForm = document.getElementById('contactForm');
    
    // Check if form exists in the page
    if (contactForm) {
        contactForm.addEventListener('submit', handleContactFormSubmit);
    }
});

// Handle the contact form submission
function handleContactFormSubmit(event) {
    event.preventDefault(); // Prevent page reload on form submission
    
    const formData = new FormData(event.target);
    
    // Basic form validation
    if (!formData.get('name') || !formData.get('email') || !formData.get('message')) {
        alert("All fields are required!");
        return;
    }

    // Prepare the data to be sent to the backend
    const data = {
        name: formData.get('name'),
        email: formData.get('email'),
        message: formData.get('message')
    };
    
    // Send data to the backend via AJAX (Using Fetch API)
    fetch('https://your-backend-url.com/contact', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data) // Converting data to JSON format
    })
    .then(response => response.json()) // Parse response as JSON
    .then(data => {
        if (data.success) {
            alert('Your message has been sent successfully!');
            contactForm.reset(); // Reset the form
        } else {
            alert('There was an error submitting your message. Please try again.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('There was an error submitting your message. Please try again.');
    });
}

// Sample for other dynamic interactions
function updateFeatureContent() {
    // Example of dynamically updating feature content via API call
    fetch('https://your-backend-url.com/features')
        .then(response => response.json())
        .then(data => {
            // Update the feature section with data from the backend
            const featuresContainer = document.querySelector('.features');
            featuresContainer.innerHTML = '';
            data.features.forEach(feature => {
                const featureCard = document.createElement('div');
                featureCard.classList.add('feature-card');
                featureCard.innerHTML = `
                    <h3>${feature.title}</h3>
                    <p>${feature.description}</p>
                `;
                featuresContainer.appendChild(featureCard);
            });
        })
        .catch(error => {
            console.error('Error fetching features:', error);
            alert('Error loading features.');
        });
}