from fastapi.testclient import TestClient

from my_project.app import app


def test_health_check() -> None:
    """测试健康检查端点。"""
    # Arrange
    client = TestClient(app)

    # Act
    response = client.get("/")

    # Assert
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "service": "user-api"}
