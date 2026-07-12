from app.admin.application import admin_dashboard_service


def test_get_admin_dashboard_data_returns_counts_and_lists(monkeypatch):
    users = ["user-1", "user-2"]
    services = ["service-1"]
    bookings = ["booking-1", "booking-2", "booking-3"]
    reviews = ["review-1"]

    monkeypatch.setattr(
        admin_dashboard_service,
        "find_all_users",
        lambda: users
    )

    monkeypatch.setattr(
        admin_dashboard_service,
        "find_all_services",
        lambda: services
    )

    monkeypatch.setattr(
        admin_dashboard_service,
        "find_all_bookings",
        lambda: bookings
    )

    monkeypatch.setattr(
        admin_dashboard_service,
        "find_all_reviews",
        lambda: reviews
    )

    dashboard_data = admin_dashboard_service.get_admin_dashboard_data()

    assert dashboard_data["users_count"] == 2
    assert dashboard_data["services_count"] == 1
    assert dashboard_data["bookings_count"] == 3
    assert dashboard_data["reviews_count"] == 1

    assert dashboard_data["users"] == users
    assert dashboard_data["services"] == services
    assert dashboard_data["bookings"] == bookings
    assert dashboard_data["reviews"] == reviews