from django.db import models

# Used for the song image
def upload_path(instance, filename):
    # return '/'.join(['images', str(instance.songTitle), filename])
    return '/'.join(['images', filename])

# Used for the sound file
def upload_soundFile_path(instance, fileName):
    return '/'.join(['soundFiles', fileName])

class Song(models.Model):
    songTitle = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    image = models.ImageField(upload_to=upload_path, null=True)
    audio = models.FileField(upload_to=upload_soundFile_path, null=True)

    def __str__(self):
        return self.songTitle + " by " + self.author