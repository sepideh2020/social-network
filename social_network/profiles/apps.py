from django.apps import AppConfig


class ProfilesConfig(AppConfig):
    name = 'profiles'
    verbose_name = 'Profiles, Relationships'

    def ready(self):
        import profiles.signals
