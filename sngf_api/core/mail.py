from django.core.mail import EmailMessage


class SendMail:
    def __init__(  # noqa: PLR0913
        self,
        subject: str,
        body: str,
        to: list[str],
        from_email: str | None = None,
        cc: list[str] | None = None,
        bcc: list[str] | None = None,
        attachments: list[str] | None = None,
    ):
        self.subject = subject
        self.body = body
        self.to = to
        self.from_email = from_email
        self.cc = cc
        self.bcc = bcc
        self.attachments = attachments or []

    def send(self):
        email = EmailMessage(
            subject=self.subject,
            body=self.body,
            from_email=self.from_email,
            to=self.to,
            cc=self.cc,
            bcc=self.bcc,
        )

        for attachment_path in self.attachments:
            email.attach_file(attachment_path)

        email.send()
