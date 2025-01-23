def Check_Username(conection_db, username):
    cursor = conection_db.cursor()
    cursor.execute("SELECT COUNT(username) FROM players WHERE BINARY username = %s", (username,))
    result = cursor.fetchone()
    return result[0] > 0

def Get_UCP(conection_db, discordid):
    cursor = conection_db.cursor()
    cursor.execute("SELECT ucp FROM playerucp WHERE DiscordID = %s", (discordid,))
    result = cursor.fetchone()
    return result