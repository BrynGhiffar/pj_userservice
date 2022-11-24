from adapter.discord.api import DiscordApi

class NotificationService:

    def __init__(self, api: DiscordApi):
        self.api = api
    
    def send_message(self, title: str, message: str, body: str) -> None:
        to_be_sent = message + "\n"
        to_be_sent += f"> **{title}**\n"
        for line in body.splitlines():
            to_be_sent += f"> {line}\n"
        self.api.send_message(to_be_sent)
    
    def send_user_created_notification(self, user_id: str, user_email: str, user_name: str) -> None:

        title = "User Created!"
        message = "A user was created."
        body = "```\n" \
            + "user id: " + user_id + "\n" \
            + "user email: " + user_email + "\n" \
            + "user name: " + user_name + "\n" \
            + "```\n"
        self.send_message(title, message, body)
