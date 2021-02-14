import os

app_dir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig:
    DEBUG = True
    POSTGRES_URL="techconfdb-migration.postgres.database.azure.com"
    POSTGRES_USER="admric@techconfdb-migration"
    POSTGRES_PW="pass123456@"
    POSTGRES_DB="techconfdb"
    DB_URL = 'postgresql://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER,pw=POSTGRES_PW,url=POSTGRES_URL,db=POSTGRES_DB)
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI') or DB_URL
    CONFERENCE_ID = 1
    SECRET_KEY = 'LWd2tzlprdGHCIPHTd4tp5SBFgDszm'
    SERVICE_BUS_CONNECTION_STRING ='Endpoint=sb://sb-notification-techconf.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=QLkjcB41bESCyA1ONRZpncYWKBZMfhv1RlnouOFJd6Q=' 
    SERVICE_BUS_QUEUE_NAME ='notificationqueue'
    ADMIN_EMAIL_ADDRESS: 'fantaere@gmail.com'
    SENDGRID_API_KEY = 'SG.GYlCv6TOQouKv0jsxx8kuw.Ike8ot3YMsG-k7TceFG386P88oQh0IVTud3TtvVS4nM' 

class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False