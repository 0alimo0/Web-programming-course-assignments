<div dir="rtl" style="text-align: right; font-family: Tahoma, Vazirmatn, Arial, sans-serif; line-height: 1.9; color: #222;">

  <h3 style="color: #1a73e8; margin-top: 24px;">سوال یک :</h3>

  <p><strong>تفاوت نسخه‌های <span dir="ltr">HTTP</span>:</strong></p>
  <ul>
    <li><strong><span dir="ltr">HTTP/0.9</span>:</strong> خیلی ساده بود؛ فقط متد <code dir="ltr">GET</code> داشت، هدر و کد وضعیت نداشت، پاسخ فقط <span dir="ltr">HTML</span> بود و بعد از هر پاسخ اتصال بسته می‌شد.</li>
    <li><strong><span dir="ltr">HTTP/1.0</span>:</strong> هدرها، کدهای وضعیت، متدهای <code dir="ltr">GET / POST / HEAD</code> و هدرهایی مثل <code dir="ltr">Content-Type</code> اضافه شد. اتصال به‌صورت پیش‌فرض غیر<span dir="ltr">persistent</span> بود؛ یعنی برای هر درخواست معمولا اتصال جدید باز می‌شد.</li>
    <li><strong><span dir="ltr">HTTP/1.1</span>:</strong> اتصال <span dir="ltr">keep-alive</span> پیش‌فرض شد، هدر <code dir="ltr">Host</code> اجباری شد و <span dir="ltr">virtual hosting</span> راحت‌تر شد. همچنین <span dir="ltr">pipelining</span>، <span dir="ltr">chunked transfer</span>، <span dir="ltr">Range</span> و مکانیزم‌های کش مثل <code dir="ltr">ETag</code> و <code dir="ltr">Cache-Control</code> اضافه شد.</li>
    <li><strong><span dir="ltr">HTTP/2</span>:</strong> باینری شد، <span dir="ltr">multiplexing</span> روی یک اتصال <span dir="ltr">TCP</span> دارد، هدرها با <span dir="ltr">HPACK</span> فشرده می‌شوند، <span dir="ltr">server push</span> و <span dir="ltr">priority</span> دارد. مشکل اصلی‌اش این است که هنوز روی <span dir="ltr">TCP</span> است و می‌تواند دچار <span dir="ltr">HOL blocking</span> شود.</li>
    <li><strong><span dir="ltr">HTTP/3</span>:</strong> روی <span dir="ltr">QUIC</span> و در واقع روی <span dir="ltr">UDP</span> ساخته شده، <span dir="ltr">TLS 1.3</span> دارد، <span dir="ltr">multiplexing</span> بدون <span dir="ltr">TCP HOL blocking</span> انجام می‌دهد، <span dir="ltr">handshake</span> سریع‌تر و <span dir="ltr">0-RTT</span> دارد و <span dir="ltr">connection migration</span> هم دارد.</li>
  </ul>

  <p><strong>چرا <span dir="ltr">HTTP/3</span> از <span dir="ltr">UDP</span> استفاده می‌کند؟</strong></p>
  <p>چون <span dir="ltr">QUIC</span> روی <span dir="ltr">UDP</span> پیاده‌سازی شده و خودش <span dir="ltr">reliability</span>، <span dir="ltr">ordering</span>، <span dir="ltr">congestion control</span> و رمزنگاری را انجام می‌دهد. با این کار از <span dir="ltr">HOL blocking TCP</span> خلاص می‌شویم، <span dir="ltr">handshake</span> کم‌تاخیرتر می‌شود و پیاده‌سازی در <span dir="ltr">user-space</span> راحت‌تر است. در واقع <span dir="ltr">UDP</span> فقط بستر انتقال است و <span dir="ltr">QUIC</span> همه‌چیز را مدیریت می‌کند.</p>

  <hr style="border: 0; border-top: 1px solid #ddd; margin: 20px 0;">

  <h3 style="color: #1a73e8;">سوال دو :</h3>

  <p><strong>الف)</strong><br>
  در ارتباطات <span dir="ltr">stateless</span>، سرور بین درخواست‌ها حالت یا <span dir="ltr">context</span> کلاینت را نگه نمی‌دارد و هر درخواست مستقل است. در <span dir="ltr">stateful</span>، سرور وضعیت قبلی کلاینت را نگه می‌دارد و درخواست بعدی به آن وابسته است.</p>

  <p><strong>ب)</strong><br>
  پروتکل <span dir="ltr">HTTP</span> ذاتا <span dir="ltr">stateless</span> است؛ یعنی هر درخواست جداگانه بررسی می‌شود و سرور به‌خاطر نمی‌اورد درخواست قبلی چه بوده. برای حل مشکلاتی مثل لاگین، سبد خرید و شخصی‌سازی، معمولا از <span dir="ltr">cookie</span>، <span dir="ltr">session id</span>، توکن / <span dir="ltr">JWT</span>، <span dir="ltr">hidden field</span> یا <span dir="ltr">URL rewriting</span> استفاده می‌شود تا حالت کاربر بین درخواست‌ها حفظ شود. بعضی از این راه‌حل‌ها خودشان <span dir="ltr">state</span> را سمت کلاینت نگه می‌دارند و بعضی سمت سرور.</p>

  <hr style="border: 0; border-top: 1px solid #ddd; margin: 20px 0;">

  <h3 style="color: #1a73e8;">سوال سه :</h3>

  <p><strong>الف)</strong><br>
  در مدل <span dir="ltr">client / server</span> معمولاً کلاینت شروع‌کننده است و سرور فقط جواب درخواست را می‌دهد. سرور نمی‌تواند بدون درخواست قبلی داده بفرستد. برای <span dir="ltr">webhook</span>، چت و <span dir="ltr">alerting</span> که سرور باید سریع خبر بدهد، این محدودیت دردسر می‌سازد. علاوه بر این کلاینت ممکن است پشت <span dir="ltr">NAT</span> یا فایروال باشد و <span dir="ltr">IP</span> عمومی نداشته باشد، پس سرور نمی‌تواند راحت به کلاینت وصل شود.</p>

  <p><strong>ب)</strong></p>
  <ul>
    <li><strong><span dir="ltr">Polling</span>:</strong> کلاینت هر چند وقت یک‌بار درخواست می‌زند؛ ساده است ولی تأخیر و ترافیک اضافه دارد.</li>
    <li><strong><span dir="ltr">Long polling</span>:</strong> سرور درخواست را باز نگه می‌دارد تا <span dir="ltr">event</span> بیاید یا <span dir="ltr">timeout</span> شود؛ تأخیر کمتر است ولی منابع و اتصال بیشتری مصرف می‌شود.</li>
    <li><strong><span dir="ltr">SSE</span>:</strong> سرور از طریق <span dir="ltr">HTTP</span> یک جریان یک‌طرفه <span dir="ltr">event</span> می‌فرستد؛ برای <span dir="ltr">alert</span> و اعلان خوب است ولی دوطرفه نیست.</li>
    <li><strong><span dir="ltr">WebSocket</span>:</strong> با <span dir="ltr">upgrade</span> از <span dir="ltr">HTTP</span> یک اتصال <span dir="ltr">full-duplex</span> می‌سازیم؛ برای چت عالی است ولی <span dir="ltr">stateful</span>تر است و <span dir="ltr">scaling / proxy</span> سخت‌تری دارد.</li>
    <li><strong><span dir="ltr">HTTP/2 server push</span>:</strong> سرور می‌تواند منابع را <span dir="ltr">push</span> کند؛ ولی برای پیام‌رسانی عمومی مناسب نیست و در مرورگرها عملاً کنار گذاشته شده است.</li>
    <li><span dir="ltr">Push notification</span>، <span dir="ltr">message broker</span> و <span dir="ltr">WebRTC data channel</span> هم برای اعلان و ارتباط <span dir="ltr">real-time</span> استفاده می‌شوند.</li>
  </ul>

  <hr style="border: 0; border-top: 1px solid #ddd; margin: 20px 0;">

  <h3 style="color: #1a73e8;">سوال چهار :</h3>

  <p>برای لینک: <br>
  <code dir="ltr" style="background: #f4f4f4; padding: 3px 6px; border-radius: 4px; display: inline-block; margin: 4px 0;">ss://asghar:1234!@ss.myproxy.com:1234#shadowSocks1</code></p>

  <ul style="list-style-type: none; padding-right: 0;">
    <li><span dir="ltr" style="display: inline-block; font-family: monospace;">• scheme: ss</span></li>
    <li><span dir="ltr" style="display: inline-block; font-family: monospace;">• userinfo: asghar:1234!</span></li>
    <li><span dir="ltr" style="display: inline-block; font-family: monospace;">• username: asghar</span></li>
    <li><span dir="ltr" style="display: inline-block; font-family: monospace;">• password: 1234!</span></li>
    <li><span dir="ltr" style="display: inline-block; font-family: monospace;">• host: ss.myproxy.com</span></li>
    <li><span dir="ltr" style="display: inline-block; font-family: monospace;">• port: 1234</span></li>
    <li><span dir="ltr" style="display: inline-block; font-family: monospace;">• path:</span> خالی</li>
    <li><span dir="ltr" style="display: inline-block; font-family: monospace;">• query:</span> خالی</li>
    <li><span dir="ltr" style="display: inline-block; font-family: monospace;">• fragment: shadowSocks1</span> (معمولا برچسب یا نام کانفیگ است)</li>
  </ul>

  <hr style="border: 0; border-top: 1px solid #ddd; margin: 20px 0;">

  <h3 style="color: #1a73e8;">سوال پنج :</h3>

  <ol>
    <li><span dir="ltr"><strong>500 Internal Server Error</strong></span>؛ اگر کل سرویس موقتا <span dir="ltr">unavailable</span> است، <span dir="ltr"><strong>503 Service Unavailable</strong></span> هم مناسب است.</li>
    <li><span dir="ltr"><strong>401 Unauthorized</strong></span>؛ بهتر است پیام کلی باشد تا <span dir="ltr">username enumeration</span> نشود. کد <span dir="ltr">404</span> برای <span dir="ltr">login</span> مناسب نیست.</li>
    <li><span dir="ltr"><strong>301 Moved Permanently</strong></span>؛ اگر می‌خواهیم متد و بدنه حفظ شود <span dir="ltr"><strong>308</strong></span>، و اگر انتقال موقت است <span dir="ltr"><strong>302</strong></span> یا <span dir="ltr"><strong>307</strong></span>.</li>
    <li><span dir="ltr"><strong>429 Too Many Requests</strong></span>.</li>
    <li><span dir="ltr"><strong>200 OK</strong></span>؛ اگر بدنه نداریم <span dir="ltr"><strong>204 No Content</strong></span> هم قابل قبول است.</li>
    <li><span dir="ltr"><strong>403 Forbidden</strong></span> و یا <span dir="ltr"><strong>451 Unavailable For Legal Reasons</strong></span> هم مناسب است.</li>
  </ol>

  <hr style="border: 0; border-top: 1px solid #ddd; margin: 20px 0;">

  <h3 style="color: #1a73e8;">سوال شش :</h3>

  <ol>
    <li><span dir="ltr"><strong>Caching proxy / Mirror / Reverse proxy</strong></span> برای مخازن <span dir="ltr">apt</span>. این سرور پکیج‌ها را کش می‌کند یا از <span dir="ltr">upstream</span> می‌گیرد و به کلاینت‌های داخلی می‌دهد.</li>
    <li><span dir="ltr"><strong>Reverse proxy / Load balancer</strong></span> با مسیریابی جغرافیایی که معمولا همراه با <span dir="ltr">GeoDNS</span> یا <span dir="ltr">GSLB</span> کار می‌کند.</li>
    <li><span dir="ltr"><strong>Reverse proxy</strong></span> به عنوان <span dir="ltr">auth gateway / authenticating proxy</span> که جلوی سرویس قدیمی قرار می‌گیرد و اول احراز هویت را انجام می‌دهد.</li>
  </ol>

  <hr style="border: 0; border-top: 1px solid #ddd; margin: 20px 0;">

  <p style="font-size: 0.9em; color: #666;">از هوش مصنوعی <span dir="ltr">DeepSeek</span> به عنوان یک ابزار جست‌وجوگر هوشمند استفاده شده است. (ازش سوال میپرسیدم)</p>
  در آخر هم متن رو به AI studio دادم تا مشکل RTL نبودنش رو درست کنه (خودش یه سری جاها رو بولد و ... هم کرد)

</div>
