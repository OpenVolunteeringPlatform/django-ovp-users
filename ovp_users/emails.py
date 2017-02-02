from ovp_core.emails import BaseMail

class UserMail(BaseMail):
  """
  This class is responsible for firing emails for Users
  """
  def __init__(self, user, async_mail=None):
    super(UserMail, self).__init__(user.email, async_mail)

  def sendWelcome(self, context={}):
    """
    Sent when user registers
    """
    return self.sendEmail('welcome', 'Welcome', context)


  def sendRecoveryToken(self, context):
    """
    Sent when volunteer requests recovery token
    """
    return self.sendEmail('recoveryToken', 'Password recovery', context)

