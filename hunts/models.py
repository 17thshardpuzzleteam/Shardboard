from django.conf import settings
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
    web_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['guild_id', 'category_id'], name='unique_guild_hunt_category_combination'
            )
        ]


class Round(models.Model):
    name = models.CharField(max_length=255, verbose_name='Name')
    marker = models.CharField(max_length=7, verbose_name='Marker')
    category_id = models.IntegerField(verbose_name='Round Category ID')
    hunt = models.ForeignKey(Hunt, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['hunt', 'name'], name='unique_hunt_round_combination'
            ),
            models.UniqueConstraint(
                fields=['hunt', 'marker'], name='unique_hunt_marker_combination'
            ),
            models.UniqueConstraint(
                fields=['hunt', 'category_id'], name='unique_hunt_category_combination'
            )
        ]

    def __str__(self):
        return self.marker + ' ' + self.name


class Puzzle(models.Model):
    name = models.CharField(max_length=511, verbose_name='Name')
    channel_id = models.IntegerField(verbose_name='Channel ID')
    voice_channel_id = models.IntegerField(verbose_name='Voice Channel ID', null=True)
    answer = models.CharField(max_length=255, verbose_name='Answer', null=True)
    spreadsheet_link = models.CharField(max_length=255, verbose_name='Spreadsheet Link')
    priority = models.CharField(max_length=15, verbose_name='Priority')
    notes = models.CharField(max_length=511, verbose_name='Notes', null=True)
    unlock_time = models.DateTimeField(verbose_name='Unlock Time')
    solve_time = models.DateTimeField(verbose_name='Solve Time', null=True)
    is_meta = models.BooleanField(verbose_name='Is Meta?', default=False)
    hunt = models.ForeignKey(Hunt, on_delete=models.CASCADE)
    rounds = models.ManyToManyField(Round)
    feeders = models.ManyToManyField('self', related_name='feeding', symmetrical=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['hunt', 'name'], name='unique_hunt_puzzle_combination'
            ),
            models.UniqueConstraint(
                fields=['hunt', 'channel_id'], name='unique_hunt_channel_combination'
            )
        ]

    def __str__(self):
        return self.name
