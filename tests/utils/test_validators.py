import pytest

from app.utils.validators import password_validate, username_validate


class TestUsernameValidate:

    def test_username_validator_positive(self):
        username = "Ilya"
        assert username == username_validate(username)


    def test_username_validator_negative(self):
        with pytest.raises(ValueError):
            username = "Ilya@"
            username_validate(username)


class TestPasswordValidate:

    negative_test_passwords = [
        "hack_me",
        "dqkppofcmw3fpo3i22",
        "(*%()!%!)",
    ] 

    def test_password_validator_positive(self):
        password = "iobpdwd1223*%"
        assert password == password_validate(password)

    def test_password_validator_negative(self):
        for password in self.negative_test_passwords:
            with pytest.raises(ValueError):
                assert password_validate(password)