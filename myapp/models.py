from django.db import models
from django.contrib.auth.models import User
from cryptography.fernet import Fernet

# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    marks = models.IntegerField(default=20)

    def __str__(self):
        return self.question_text

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=100)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.answer_text
    
class Results(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_marks=models.BinaryField(default=0)
    correct_answers=models.IntegerField(default=0)
    incorrect_answers=models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.total_marks = self._encrypt_marks()
        super().save(*args, **kwargs)

    def _encrypt_marks(self):
        key = b'b26tkx7hwc7-7gXPGzz_7mu4GH_-kmUy3M4wQMuj9TM='  
        cipher_suite = Fernet(key)
        encrypted_marks = cipher_suite.encrypt(str(self.total_marks).encode())
        return encrypted_marks

    def get_decrypted_marks(self):
        from cryptography.fernet import Fernet
        key = b'b26tkx7hwc7-7gXPGzz_7mu4GH_-kmUy3M4wQMuj9TM='  
        cipher_suite = Fernet(key)
        decrypted_marks = cipher_suite.decrypt(self.total_marks).decode()
        return int(decrypted_marks)
