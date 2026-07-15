const categories = [
    "Cleaning",
    "Plumbing",
    "Maintenance",
    "Electrical",
    "Gaming",
    "Gardening",
    "Painting",
    "Carpentry",
    "Pest Control",
    "Moving",
    "Tutoring",
    "Pet Care",
    "Beauty Services",
    "Fitness Training",
    "Event Planning",
    "Photography",
    "Catering",
    "Transportation",
    "Home Improvement",
    "Appliance Repair",
    "Interior Design",
    "Landscaping",
    "Handyman Services",
    "IT Support",
]

const selectElement = document.getElementById('category');

categories.forEach(item => {
    const option = document.createElement('option');
    option.value = item;
    option.textContent = item;
    selectElement.appendChild(option);
});
