from flask_mail import Message

def send_otp(mail,sender,email,otp):
    msg = Message(
        subject="otp from AI_LEARNING_TRACKER",
        sender = sender,
        recipients= [email]
    )
    msg.body  = f"Your OTP is {otp}"
    mail.send(msg)

