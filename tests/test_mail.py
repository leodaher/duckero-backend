from unittest import mock
from flask_mail import Message
from app.extensions.mail import mail, send_mail, send_sign_up_mail


@mock.patch("app.extensions.mail.Mail.send")
@mock.patch("app.extensions.mail.Message")
def test_send_mail(mock_message, mock_mail_send, faker):
    subject = faker.sentence()
    sender = faker.email()
    recipients = [faker.email(), faker.email()]
    body = faker.sentence()
    html = faker.sentence()

    msg = Message(subject, sender=sender, recipients=recipients, body=body, html=html)

    mock_message.return_value = msg

    send_mail(subject, sender, recipients, body, html)

    assert mock_message.call_count == 1
    mock_message.assert_called_once_with(
        subject, sender=sender, recipients=recipients, body=body, html=html
    )
    mock_mail_send.assert_called_once_with(msg)


@mock.patch("app.extensions.mail.send_mail")
def test_send_sign_up_mail(mock_send_mail, user, client):

    send_sign_up_mail(user)

    assert mock_send_mail.call_count == 1
    for args, kwargs in mock_send_mail.call_args_list:
        recipients = args[2]
        assert recipients == [user.email]
