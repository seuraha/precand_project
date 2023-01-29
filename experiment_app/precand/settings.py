from os import environ

SESSION_CONFIGS = [
    dict(
        name='T_Now',
        app_sequence=['mrt'],
        num_demo_participants=4,
        treatment="now",
    ),
    dict(
        name='T_10',
        app_sequence=['mrt'],
        num_demo_participants=4,
        treatment="10",
    ),
    dict(
        name='T_Never',
        app_sequence=['mrt'],
        num_demo_participants=4,
        treatment="never",
    ),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

ROOMS = [
    dict(
        name='Precand_session1',
        display_name='Session 1',
        participant_label_file='_rooms/participant_label.txt',
        # use_secure_urls=True
    ),
    dict(
        name='Precand_session2',
        display_name='Session 2',
        participant_label_file='_rooms/participant_label.txt',
        # use_secure_urls=True
    ),
]

PARTICIPANT_FIELDS = []
SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """
# DEBUG=False

SECRET_KEY = '2183522607764'
