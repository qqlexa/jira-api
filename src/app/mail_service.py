from abc import ABC, abstractmethod


class MailService(ABC):
    @abstractmethod
    def send_mail(self, recipients: list[str], subject: str, body: str):
        raise NotImplementedError()


class JiraFakeMailService(MailService):
    def send_mail(self, recipients: list[str], subject: str, body: str):
        print(f"List addressing to {', '.join(recipients)}")
        print(f"Subject: {subject}")
        print(f"Body: {body}")


# TODO Implement real MailService here
