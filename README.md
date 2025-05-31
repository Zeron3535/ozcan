BanaRandevu - Randevu Sistemi
BanaRandevu, profesyoneller ve müşteriler arasında randevu yönetimini kolaylaştıran bir web uygulamasıdır. Sistem, profesyonellerin hizmetlerini listelemesine, çalışma saatlerini belirlemesine ve randevularını yönetmesine olanak tanır. Müşteriler ise profesyonelleri kategorilere göre arayabilir, profil bilgilerini görüntüleyebilir ve randevu alabilir.

İçindekiler
Özellikler
Kurulum
Yapılandırma
Kullanım
Yönetici Paneli
Profesyonel Kullanıcılar
Müşteriler
Geliştirme
Dağıtım
Lisans
Özellikler
Genel Özellikler
Kullanıcı dostu, modern ve duyarlı arayüz
Çoklu kullanıcı tipleri (yönetici, profesyonel)
Kategori ve uzmanlık alanlarına göre arama
Telegram entegrasyonu ile bildirimler
Profesyoneller İçin
Özelleştirilebilir profil sayfaları
Hizmet ve fiyat yönetimi
Çalışma saatleri belirleme
Randevu onaylama ve reddetme
Online ve yüz yüze görüşme seçenekleri
Yöneticiler İçin
Kullanıcı dostu yönetim paneli
Kullanıcı yönetimi (ekleme, düzenleme, silme)
Kategori ve uzmanlık alanları yönetimi
Site ayarları yapılandırması
Telegram bot entegrasyonu
Müşteriler İçin
Üyelik gerektirmeyen randevu sistemi
Profesyonelleri kategorilere göre arama
Detaylı profesyonel profilleri görüntüleme
Kolay randevu oluşturma
Kurulum
Gereksinimler
Python 3.8 veya üzeri
Django 5.0 veya üzeri
Diğer bağımlılıklar için requirements.txt dosyası
Adımlar
Projeyi klonlayın:
git clone https://github.com/kullanici/banarandevu.git
cd banarandevu
Sanal ortam oluşturun ve etkinleştirin:
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
Bağımlılıkları yükleyin:
pip install -r requirements.txt
Veritabanı migrasyonlarını uygulayın:
python manage.py migrate
Yönetici kullanıcısı oluşturun:
python manage.py createsuperuser
Örnek verileri yükleyin (isteğe bağlı):
python manage.py populate_sample_data
Geliştirme sunucusunu başlatın:
python manage.py runserver
Tarayıcınızda http://127.0.0.1:8000 adresine giderek uygulamayı görüntüleyin.
Yapılandırma
Temel Ayarlar
Temel ayarlar randevusistemi/settings.py dosyasında bulunmaktadır. Önemli ayarlar:

DEBUG: Geliştirme modunu açar/kapatır. Canlı ortamda False olmalıdır.
SECRET_KEY: Uygulama güvenlik anahtarı. Canlı ortamda değiştirilmelidir.
ALLOWED_HOSTS: İzin verilen host adları.
DATABASES: Veritabanı yapılandırması.
TELEGRAM_BOT_TOKEN: Telegram bot entegrasyonu için token.
Site Ayarları
Site ayarları yönetici panelinden yapılandırılabilir:

Yönetici paneline giriş yapın: http://127.0.0.1:8000/yonetim/
"Site Ayarları" bölümüne gidin.
Aşağıdaki ayarları yapılandırın:
Site adı ve karşılama mesajı
İletişim bilgileri
Sosyal medya bağlantıları
Telegram bot ayarları
SEO ayarları
Telegram Bot Entegrasyonu
Şifre sıfırlama talepleri ve diğer bildirimler için Telegram bot entegrasyonu:

BotFather üzerinden bir Telegram bot oluşturun ve token alın.
settings.py dosyasında TELEGRAM_BOT_TOKEN değişkenini ayarlayın.
Yönetici panelinden "Site Ayarları" > "Telegram Bot" bölümüne gidin.
"Telegram Bot Aktif" seçeneğini işaretleyin.
"Telegram Yönetici ID'leri" alanına virgülle ayrılmış Telegram kullanıcı ID'lerini girin.
Kullanım
Yönetici Paneli
Yönetici paneline erişmek için:

http://127.0.0.1:8000/yonetim/ adresine gidin.
Süper kullanıcı bilgilerinizle giriş yapın.
Kullanıcı Yönetimi
"Kullanıcılar" bölümüne tıklayın.
Kullanıcıları görüntüleyin, düzenleyin veya silin.
"Yeni Kullanıcı" butonuna tıklayarak yeni kullanıcı ekleyin.
Kullanıcı bilgilerini doldurun:
Kullanıcı adı ve şifre
Ad, soyad ve e-posta
Kullanıcı tipi (Yönetici veya Profesyonel)
Üyelik durumu ve bitiş tarihi
Kategori ve Uzmanlık Alanları Yönetimi
"Kategoriler" veya "Uzman Türleri" bölümüne gidin.
Mevcut kayıtları görüntüleyin, düzenleyin veya silin.
"Ekle" butonuna tıklayarak yeni kayıt oluşturun.
Site Ayarları
"Site Ayarları" bölümüne gidin.
Genel site ayarlarını, iletişim bilgilerini ve Telegram bot ayarlarını yapılandırın.
Profesyonel Kullanıcılar
Profesyonel kullanıcılar için kullanım adımları:

http://127.0.0.1:8000/hesaplar/giris/ adresinden giriş yapın.
İlk girişte profil oluşturmanız istenecektir.
Profil bilgilerinizi doldurun:
Kategori ve uzmanlık alanı
Kısa tanıtım ve detaylı bilgiler
Şehir ve deneyim yılı
Online/yüz yüze hizmet seçenekleri
Hizmet Yönetimi
"Hizmetler" menüsüne tıklayın.
"Yeni Hizmet Ekle" butonuna tıklayın.
Hizmet bilgilerini doldurun:
Hizmet adı ve açıklaması
Süre ve görüşme tipi
Fiyat bilgisi (isteğe bağlı)
Çalışma Saatleri
"Çalışma Saatleri" menüsüne tıklayın.
Her gün için çalışma saatlerinizi belirleyin.
Aktif olmayan günleri işaretleyin.
Randevu Yönetimi
"Randevular" menüsüne tıklayın.
Bekleyen, onaylanan ve geçmiş randevuları görüntüleyin.
Randevuları onaylayın veya reddedin.
Müşteriler
Müşteriler için kullanım adımları (üyelik gerektirmez):

Ana sayfada kategorilere göz atın veya arama yapın.
Profesyonel profillerini inceleyin.
Randevu almak istediğiniz profesyoneli seçin.
Uygun bir hizmet ve zaman dilimi seçin.
İletişim bilgilerinizi girin ve randevuyu onaylayın.
Geliştirme
Proje Yapısı
banarandevu/
├── accounts/            # Kullanıcı yönetimi
├── appointments/        # Randevu yönetimi
├── main/                # Ana sayfa ve genel görünümler
├── professionals/       # Profesyonel profilleri
├── randevusistemi/      # Proje ayarları
├── static/              # Statik dosyalar (CSS, JS)
├── templates/           # HTML şablonları
└── yonetim/             # Özel yönetici paneli
Geliştirme Ortamı
DEBUG modunu açık tutun:
# settings.py
DEBUG = True
Statik dosyaları toplamak için:
python manage.py collectstatic
Dil dosyalarını derlemek için:
python manage.py compilemessages
Testleri çalıştırmak için:
python manage.py test

Dağıtım
Canlı ortama dağıtım için öneriler:

DEBUG modunu kapatın:
# settings.py
DEBUG = False
Güvenli bir SECRET_KEY oluşturun.

ALLOWED_HOSTS listesini güncelleyin:

ALLOWED_HOSTS = ['www.example.com', 'example.com']
Statik dosyaları toplayın:
python manage.py collectstatic
Bir WSGI sunucusu kullanın (Gunicorn, uWSGI vb.):
gunicorn randevusistemi.wsgi:application
Bir web sunucusu ile proxy yapın (Nginx, Apache vb.).

HTTPS kullanın ve güvenlik ayarlarını yapılandırın.

Lisans
Bu proje MIT Lisansı altında lisanslanmıştır.

© 2025 BanaRandevu. Tüm hakları saklıdır.
