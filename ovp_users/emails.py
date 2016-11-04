from ovp_core.emails import BaseMail

class UserMail(BaseMail):
  """
  This class is responsible for firing emails for Users
  """
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

