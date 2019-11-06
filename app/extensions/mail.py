from flask_mail import Mail, Message

mail = Mail()


def send_mail(subject, sender, recipients, text_body, html_body):
    msg = Message(
        subject, sender=sender, recipients=recipients, body=text_body, html=html_body
    )
    mail.send(msg)


def send_sign_up_mail(user):
    subject = "Bem-vindo ao Robinhood Brasil"
    sender = ("Robinhood Brasil", "rhoodbrazil@gmail.com")
    recipients = [user.email]
    text_body = "text body"
    html_body = f"<p>Olá!</p><p>Obrigado pelo cadastro! Você foi adicionado à nossa lista de espera.</p><p>Se quiser ter acesso mais cedo, é só compartilhar este link: http://localhost:3000/?ref={user.id}</p><p>Você pode verificar sua posição na lista de espera neste clicando <a href='http://localhost:3000/{user.id}'>aqui</a>"
    send_mail(subject, sender, recipients, text_body, html_body)
