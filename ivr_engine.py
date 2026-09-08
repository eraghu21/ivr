import re
from agriculture_data import WEATHER, MARKET_PRICES, SCHEMES, IRRIGATION, FERTILIZER

def normalize(text):
    return re.sub(r"\s+", " ", text.strip().lower())

def detect_intent(text):
    t = normalize(text)
    if any(k in t for k in ["weather", "rain", "temperature", "வானிலை", "மழை", "வெப்பநிலை"]): return "weather"
    if any(k in t for k in ["price", "market", "rate", "விலை", "சந்தை"]): return "market_price"
    if any(k in t for k in ["scheme", "subsidy", "government", "திட்டம்", "மானியம்"]): return "schemes"
    if any(k in t for k in ["irrigation", "water", "watering", "பாசனம்", "தண்ணீர்", "நீர்"]): return "irrigation"
    if any(k in t for k in ["fertilizer", "fertiliser", "urea", "உரம்", "யூரியா"]): return "fertilizer"
    if any(k in t for k in ["disease", "leaf", "yellow", "pest", "நோய்", "இலை", "மஞ்சள்", "பூச்சி"]): return "crop_disease"
    return "help"

def find_crop(text):
    t = normalize(text)
    crops = {
        "tomato": ["tomato", "தக்காளி"], "rice": ["rice", "paddy", "நெல்", "அரிசி"],
        "cotton": ["cotton", "பருத்தி"], "groundnut": ["groundnut", "peanut", "நிலக்கடலை"],
        "sugarcane": ["sugarcane", "கரும்பு"],
    }
    for crop, words in crops.items():
        if any(w in t for w in words): return crop
    return None

def process_query(text, language="English"):
    intent, crop = detect_intent(text), find_crop(text)
    if language == "தமிழ்": return tamil_response(intent, crop)
    if intent == "weather": return {"intent": intent, "response": WEATHER["English"]}
    if intent == "market_price":
        if crop in MARKET_PRICES: return {"intent": intent, "response": f"Today's indicative {crop} market price is ₹{MARKET_PRICES[crop]} per kg."}
        return {"intent": intent, "response": "Please mention the crop name, for example: tomato market price."}
    if intent == "schemes": return {"intent": intent, "response": SCHEMES["English"]}
    if intent == "irrigation":
        if crop in IRRIGATION: return {"intent": intent, "response": IRRIGATION[crop]["English"]}
        return {"intent": intent, "response": "Please mention the crop name to receive irrigation advice."}
    if intent == "fertilizer":
        if crop in FERTILIZER: return {"intent": intent, "response": FERTILIZER[crop]["English"]}
        return {"intent": intent, "response": "Please mention the crop name to receive fertilizer guidance."}
    if intent == "crop_disease": return {"intent": intent, "response": "For reliable disease diagnosis, upload a clear crop-leaf photo in the main agriculture platform. Describe the crop and symptoms. Do not apply pesticides without local expert confirmation."}
    return {"intent": intent, "response": "You can ask about weather, market price, crop disease, government schemes, irrigation, or fertilizer advice."}

def tamil_response(intent, crop):
    names = {"tomato":"தக்காளி", "rice":"நெல்", "cotton":"பருத்தி", "groundnut":"நிலக்கடலை", "sugarcane":"கரும்பு"}
    if intent == "weather": return {"intent": intent, "response": WEATHER["தமிழ்"]}
    if intent == "market_price":
        if crop in MARKET_PRICES: return {"intent": intent, "response": f"இன்றைய மாதிரி {names[crop]} சந்தை விலை கிலோ ஒன்றுக்கு ₹{MARKET_PRICES[crop]}."}
        return {"intent": intent, "response": "பயிரின் பெயரை சொல்லுங்கள். உதாரணமாக: தக்காளி சந்தை விலை என்ன?"}
    if intent == "schemes": return {"intent": intent, "response": SCHEMES["தமிழ்"]}
    if intent == "irrigation":
        if crop in IRRIGATION: return {"intent": intent, "response": IRRIGATION[crop]["தமிழ்"]}
        return {"intent": intent, "response": "பாசன ஆலோசனைக்கு பயிரின் பெயரை சொல்லுங்கள்."}
    if intent == "fertilizer":
        if crop in FERTILIZER: return {"intent": intent, "response": FERTILIZER[crop]["தமிழ்"]}
        return {"intent": intent, "response": "உர ஆலோசனைக்கு பயிரின் பெயரை சொல்லுங்கள்."}
    if intent == "crop_disease": return {"intent": intent, "response": "நோயை நம்பகமாக கண்டறிய, வேளாண்மை தளத்தில் பயிர் இலை புகைப்படத்தை பதிவேற்றவும். உள்ளூர் நிபுணர் ஆலோசனை இல்லாமல் பூச்சிக்கொல்லி பயன்படுத்த வேண்டாம்."}
    return {"intent": intent, "response": "வானிலை, சந்தை விலை, பயிர் நோய், அரசு திட்டங்கள், பாசனம் அல்லது உரம் பற்றி கேட்கலாம்."}
