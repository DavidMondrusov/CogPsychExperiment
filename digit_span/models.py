from django.db import models

class Test(models.Model):
    name = models.CharField(max_length=255)
    round = models.IntegerField()
    music = models.CharField(max_length=10)
    bothEars = models.CharField(max_length=5)
    score = models.IntegerField() 
   

    def __str__(self):
        return f"{self.name} - {self.score}"
    
class PlayerCount(models.Model):
    count = models.IntegerField(default=0)

    def increment(self):
        self.count += 1
        self.save()

    @classmethod
    def get_count(cls):
        obj, created = cls.objects.get_or_create(id=1)  # Ensures only one instance
        return obj.count