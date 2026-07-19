document.addEventListener("DOMContentLoaded", function () {
    const bookingForm = document.getElementById("booking-form");
    const problemDescriptionInput = document.getElementById("problem_description");
    const bookingDateInput = document.getElementById("booking_date");
    const bookingTimeInput = document.getElementById("booking_time");
    const bookingAddressInput = document.getElementById("address");
    const phone_numberInput = document.getElementById("phone_number");
    if (!problemDescriptionInput || !bookingForm || !bookingDateInput || !bookingTimeInput || !bookingAddressInput || !phone_numberInput) {
        return;
    }

    const draftKey = 'booking_draft';

    const savedDraft = JSON.parse(localStorage.getItem(draftKey)) || {};

    if (savedDraft.problemDescription && problemDescriptionInput.value.trim() === "") {
        problemDescriptionInput.value = savedDraft.problemDescription;
    }

    if (savedDraft.bookingDate && bookingDateInput.value.trim() === "") {
        bookingDateInput.value = savedDraft.bookingDate;
    }

    if (savedDraft.bookingTime && bookingTimeInput.value.trim() === "") {
        bookingTimeInput.value = savedDraft.bookingTime;
    }

    if (savedDraft.bookingAddress && bookingAddressInput.value.trim() === "") {
        bookingAddressInput.value = savedDraft.bookingAddress;
    }

    if (savedDraft.phone_number && phone_numberInput.value.trim() === "") {
        phone_numberInput.value = savedDraft.phone_number;
    }

    bookingForm.addEventListener("input", function () {
        localStorage.setItem(draftKey, JSON.stringify({
            problemDescription: problemDescriptionInput.value,
            bookingDate: bookingDateInput.value,
            bookingTime: bookingTimeInput.value,
            bookingAddress: bookingAddressInput.value,
            phone_number: phone_numberInput.value
        }));
    });

    bookingForm.addEventListener("submit", function () {
        localStorage.removeItem(draftKey);
    });
});