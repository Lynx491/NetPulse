# NetPulse 0.1

## Tanım

**Bu proje birden fazla ajanın birden fazla monitor'e veri göndermesini sağlar**

### Veriler

1. CPU sıcaklığı
2. GPU sıcakığı
3. Ram kullanımı
4. Swap kullanımı
5. İndirme hızı
6. Yükleme hızı
7. Çekirdek başına düşen işlemci sıcaklığı

## Görseller


| ss1                                               | ss2                                               | ss3                                               |
| ------------------------------------------------- | ------------------------------------------------- | ------------------------------------------------- |
| ![1791126892810](images/readme/1791126892810.png) | ![1791126906180](images/readme/1791126906180.png) | ![1791126933027](images/readme/1791126933027.png) |
|                                                   |                                                   |                                                   |

## Özellikler

* Birden fazla ajan birden fazla monitore aynanda veri gönderebiliyor.
* kasmayan, modern ve şık bir GUI.
* SQL ile ajan verileri toplanıyor.

## Teknoloji Yığını & Gereksinimler

### Sunucu

* Sunucu FastApi ile Asenkron şekilde yazıldı, aynanda dinlerken aynanda veri gönderebiliyor.
* Veritabanı olarak Sql 8.0, SqlModel ile asenkron şekilde yazıldı.

### Ajan

* platform ile bilgisyar adı çekildi
* psutil ile bilgisiyardan bilgiler toplandı
* aiohttp ile asenkron şekilde sunucuya veri gönderildi

### İstemci

* Flet ile arayüz tasarlandı flet-charts ile grafik tablosu oluşturuldu
* aiohttp ile asenkron şekilde sunucu sürekli dinlendi

## Kurulum & Çalıştırma

python 3.12.3'ü indirin.

### Windows

Windows için [indir](https://www.python.org/downloads/release/python-3123/)

### MaxOS

```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

```
brew install python
```

`python3 --version`

### Linux

#### Debian, Ubuntu ve Türvleri (Linux Mint)

```
sudo apt install python3
```

#### Fedora ve Türevleri

```
sudo dnf install python3
```

#### Arch ve Türevleri

```
sudo pacman -S python
```

#### Pisi Linux ve Türevleri

```
sudo pisi it python3
```

### Gerekli bağımlılıkları indirme

```
pip install -r requirements.txt
```

### Çalıştır

```
source venv/bin/activate
```

#### Sunucuyu çaıştır 

```
python3 main.py
```

#### Ajanı çalıştır

```
python3 agent.py
```

#### İstemciyi çalıştır

```
python3 client.py
```
