from linear_python_client import LinearClient


def test_client_init():
    client = LinearClient("test-key")
    assert client._client.headers["Authorization"] == "test-key"
    client.close()


def test_client_context_manager():
    with LinearClient("test-key") as client:
        assert client._client.headers["Authorization"] == "test-key"
