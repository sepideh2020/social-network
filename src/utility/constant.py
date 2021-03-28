WEBSITE_REGEX = '(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})'
PASSWORD_REGEX = "^(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])(?=.*[@#/$])[\w\d@/#$]{6,}$"
PHONE_REGEX = '^(09[0-9]{9})$'
EMAIL_REGEX = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
USERNAME_REGEX = '^(?!.*\.\.)(?!.*\.$)[^\W][\w.]{0,29}$'
