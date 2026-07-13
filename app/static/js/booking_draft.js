document.addEventListener("DOMContentLoaded", function () {
    const bookingForm = document.getElementById("booking-form");
    const problemDescriptionInput = document.getElementById("problem_description");
    const bookingDateInput = document.getElementById("booking_date");
    const bookingTimeInput = document.getElementById("booking_time");
    const bookingAddressInput = document.getElementById("address");

    if (!problemDescriptionInput || !bookingForm) {
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

    bookingForm.addEventListener("input", function () {
        localStorage.setItem(draftKey, JSON.stringify({
            problemDescription: problemDescriptionInput.value,
            bookingDate: bookingDateInput.value,
            bookingTime: bookingTimeInput.value,
            bookingAddress: bookingAddressInput.value
        }));
    });

    bookingForm.addEventListener("submit", function () {
        localStorage.removeItem(draftKey);
    });
});