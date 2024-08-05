import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'ALongRandomlyGeneratedString')
    SESSION_TYPE = 'filesystem'
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb+srv://chrisdepallan:chrisdepallan@cluster0.1fiecxd.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
    OAUTH2_CLIENT_ID = "563837791779-428mfra3k3klg8vk9f5ai1a5t2pmu6ea.apps.googleusercontent.com"
    OAUTH2_CLIENT_SECRET = "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"
    OAUTH2_META_URL = "https://accounts.google.com/.well-known/openid-configuration"
    NEWSAPI_KEYS = [
        "83e536c598ae4d45882122a4eeb377c6",
        "4dbc17e007ab436fb66416009dfb59a8"
    ]
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    
    MAIL_USERNAME = os.getenv('MAIL_USERNAME', 'modderhubmail@gmail.com')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', 'qbvb ijzi zzib nlln')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', 'modderhubmail@gmail.com')
    PFP_STYLE = ['pixel-art', 'avataaars', 'bottts', 'gridy', 'identicon', 'jdenticon', 'micah', 'lorelei']


