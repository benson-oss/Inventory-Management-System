import sys

sys.path.insert(0, ".")
import cli
def test_cli_login(monkeypatch):
    # Provide username and password automatically
    inputs = iter(["benson", "12344"])
    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs))
    

    class FakeResponse:
        status_code = 200
        def json(self):
            return {
                "message": "Login successful",
                "admin": "benson"
            }
    def fake_post(*args, **kwargs):
        return FakeResponse()
    monkeypatch.setattr(
        cli.session,
        "post",
        fake_post
    )
    result = cli.login()
    assert result is True