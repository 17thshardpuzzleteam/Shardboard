from django.db import models


class Hunt(models.Model):
    guild_id = models.IntegerField(verbose_name='Guild ID')
    name = models.CharField(max_length=255, verbose_name='Name')
    category_id = models.IntegerField(verbose_name='Category ID')
    role_id = models.IntegerField(verbose_name='Role ID', null=True)
    url = models.SlugField(max_length=255, verbose_name='URL', null=True)
    username = models.SlugField(max_length=255, verbose_name='Username', null=True)
    password = models.SlugField(max_length=255, verbose_name='Password', null=True)
    folder = models.SlugField(max_length=511, verbose_name='Folder Link')
    nexus = models.SlugField(max_length=511, verbose_name='Nexus Link')
    team_name = models.CharField(max_length=255, verbose_name='Team Name', null=True)
    is_bighunt = models.BooleanField(verbose_name="Is Bighunt?")
    logfeed = models.IntegerField(verbose_name="Logfeed Channel ID", null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['guild_id', 'category_id'], name='unique_guild_name_combination'
            )
        ]

    def __str__(self):
        return self.name
