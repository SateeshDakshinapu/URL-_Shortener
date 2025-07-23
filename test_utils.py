from app.utils import validate_url, generate_short_code

def test_validate_url_valid():
    assert validate_url("https://www.google.com")
    assert validate_url("http://example.org/test")

def test_validate_url_invalid():
    assert not validate_url("bad_url")
    assert not validate_url("google.com")
    assert not validate_url("ftp:/example.com")

def test_generate_short_code_default_length():
    code = generate_short_code()
    assert len(code) == 6
    assert code.isalnum()

def test_generate_short_code_custom_length():
    code = generate_short_code(10)
    assert len(code) == 10
    assert code.isalnum()
