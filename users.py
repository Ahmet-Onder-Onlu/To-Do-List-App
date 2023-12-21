"""path = "userRegisters.txt" -> Buradan kullanıcı adına ve şifresine bakıp
doğru giriş yaılmalı aksi takdirde hata alınır.
file = open(path, "w")
file.write("* * * * * User Registers * * * * *")
file.close() Önce bunu çalıştırıp sonra yoruma aldım"""

# Kullanıcı adı ve şifresi dosyaya yazılır.
def users(user_name, user_password):
    path = "userRegisters.txt"
    file = open(path, "a")
    file.write(f" {user_name} {user_password}")



# Sifre dogruysa 1 döndür, sifre yanlıs ise -1 ve kisi yoksa 0 dondur.
def account_control(name, password, user_info):
    if name in user_info.keys():
        if user_info[name] == password:
            return 1
        else:
            return -1

    else:
        return 0
