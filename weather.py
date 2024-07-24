import requests

def get_coordinates(address):
    geocode_url = f"https://nominatim.openstreetmap.org/search?q={address}&format=json&limit=1"
    response = requests.get(geocode_url)
    
    if response.status_code == 200:
        data = response.json()
        if data:
            lat = data[0]['lat']
            lon = data[0]['lon']
            return lat, lon
        else:
            return None, None
    else:
        return None, None

def get_weather(address):
    lat, lon = get_coordinates(address)

    if lat and lon:
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        response = requests.get(weather_url)
        
        if response.status_code == 200:
            data = response.json()
            
            if 'current_weather' in data:
                weather = data['current_weather']
                temperature = weather.get('temperature', "noma'lum")
                wind_speed = weather.get('windspeed', "noma'lum")
                humidity = weather.get('relative_humidity', "noma'lum")
                pressure = weather.get('pressure', "noma'lum")
                time = weather.get('time', "noma'lum")
                winddirection = weather.get('winddirection', "noma'lum")
                
                # Format the output
                formatted_output = (
                    f"📍 <b>Manzil:</b> {address.capitalize()}\n"
                    f"🌡️ <b>Harorat:</b> {temperature}°C\n"
                    f"🌪️ <b>Shamol tezligi:</b> {wind_speed} km/h\n"
                    f"💨 <b>Shamol yo'nalishi:</b> {winddirection}\n"
                    f"💧 <b>Namlik:</b> {humidity} %\n"
                    f"💨 <b>Bosim:</b> {pressure} hPa\n"
                    f"⌚ <b>Vaqt:</b> {time}"
                )
                
                return formatted_output
            else:
                return f"Uzr, serverda yoki internetda xatolik.\nIltimos kiritgan mamlakat yoki shahar nomini to'g'riligini tekshiring."
        else:
            return f"Uzr, serverda yoki internetda xatolik.\nIltimos kiritgan mamlakat yoki shahar nomini to'g'riligini tekshiring."
    else:
        return f"Uzr, serverda yoki internetda xatolik.\nIltimos kiritgan mamlakat yoki shahar nomini to'g'riligini tekshiring."