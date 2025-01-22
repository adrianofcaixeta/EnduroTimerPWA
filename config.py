class Config:
    SECRET_KEY = 'sua_chave_secreta_aqui'
    PWA_NAME = 'Enduro Timer'
    PWA_SHORT_NAME = 'EnduroTimer'
    PWA_THEME_COLOR = '#000000'
    PWA_BACKGROUND_COLOR = '#ffffff'
    PWA_DISPLAY = 'standalone'
    PWA_SCOPE = '/'
    PWA_START_URL = '/'
    PWA_ICONS = [
        {
            'src': '/static/images/icon-192x192.png',
            'sizes': '192x192',
            'type': 'image/png'
        },
        {
            'src': '/static/images/icon-512x512.png',
            'sizes': '512x512',
            'type': 'image/png'
        }
    ]