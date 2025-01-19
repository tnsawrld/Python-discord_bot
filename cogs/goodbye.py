import discord
import easy_pil
import random
import os
from discord.ext import commands

#--------------------[LEAVE MESSAGE]-----------------------------
class MemberLeaveHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"[File] : {__name__} berhasil dijalankan!")

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        print(f"[Event] : on_member_leave berhasil berjalan!")

        ch_welcome = member.guild.system_channel
        if ch_welcome is None:
            print(f"[Event] : system channel terdeteksi >> (None)!")
            return

        try:
            #Check the image folder
            img = [image for image in os.listdir("./cogs/img_server") if image.endswith(('png', 'jpg', 'jpeg'))]
            if not img:
                print(f"[Event] : Folder image tak terdeteksi! >> (None)!")
                return
            random_image = random.choice(img)
            print(f"[Event] : Gambar dipilih >> {random_image}!")

            #Image processing process / edit
            try:
                background_edit = easy_pil.Editor(f"./cogs/img_server/{random_image}").resize((1920, 1080))
                if member.avatar:
                    profil_img = await easy_pil.load_image_async(str(member.avatar.url))
                else:
                    profil_img = await easy_pil.load_image_async("default_avatar.png")  # Ganti dengan avatar default

                profil_edit = easy_pil.Editor(profil_img).resize((250, 250)).circle_image()

                font_big = easy_pil.Font.poppins(size=90, variant="bold")
                font_small = easy_pil.Font.poppins(size=50, variant="bold")

                background_edit.paste(profil_edit, (835, 340))
                background_edit.ellipse((835, 340), 250, 250, outline="white", stroke_width=6)

                background_edit.text((960, 620), f"Selamat tinggal {member.name}!", color="white", align="center", font=font_big)
                background_edit.text((960, 740), f"Terima kasih sudah bergabung ke dalam server {member.guild.name}!", color="white", align="center", font=font_small)

                file_img = discord.File(fp=background_edit.image_bytes, filename=random_image)
            except Exception as e:
                print(f"Error saat memproses gambar: {e}")
                return
            #send images to the discord channel
            try:
                await ch_welcome.send(f"Selamat tinggal {member.name}!, hati-hati dijalan!")
                await ch_welcome.send(file=file_img)
                print("[Event] Pesan selamat tinggal berhasil dikirim.")
            except Exception as e:
                print(f"[Event] : Error saat mengirim pesan atau gambar >> {e}!")

        except Exception as e:
            print(f"[Event] : Terjadi error di event on_member_leave >> {e}!")

async def setup(bot):
    await bot.add_cog(MemberLeaveHandler(bot))
