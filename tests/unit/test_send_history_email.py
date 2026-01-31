import datetime
import pytest

from src.personal_account import PersonalAccount
from src.company_account import CompanyAccount


class TestEmail:
    today_date = datetime.datetime.today().strftime('%Y-%m-%d')
    email_address = "test@email.com"

    # Personal Account

    def test_send_history_via_email_personal_account(self, mocker):
        account = PersonalAccount("Jane", "Smith", "98765432101")

        # account.incoming_transfer(150.0)
        # account.outgoing_transfer(50.0)

        account.history = [150.0, -50.0]

        mock_send = mocker.patch(
            'src.personal_account.SMTPClient.send',
            return_value=True
        )

        result = account.send_history_via_email(self.email_address)

        assert result is True
        mock_send.assert_called_once()

        subject = mock_send.call_args[0][0]
        text = mock_send.call_args[0][1]
        email_address = mock_send.call_args[0][2]

        assert subject == "Account Transfer History " + self.today_date
        assert email_address == self.email_address
        assert text == f"Personal account history: {account.history}"

    def test_send_history_via_email_personal_account_failed(self, mocker):
        account = PersonalAccount("Jane", "Smith", "98765432101")
        account.history = [150.0, -50.0]

        mock_send = mocker.patch(
            'src.personal_account.SMTPClient.send',
            return_value=False
        )

        result = account.send_history_via_email(self.email_address)

        assert result is False

    # Company Account

    @pytest.fixture(autouse=True)
    def _mock_verify_nip(self, mocker):
        mocker.patch(
            "src.company_account.CompanyAccount.verify_nip",
            return_value=True
        )

    def test_send_history_via_email_company_account_success(self, mocker):
        account = CompanyAccount("Tech Solutions", "1234567890")
        account.history = [5000.0, -1000.0, 500.0]

        mock_send = mocker.patch(
            "src.company_account.SMTPClient.send",
            return_value=True
        )

        result = account.send_history_via_email("corp@test.com")

        assert result is True
        mock_send.assert_called_once()

        subject, text, email = mock_send.call_args[0]

        assert subject == f"Account Transfer History {self.today_date}"
        assert text == f"Company account history: {account.history}"
        assert email == "corp@test.com"

    def test_send_history_via_email_company_account_failed(self, mocker):
        account = CompanyAccount("Tech Solutions", "1234567890")
        account.history = [5000.0, -1000.0]

        mocker.patch(
            "src.company_account.SMTPClient.send",
            return_value=False
        )

        result = account.send_history_via_email("corp@test.com")

        assert result is False