# 📚 Quiz Bot - Telegram Bot

Aiogram 3.22 bilan yozilgan **Quiz Bot** - foydalanuvchilarga turli yo'nalishda test ishlash imkoniyatini beradi.

## 🎯 Xususiyatlar

✅ **Kanal obunasi** - Kanal obunasini tekshirish  
✅ **Test ishlash** - 4 kategoriya: Backend, Frontend, Grafika, Savodhonlik  
✅ **Vaqt limiti** - 15 soniyada javob berish kerak  
✅ **QBC tizimi** - To'g'ri javob = +0.5 QBC  
✅ **Referral tizimi** - Har bir referral = +0.2 QBC  
✅ **Admin paneli** - Statistika, savol qo'shish, reklama  
✅ **Copy/Screenshot blokirovka** - Savol copy-paste va screenshot qilib bo'lmaydi  
✅ **JSON storage** - Barcha ma'lumotlar JSON faylida saqlanadi  
✅ **Menyu** - Balans, Qo'llanma, Yordam, Premium

## 📁 Loyiha Strukturasi

```
mukammal bot/
├── main.py                 # Asosiy bot file
├── config.py              # Konfiguratsiya
├── utils.py               # JSON bilan ishlash
├── keyboards.py           # Tugmalar
├── filters.py             # Kanal tekshirish
├── logger.py              # Log yozish
├── middleware.py          # Middleware
├── requirements.txt       # Dependencies
├── .env                   # Environment variables
├── data/
│   ├── users.json        # Foydalanuvchilar
│   └── questions.json    # Savollar
└── handlers/
    ├── start.py          # Start handler
    ├── test.py           # Test handler
    ├── menu.py           # Menyu handler
    ├── admin.py          # Admin handler
    └── referral.py       # Referral handler
```

## 🚀 O'rnatish va Ishga tushirish

### 1. Dependencies o'rnatish

```bash
pip install -r requirements.txt
```

### 2. .env faylini sozlash

```env
BOT_TOKEN=YOUR_BOT_TOKEN
ADMIN_ID=YOUR_ADMIN_ID
CHANNEL_ID=-1001234567890
CHANNEL_URL=https://t.me/yourchannel
```

### 3. Botni ishga tushirish

```bash
python main.py
```

## 📊 Buyruqlar

- `/start` - Botni boshlash
- `/admin` - Admin panelini ochish
- `/help` - Yordam

## 🎮 Foydalanuvchi Interfeysi

### Asosiy Menyu
- 📝 Test ishlash
- 💰 Balans
- 📖 Qo'llanma
- 🆘 Yordam
- ⭐ Premium

### Test Kategoriyalari
- Backend
- Frontend
- Grafika
- Savodhonlik

## 🔐 Admin Buyruqlari

- **Statistika ko'rish** - Foydalanuvchi statistikasi (bugun, shu hafta, shu oy)
- **Savol qo'shish** - Yangi savol va javoblarni qo'shish
- **Reklama yuborish** - Barcha foydalanuvchilarga habar yuborish

## 💾 JSON Fayl Strukturasi

### users.json
```json
[
  {
    "id": 123456789,
    "username": "user123",
    "qbc": 5.5,
    "total_questions": 10,
    "correct_answers": 8,
    "referrals": [111, 222],
    "referred_by": 100,
    "created_at": "2025-11-15 10:30:00",
    "is_premium": false,
    "attempted_questions": [1, 2, 3]
  }
]
```

### questions.json
```json
{
  "backend": [
    {
      "id": 1,
      "question": "Python-da o'zgaruvchini e'lon qilish?",
      "answers": [
        {"text": "var x = 5", "correct": false},
        {"text": "x = 5", "correct": true},
        {"text": "let x = 5", "correct": false},
        {"text": "const x = 5", "correct": false}
      ]
    }
  ]
}
```

## 🔄 Referral Tizimi

1. Foydalanuvchi o'z referral kodini do'stlariga yuboradi
2. Do'st `/start ref_USER_ID` linki bilan boshlaydi
3. Har bir referral uchun: +0.2 QBC

## ⏱️ Test Vaqti

- Har bir savol: 15 soniya
- Vaqt tugaganda: Avtomatik keyingi savolga o'tish
- Har bir to'g'ri javob: +0.5 QBC

## 🛡️ Xavfsizlik

- **Copy/Paste blokirovka** - Forward va nusxalashni oldini olish
- **Screenshot blokirovka** - Savol davomida boshqa buyruqlar ishlash uchun
- **Test vaqti** - Vaqt tugaganda avtomatik o'tish

## 🐛 Ehtimoliy Muammolar va Yechimi

### Bot token to'g'ri emas
- `.env` faylida `BOT_TOKEN`ni tekshiring
- BotFather dan yangi token oling

### Kanal ID to'g'ri emas
- Kanal ID (negative): `-1001234567890`
- Kanalga qo'shilgang botga ruxsat bering

### JSON error
- `data/` papkasi yaratilgan-mi tekshiring
- `data/users.json` va `data/questions.json` mavjud-mi

## 📝 Savollar va Javoblar

Savollarni `.json` faylida qo'shish yoki admin /admin buyrug'i bilan qo'shish mumkin.

## 🎓 O'quv Resurslar

- [Aiogram 3 Dokumentatsiyasi](https://docs.aiogram.dev/)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [Python Async/Await](https://docs.python.org/3/library/asyncio.html)

## 📞 Aloqa

Muammolar uchun GitHub issues qo'ying yoki admin bilan bog'laning.

---

**Tayyorlagan:** Quiz Bot Team  
**Versiya:** 1.0.0  
**Sana:** 15.11.2025
