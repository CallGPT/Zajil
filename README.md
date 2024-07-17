
# مشروع FoodPhone 🌟

## مقدمة 🎉
## URL 
```
https://api.call-gpt.tech
```

ده مشروع مكتوب بـ Flask عشان تسجل الأوامر الصوتية والكتابية، وتطلع الفواتير وتاريخ المحادثات. فيه نهايات API متعددة:
1. `/api/v1/order/voice/<chatId>` - لتحويل النص لصوت
2. `/api/v1/order/chat/<chatId>` - للدردشة
3. `/api/v1/order/history/<chatId>` - لعرض تاريخ الدردشة
4. `/api/v1/order/close/<chatId>` - لغلق الطلب وتوليد الفاتورة

 
## الشرح 📝

### 1. تحويل النص لصوت 📋
لما حد عايز يحول نص لصوت، هيبعت طلب POST لـ `/api/v1/order/voice/<chatId>` ومعاه JSON فيه `text`. هنستخدم AI عشان نرد على النص، وهنولد صوت للرد.

- البيانات اللي تبعتها لازم تكون زي كده:
  ```json
  {
    "text": "النص هنا"
  }
  ```

### 2. الدردشة 🔐
لما حد عايز يدردش، هيبعت طلب POST لـ `/api/v1/order/chat/<chatId>` ومعاه JSON فيه `text`. هنستخدم AI عشان نرد على النص ونسجل الدردشة في قاعدة البيانات.

- البيانات اللي تبعتها لازم تكون زي كده:
  ```json
  {
    "text": "النص هنا"
  }
  ```

### 3. عرض تاريخ الدردشة ♻️
لما حد عايز يشوف تاريخ الدردشة، هيبعت طلب GET لـ `/api/v1/order/history/<chatId>`. هنرجع كل الرسائل اللي اتسجلت في الدردشة دي.

### 4. غلق الطلب وتوليد الفاتورة ✅
لما حد عايز يغلق الطلب ويولد فاتورة، هيبعت طلب GET لـ `/api/v1/order/close/<chatId>`. هنستخدم AI عشان نلخص الطلب ونحفظه كفاتورة.