import pathlib
from datetime import datetime
from email.message import EmailMessage

import aiosmtplib
from fastapi.templating import Jinja2Templates

from app.core.config import settings
from app.core.tasks import broker

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

@broker.task
async def task_send_recovery_email(email: str, token: str) -> None:
    message = EmailMessage()
    message["From"] = f"{settings.app.name} <{settings.smtp.user}>"
    message["To"] = email
    message["Subject"] = "Recovery password"

    reset_link = f"https://{settings.app.name}.{settings.app.domain}/reset?token={token}"

    template_response = templates.get_template("auth/recovery_email.html")
    current_year = datetime.now().year
    html_content = template_response.render({"reset_link": reset_link, "app": settings.app.name, "subject": message["Subject"], "year": current_year})

    message.add_alternative(html_content, "html")

    await aiosmtplib.send(
        message,
        hostname=settings.smtp.host,
        port=settings.smtp.port,
        username=settings.smtp.user,
        password=settings.smtp.password,
        use_tls=settings.smtp.ssl_required,
    )