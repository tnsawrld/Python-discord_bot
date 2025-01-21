# Python Discord Bot

## About
Ini adalah bot simple yang dibuat dengan `Python` menggunakan libary `discord.py`. Pembuatan bot ini ditujukan untuk `SAMP` dalam memanage server

## Features
- **Slash Commands**: Berinteraksi dengan bot dengan mudah menggunakan sistem slash commands Discord.
- **MySQL**: Menggunakan system database MySQL.
- **Welcome and Goodbye**: Membuat ucapan selamat datang ata selamat tinggal disertai foto background yang bebas custom.
- **UCP Register**: Dapat melakukan register UCP untuk SAMP. 

## Preview
1. **UCP Registration**</br>
![Image](https://github.com/user-attachments/assets/088717c9-248f-4f4b-a165-57f517510e1a)

2. **Using config.ini for custom**</br>
![Image](https://github.com/user-attachments/assets/aa555dc6-541e-46dd-85b7-01c097e57044)

3. **Preview Welcome Message**</br>
![Image](https://github.com/user-attachments/assets/b288bd72-cb72-4815-a151-3b6bfeef096d)

4. **Preview Goodbye Message**</br>
![Image](https://github.com/user-attachments/assets/bdc96a79-6af0-4199-99b9-74d84012ee6d)

## Setup Instructions

1. **Clone the Repository:**
   Download melalui `download zip` atau menggunakan git clone :
   ```bash
   git clone https://github.com/tnsawrld/Python-discord_bot.git
   ```

2. **Install Dependencies:**
   Pastikan anda memiliki Python dengan versi 3.8 or atau lebih tinggi :
   ```bash
   pip install discord.py
   ```
   ```bash
   pip install easy-pil
   ```
   ```bash
   pip install mysql-connector-python
   ```

3. **Setup the BOT :**
   - Tambahkan token, database ke config.ini
   - Periksa setiap file untuk mengganti database

4. **Run the Bot:**
   Klik run di VScode atau menggunakan `terminal`:
   ```bash
   python main.py
   ```

5. **Sync Slash Commands:**
   Bot secara otomatis menyinkronkan perintah garis miring saat startup.

## Example Commands

### Public Commands
- `/clear`: Untuk menghapus pesan sesuai jumlah.
- `/hello`: Hanya menyapa.
- `/ping`: Mendapatkan ping dari bot.
- `/dm`: Mengirim pesan pribadi melalui bot.

### SAMP Commands
- `/register`: Melakukan register UCP ke database.

## Important
Setup bot di [Discord Developer](https://discord.com/developers/applications):
- Privileged Gateway Intents semua harus on

## About Me
- [Youtube](update.md)

## About Me
- [Youtube](https://www.youtube.com/@Tnsawrld)
