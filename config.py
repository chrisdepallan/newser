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
        "4dbc17e007ab436fb66416009dfb59a8",
        "e0365bedc3b9406f9b278e204b53befd"
    ]
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    OPENAI_API_KEY= "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"

    MAIL_USERNAME = os.getenv('MAIL_USERNAME', 'modderhubmail@gmail.com')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', 'qbvb ijzi zzib nlln')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', 'modderhubmail@gmail.com')
    PFP_STYLE = ['pixel-art', 'avataaars', 'bottts', 'gridy', 'identicon', 'jdenticon', 'micah', 'lorelei']
    CLOUDINARY_CLOUD_NAME = os.getenv('CLOUDINARY_CLOUD_NAME', 'dbco4nje5')
    CLOUDINARY_API_KEY = os.getenv('CLOUDINARY_API_KEY', '864987881763555')
    CLOUDINARY_API_SECRET = os.getenv('CLOUDINARY_API_SECRET', 'UQA7JNdHcdpDMQvka0guWEtYhwQ')
    WEATHERAPI_KEY = 'd288547b5e1e498abbc175853240808'
    # REDIS_URL = "redis://default:TCnfNcNZYpS4ujKc9GViKIRTt64Ts8Wn@redis-13853.c89.us-east-1-3.ec2.redns.redis-cloud.com:13853"
    REDIS_URL="redis://default:jVeCrZx3iUxk1wc7aTrs0SCLLwUnBUW7@redis-11404.c90.us-east-1-3.ec2.redns.redis-cloud.com:11404"