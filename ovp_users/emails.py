from django.core.mail import EmailMultiAlternatives
from django.template import Context, Template
from django.template.loader import get_template

from utils.router import ClientRouter


class BaseMail:
  """
  This class is responsible for firing emails
  """
  from_email = ''

  def __init__(self, user):
    self.user = user

  def sendEmail(self, template_name, subject, context):
    ctx = Context(context)
    text_content = get_template('email/{}.txt'.format(template_name)).render(ctx)
    html_content = get_template('email/{}.html'.format(template_name)).render(ctx)

    msg = EmailMultiAlternatives(subject, text_content, self.from_email, [self.user.email])
    msg.attach_alternative(text_content, "text/plain")
    msg.attach_alternative(html_content, "text/html")
    return msg.send() > 0

class UserMail(BaseMail):
  """
  This class is responsible for firing emails for Users
  """
  def sendRecoveryToken(self, context):
    """
    Sent when volunteer requests recovery token
    """
    c = {'link': ClientRouter.recoverPassword(context['token'])}
    return self.sendEmail('recoveryToken', 'Solicitação de recuperação de senha', c)
