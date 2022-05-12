#vår app
from web import create_app # hämtar create_app ifrån __init__.py inne i vårt python paket som är web mappen

if __name__ == '__main__':
    app = create_app()       #vi skapar våran app
    app.run(debug=True)      #någon tjusig kod för uppdatera sidan när du jobbar med den 