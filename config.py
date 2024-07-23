import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'ALongRandomlyGeneratedString')
    SESSION_TYPE = 'filesystem'
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb+srv://chrisdepallan:chrisdepallan@cluster0.1fiecxd.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
    OAUTH2_CLIENT_ID = "563837791779-428mfra3k3klg8vk9f5ai1a5t2pmu6ea.apps.googleusercontent.com"
    OAUTH2_CLIENT_SECRET = "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"
    OAUTH2_META_URL = "https://accounts.google.com/.well-known/openid-configuration"
