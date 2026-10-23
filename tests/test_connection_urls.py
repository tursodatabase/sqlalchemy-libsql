import pytest
from sqlalchemy import create_engine
from urllib.parse import urlsplit


@pytest.mark.parametrize("host", ["::1", "2001:db8::1", "127.0.0.1", "example.com"])
@pytest.mark.parametrize("secure", [False, True])
def test_remote_connection_url(host, secure):
    authority = f"[{host}]" if ":" in host else host
    engine = create_engine(
        f"sqlite+libsql://{authority}:8080/database?secure={str(secure).lower()}"
    )
    try:
        args, options = engine.dialect.create_connect_args(engine.url)
        scheme = "https" if secure else "http"
        assert args == [f"{scheme}://{authority}:8080/database"]
        parsed = urlsplit(args[0])
        assert parsed.hostname == host
        assert parsed.port == 8080
        assert options["uri"] is True
    finally:
        engine.dispose()
