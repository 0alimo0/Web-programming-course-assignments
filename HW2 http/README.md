سوال یک : 

تفاوت نسخه‌های HTTP:

HTTP/0.9: خیلی ساده بود؛ فقط متد GET داشت، هدر و کد وضعیت نداشت، پاسخ فقط HTML بود و بعد از هر پاسخ اتصال بسته می‌شد.
HTTP/1.0: هدرها، کدهای وضعیت، متدهای GET/POST/HEAD و هدرهایی مثل Content-Type اضافه شد. اتصال به‌صورت پیش‌فرض غیرpersistent بود؛ یعنی برای هر درخواست معمولاً اتصال جدید باز می‌شد.
HTTP/1.1: اتصال keep-alive پیش‌فرض شد، هدر Host اجباری شد و virtual hosting راحت‌تر شد. همچنین pipelining، chunked transfer، Range و مکانیزم‌های کش مثل ETag و Cache-Control اضافه شد.
HTTP/2: باینری شد، multiplexing روی یک اتصال TCP دارد، هدرها با HPACK فشرده می‌شوند، server push و priority دارد. مشکل اصلی‌اش این است که هنوز روی TCP است و می‌تواند دچار HOL blocking شود.
HTTP/3: روی QUIC و در واقع روی UDP ساخته شده، TLS 1.3 دارد، multiplexing بدون HOL blocking TCP انجام می‌دهد، handshake سریع‌تر و 0-RTT دارد و connection migration هم دارد.

چرا HTTP/3 از UDP استفاده می‌کند؟
چون QUIC روی UDP پیاده‌سازی شده و خودش reliability، ordering، congestion control و رمزنگاری را انجام می‌دهد. با این کار از HOL blocking TCP خلاص می‌شویم، handshake کم‌تاخیرتر می‌شود و پیاده‌سازی در user-space راحت‌تر است. در واقع UDP فقط بستر انتقال است و QUIC همه‌چیز را مدیریت می‌کند.


سوال دو : 

الف)
در ارتباطات stateless، سرور بین درخواست‌ها حالت یا context کلاینت را نگه نمی‌دارد و هر درخواست مستقل است. در stateful، سرور وضعیت قبلی کلاینت را نگه می‌دارد و درخواست بعدی به آن وابسته است.

ب)
پروتکل HTTP ذاتا stateless است؛ یعنی هر درخواست جداگانه بررسی می‌شود و سرور به‌خاطر نمی‌آورد درخواست قبلی چه بوده. برای حل مشکلاتی مثل لاگین، سبد خرید و شخصی‌سازی، معمولا از cookie، session id، توکن/JWT، hidden field یا URL rewriting استفاده می‌شود تا حالت کاربر بین درخواست‌ها حفظ شود. بعضی از این راه‌حل‌ها خودشان state را سمت کلاینت نگه می‌دارند و بعضی سمت سرور.


سوال سه : 

الف)
در مدل client/server معمولا کلاینت شروع‌کننده است و سرور فقط جواب درخواست را می‌دهد. سرور نمی‌تواند بدون درخواست قبلی داده بفرستد. برای webhook، چت و alerting که سرور باید سریع خبر بدهد، این محدودیت دردسر می‌سازد. ademas کلاینت ممکن است پشت NAT یا فایروال باشد و IP عمومی نداشته باشد، پس سرور نمی‌تواند راحت به کلاینت وصل شود.

ب)
Polling: کلاینت هر چند وقت یک‌بار درخواست می‌زند؛ ساده است ولی تأخیر و ترافیک اضافه دارد.
Long polling: سرور درخواست را باز نگه می‌دارد تا event بیاید یا timeout شود؛ تأخیر کمتر است ولی منابع و اتصال بیشتری مصرف می‌شود.
SSE: سرور از طریق HTTP یک جریان یک‌طرفه event می‌فرستد؛ برای alert و اعلان خوب است ولی دوطرفه نیست.
WebSocket: با upgrade از HTTP یک اتصال full-duplex می‌سازیم؛ برای چت عالی است ولی statefulتر است و scaling/proxy سخت‌تر دارد.
HTTP/2 server push: سرور می‌تواند منابع را push کند؛ ولی برای پیام‌رسانی عمومی مناسب نیست و در مرورگرها عملاً کنار گذاشته شده.
Push notification، message broker و WebRTC data channel هم برای اعلان و ارتباط real-time استفاده می‌شوند.


سوال چهار : 

برای   ss://asghar:1234!@ss.myproxy.com:1234#shadowSocks1

scheme: ss
userinfo: asghar:1234!
username: asghar
password: 1234!
host: ss.myproxy.com
port: 1234
path: خالی
query: خالی
fragment: shadowSocks1 که معمولا برچسسب یا نام کانفیگ است.


سوال پنج : 

1- 500 Internal Server Error؛ اگر کل سرویس موقتاً unavailable است، 503 Service Unavailable هم مناسب است.
2- 401 Unauthorized؛ بهتر است پیام کلی باشد تا username enumeration نشود. 404 برای login مناسب نیست.
3- 301 Moved Permanently؛ اگر می‌خواهیم متد و بدنه حفظ شود 308، و اگر انتقال موقت است 302 یا 307.
4- 429 Too Many Requests.
5- 200 OK؛ اگر بدنه نداریم 204 No Content هم قابل قبول است.
6- 403 Forbidden و یا 451 Unavailable For Legal Reasons هم مناسب است.


سوال شش : 

1- caching proxy / mirror / reverse proxy برای مخازن apt. این سرور پکیج‌ها را کش می‌کند یا از upstream می‌گیرد و به کلاینت‌های داخلی می‌دهد.
2- reverse proxy / load balancer با مسیریابی جغرافیایی که معمولا همراه با GeoDNS یا GSLB کار می‌کند.
3- reverse proxy به عنوان auth gateway / authenticating proxy که جلوی سرویس قدیمی قرار می‌گیرد و اول احراز هویت را انجام می‌دهد.



از هوش مصنوعی deepseek به عنوان یک ابزار جستوجوگر هوشمند استفاده شده است. 
