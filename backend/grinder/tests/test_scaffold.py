def test_health(client):
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_admin_login(client):
    assert client.get("/admin/login/").status_code == 200
