import smtplib

def send_email(to_email, subject, message):
    try:
        sender = "your_email@gmail.com"
        password = "your_app_password"
        
        if sender == "your_email@gmail.com":
            print(f"Bypassing real email trigger to {to_email}. Ensure real credentials are provided.")
            return

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender, password)

        msg = f"Subject: {subject}\n\n{message}"

        server.sendmail(sender, to_email, msg)
        server.quit()
    except Exception as e:
        print(f"Error firing email: {e}")
