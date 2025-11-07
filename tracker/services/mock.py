from django.contrib.auth import get_user_model


User = get_user_model()
# Наприклад, у функції:
def get_first_user():
    return User.objects.first() # або .get(id=1) якщо точно знаєш ID

class MockRequest:
    def __init__(self):
        self.user = get_first_user()
        self.session = {"session_key": get_first_user().id}