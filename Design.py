# Tasarım ve fonksiyonellik için gerekli
#class ve modüller import edildi(nesne oluşturuldu)
import tkinter as tk
from toDoList import ToDoList
from users import *

newToDoList = ToDoList()

#Kullanıcı login ve signUp yapabilmek için
#Kullnıcı adı ve şifresi boş olmaması kontrol
#edilerek userRegisters.txt ye kayıt edildi
path = "userRegisters.txt"
file = open(path, "r")
text = file.read()
file.close()
array_user = text.split(" ")
user_sign_in = {}
for i in range(0, len(array_user), 2):
    user_sign_in[array_user[i]] = array_user[i + 1]

#Farklı yerlerde kullanılacak global değerler oluşturuldu
global timer
timer= 0
global password

#Login sayfası 3 hatalı girişte hesap silinecek şekilde ayarlandı.
#Ve doğru girişte hesaba bağladı. Kayıtlı dosyadan veriler çekildi.
def login():
    username = username_entry.get()
    global password
    password = password_entry.get()

    global attention_message1, timer
    attention_message1 = tk.Label(root, text="", fg="red", bg="lightblue")
    attention_message1.place(x=130, y=145)

    get_control = account_control(username, password, user_sign_in)

    if get_control == 1:
        menu_page()

    elif get_control == -1:
        timer += 1
        attention_message1.config(text=f"Hatalı Şifre {timer} ")
        if timer == 3:
            attention_message1.config(text="Hesap Kapatıldı!")
            del user_sign_in[username]
            for i in user_sign_in.keys():
                users(i, user_sign_in[i])

    else:

        attention_message1.config(text="Hesap Bulunamadı")

#Kullanıcı kayıtlı değilse txt uzantılı dosyaya kayıt edildi.
def signup():
    username = username_entry.get()
    password = password_entry.get()

    attention_message1 = tk.Label(root, text="", fg="red", bg="lightblue")
    attention_message1.place(x=130, y=145)

    get_control = account_control(username, password, user_sign_in)

    if get_control == 1 or get_control == -1:
        attention_message1.config(text="Hesap Zaten Var")

    else:
        users(username, password)
        attention_message1.config(text="Successfully done.")
        menu_page()

#Kullanıcı uygulamadan çıkmak istediğinde çıkış butonuna basar.
def exit_program():
    root.destroy()  # Programı kapat

#Tasarladığımız ekranları bilgisayarın ortasına ve ayarlanmış taşır.
def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)

    window.geometry(f'{width}x{height}+{int(x)}+{int(y)}')

#Görev eklemek amaçlı sayfa tasarlandı aslında hepsi menu sayfasında
#Oluyor ancak ekran yenileniyor. Yani sayfa temizlenip yazılıyor.
def open_add_task_window():
    #Direkt görevler sınıfa gider ve txt PersonalDatas.txt dosyasına kayıt olur.
    def add_task():
        task_title = title_entry.get()
        task_content = content_entry.get()

        # Görev başlığını ve içeriğini ekrana yazdırma
        control = newToDoList.add_task(task_title, task_content)
        get_message = newToDoList.save_changes(password, control)
        task_label = tk.Label(menu_root, text=get_message)
        task_label.config(bg="lightgreen", fg="red")
        task_label.place(x=100, y=200)

    menu_root.withdraw()
    menu_page()
    # Görev başlığı ve içeriği için giriş alanları
    title_label = tk.Label(menu_root, text="Görev Başlığı:")
    title_label.config(bg="lightgray", fg="black")
    title_label.pack(padx=20, pady=10)

    title_entry = tk.Entry(menu_root)
    title_entry.config(bg="lightblue", fg="black", width=30)
    title_entry.pack(padx=20, pady=10)

    content_label = tk.Label(menu_root, text="Görev İçeriği:")
    content_label.config(bg="lightgray", fg="black")
    content_label.pack(padx=20, pady=10)

    content_entry = tk.Entry(menu_root)
    content_entry.config(bg="lightblue", fg="black", width=30)
    content_entry.pack(padx=20, pady=10)

    # Görevi ekle butonu
    add_button = tk.Button(menu_root, text="Ekle", command=add_task)
    add_button.config(width=9, foreground="black")
    add_button.place(x=220, y=210)

    # Arka plan
    menu_root.config(background="lightgray")

    # Renklendirme
    title_label.config(bg="lightgray")
    content_label.config(bg="lightgray")

    # Merkezleme
    center_window(menu_root, 400, 400)
    menu_root.mainloop()

    # Görev bilgisi etiketi
    task_info_label = tk.Label(menu_root, text="")
    task_info_label.config(bg="lightgreen", fg="red")
    task_info_label.pack()

#Menuden görev silmek istediğinizde bu pencereye gelir. Ve
#Silmek için seçtiğiniz dosyalar txt uzantılı dosyadan seçilir.
def open_delete_task_window():
    menu_root.withdraw()
    menu_page()

    marked_password = '*' + password
    uncompleted_tasks = newToDoList.display_uncompleted_tasks(password)
    completed_tasks = newToDoList.display_completed_tasks(marked_password)

    #Silmek istedğiniz de ekrana pop up ekran belirir ve uyarı verir.
    def confirm_delete():
        selected_tasks = [task_title for task_title, checkbox_var in checkboxes.items() if checkbox_var.get() == 1]
        confirm_window = tk.Toplevel(menu_root)
        center_window(confirm_window, 180, 80)
        confirm_window.title("Görevleri Kaldır")

        def on_confirm():
            get_message = tk.Label(menu_root, text="", fg="red", bg="lightblue")
            get_message.place(x=130, y=235)
            message = ""

            for task_title in selected_tasks:
                message = newToDoList.delete_task(password, task_title)

            get_message.config(text=message)

            confirm_window.destroy()

        def on_cancel():
            confirm_window.destroy()

        confirm_label = tk.Label(confirm_window, text="Seçili görevleri kaldırmak\n istediğinizden emin misiniz?")
        confirm_label.pack()

        yes_button = tk.Button(confirm_window, text="Evet", command=on_confirm)
        yes_button.pack(side="right", padx=10, pady=5, anchor="center")

        no_button = tk.Button(confirm_window, text="Hayır", command=on_cancel)
        no_button.pack(side="left", padx=10, pady=5, anchor="center")

    checkboxes = {}

    #Tasarladığımız ekrana veri girişleri yapılır. Tamamlanmamış görevler basılır.
    for (task_title, task_content) in (uncompleted_tasks.items()):
        task_frame = tk.Frame(menu_root, bg="lightblue")
        task_frame.pack(fill="x")

        var = tk.IntVar()
        checkboxes[task_title] = var

        task_label = tk.Label(task_frame, text=f"Görev Başlığı: {task_title}\nGörev İçeriği: {task_content}")
        task_label.config(justify="left", anchor="w", bg="lightblue")
        task_label.pack(side="left")

        checkbox = tk.Checkbutton(task_frame, variable=var)
        checkbox.pack(side="right")

    # Tasarladığımız ekrana veri girişleri yapılır. Tamamlanmış görevler basılır.
    for (task_title, task_content) in (completed_tasks.items()):
        task_frame = tk.Frame(menu_root, bg="lightblue")
        task_frame.pack(fill="x")

        var = tk.IntVar()
        checkboxes[task_title] = var

        task_label = tk.Label(task_frame, text=f"Görev Başlığı: {task_title}\nGörev İçeriği: {task_content}")
        task_label.config(justify="left", anchor="w", bg="lightblue")
        task_label.pack(side="left")

        checkbox = tk.Checkbutton(task_frame, variable=var)
        checkbox.pack(side="right")

    delete_button = tk.Button(menu_root, text="Kaldır", command=confirm_delete, bg="white", fg="red")
    delete_button.pack()

# Tamamlanmamış görevler ekrana bastırılır.
def show_uncompleted_tasks():
    menu_root.withdraw()
    menu_page()

    # Örnek bir görev sözlüğü
    uncompleted_tasks = newToDoList.display_uncompleted_tasks(password)

    # Görevleri ekrana yazdırma
    for task_title, task_content in uncompleted_tasks.items():
        # Label oluşturma
        task_label_new = tk.Label(menu_root, text=f"Görev Başlığı: {task_title.upper()}\nGörev İçeriği: {task_content}")

        # Label özelliklerini ayarlama
        task_label_new.config(background="lightblue", justify="left", anchor="w")
        task_label_new.pack(fill="x", expand=True)

        # Her görev bloku arasında bir ayraç ekleme
        empty_label = tk.Label(menu_root, text="-------------------------------------------------------------")
        empty_label.config(background="lightgray")
        empty_label.pack(fill="x", expand=True)

    # Pencereyi döngüde tutma
    menu_root.mainloop()



#Tamamlanmış görevleri gösterir. Bunu şifrenin önüne (*) koyarak ayırdım.
#Kullanıcı şifresini bir ID olarak belirledim.
def show_completed_tasks():
    menu_root.withdraw()
    menu_page()

    # Örnek bir görev sözlüğü
    marked_password = '*' + password
    completed_tasks = newToDoList.display_completed_tasks(marked_password)

    # Görevleri ekrana yazdırma
    for task_title, task_content in completed_tasks.items():
        # Label oluşturma
        task_label = tk.Label(menu_root, text=f"Görev Başlığı: {task_title.upper()}\nGörev İçeriği: {task_content}")

        # Label özelliklerini ayarlama
        task_label.config(background="lightblue", justify="left", anchor="w")
        task_label.pack(fill="x", expand=True)

        # Her görev bloku arasında bir ayraç ekleme
        empty_label = tk.Label(menu_root, text="-------------------------------------------------------------")
        empty_label.config(background="lightgray")
        empty_label.pack(fill="x", expand=True)

#Görevleri düzenleyip kayıt eder.
def edit_task():
    #Kullanıcıdan görevleri düzenlemesini ve değişiklikleri kaydetmesini sağlar.

    def save_changes(task_title_var, content_entries):
        #Değişiklikleri kaydetmek için bir onay penceresi açar ve kaydetme onayı alır.
        confirm_window = tk.Toplevel(menu_root)
        center_window(confirm_window, 200, 200)
        confirm_window.title("Değişiklikleri Kaydet")

        def on_confirm():
            #Evet butonuna tıklandığında değişiklikleri kaydeder ve mesaj gösterir.
            get_message = tk.Label(menu_root, text="", fg="red", bg="lightblue")
            get_message.place(x=130, y=135)
            message = ""
            for i, task_title in enumerate(task_title_var):
                old_task_title = list(uncompleted_tasks.keys())[i]
                new_task_title = task_title.get()
                new_task_content = content_entries[i].get()

                if uncompleted_tasks[old_task_title] != new_task_content or old_task_title != new_task_title:
                    message = newToDoList.edit_tasks(password, old_task_title, new_task_title, new_task_content)

            get_message.config(text=message)

            confirm_window.destroy()

        def on_cancel():
            #Hayır butonuna tıklandığında onay penceresini kapatır.
            confirm_window.destroy()

        confirm_label = tk.Label(confirm_window, text="Değişiklikleri kaydetmek istiyor musunuz?")
        confirm_label.pack()

        yes_button = tk.Button(confirm_window, text="Evet", command=on_confirm)
        yes_button.pack(pady=5)

        no_button = tk.Button(confirm_window, text="Hayır", command=on_cancel)
        no_button.pack(pady=5)

    # Ana pencereyi gizler ve menü sayfasını gösterir.
    menu_root.withdraw()
    menu_page()

    # Pencere boyutunu yeniden ayarlar.
    center_window(menu_root, 850, 400)

    # Tamamlanmamış görevleri alır.
    uncompleted_tasks = newToDoList.display_uncompleted_tasks(password)

    # Görev başlığı ve içeriği için değişkenler oluşturur.
    task_title_var = []
    content_entries = []

    # Her görev için çerçeve, başlık girişi, içerik girişi ve etiketler oluşturur.
    for task_title, task_content in uncompleted_tasks.items():
        frame = tk.Frame(menu_root)
        frame.pack(pady=10)

        task_title_var.append(tk.StringVar(value=task_title))

        content_label = tk.Label(frame, text="Görev Başlığı:", width=30)
        content_label.pack(pady=5, side="left")

        title_entry = tk.Entry(frame, textvariable=task_title_var[-1], width=30)
        title_entry.pack(pady=5, side="left")

        content_label = tk.Label(frame, text="Görev İçeriği:", width=30)
        content_label.pack(pady=5, side="left")

        content_entry = tk.Entry(frame, width=30)
        content_entry.pack(pady=5, side="left")
        content_entry.insert("end", task_content)
        content_entries.append(content_entry)

    # Değişiklikleri kaydetmek için buton ekler.
    save_button = tk.Button(menu_root, text="Kaydet", command=lambda: save_changes(task_title_var, content_entries))
    save_button.pack(pady=10)

    # Ana pencereyi ana döngüye sokar.
    menu_root.mainloop()

#Görevleri tamamlnadı olarak işsretler
def mark_task():
    #Kullanıcıdan hangi görevleri tamamladığını işaretlemesini ve seçilenleri tamamlama onayı alır.

    # Ana pencereyi gizler ve menü sayfasını gösterir.
    menu_root.withdraw()
    menu_page()

    # Tamamlanmamış görevleri alır.
    uncompleted_tasks = newToDoList.display_uncompleted_tasks(password)

    def confirm_marked():
        #Görev işaretleme onay penceresini oluşturur ve işlem gerçekleştirir.
        selected_tasks = []
        # Seçilen görevleri checkbox değerlerine göre belirler.
        for task_title, checkbox_var in checkboxes.items():
            if checkbox_var.get() == 1:
                selected_tasks.append(task_title)

        confirm_window = tk.Toplevel(menu_root)
        center_window(confirm_window, 180, 80)
        confirm_window.title("Görevleri Tamamla")

        def on_confirm():
            #Evet butonuna tıklanınca seçilen görevleri tamamlar ve mesaj gösterir.
            get_message = tk.Label(menu_root, text="", fg="red", bg="lightblue")
            get_message.place(x=130, y=195)
            message = ""

            for task_title in selected_tasks:
                message = newToDoList.completed_task(password, task_title)

            get_message.config(text=message)

            confirm_window.destroy()

        def on_cancel():
            #Hayır butonuna tıklanınca onay penceresini kapatır.
            confirm_window.destroy()

        confirm_label = tk.Label(confirm_window, text="Seçili görevleri tamamlamak\n istediğinizden emin misiniz?")
        confirm_label.pack()

        yes_button = tk.Button(confirm_window, text="Evet", command=on_confirm)
        yes_button.pack(side="right", padx=10, pady=5, anchor="center")

        no_button = tk.Button(confirm_window, text="Hayır", command=on_cancel)
        no_button.pack(side="left", padx=10, pady=5, anchor="center")

    # Görevlerin checkbox'larıyla gösterilmesi için sözlük ve çerçeve oluşturma.
    checkboxes = {}

    for task_title, task_content in uncompleted_tasks.items():
        task_frame = tk.Frame(menu_root, bg="lightblue")
        task_frame.pack(fill="x")

        var = tk.IntVar()
        checkboxes[task_title] = var

        task_label = tk.Label(task_frame, text=f"Görev Başlığı: {task_title}\nGörev İçeriği: {task_content}")
        task_label.config(justify="left", anchor="w", bg="lightgreen")
        task_label.pack(side="left")

        checkbox = tk.Checkbutton(task_frame, variable=var)
        checkbox.pack(side="right")

    # Görevleri tamamlama butonu ekler.
    marked_button = tk.Button(menu_root, text="Tamamlandı olarak işaretle", command=confirm_marked, bg="blue", fg="red")
    marked_button.pack()

    # Ana pencereyi ana döngüye sokar.
    menu_root.mainloop()

#İlk tasarlanan ana menu sayfası.
def menu_page():
    root.withdraw()
    global menu_root
    # Sayfanın genişliği ve yüksekliği

    menu_root = tk.Toplevel()
    menu_root.title("To-Do List")
    window_width = 400
    window_height = 400

    center_window(menu_root, window_width, window_height)
    menu_root.configure(bg="lightgray")

    menubar = tk.Menu(menu_root, bg="gray", fg="white", borderwidth=3)
    menu_root.config(menu=menubar)

    file_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Görevler", menu=file_menu)
    file_menu.add_command(label="Görev Ekle", command=open_add_task_window)
    file_menu.add_command(label="Görev Sil", command=open_delete_task_window)
    file_menu.add_separator()
    file_menu.add_command(label="Görev Düzenle", command=edit_task)
    file_menu.add_command(label="Tamamlandı olarak işaretle", command=mark_task)
    file_menu.add_separator()
    file_menu.add_command(label="Tamamlanan Görevler", command=show_completed_tasks)
    file_menu.add_command(label="Tamamlanmayan Görevler", command=show_uncompleted_tasks)

    # Geri butonu fonksiyonu
    def back_to_main():
        menu_root.withdraw()
        root.deiconify()

    menubar.add_command(label="Geri", command=back_to_main)


# Ana pencere oluştur
root = tk.Tk()
root.title("Giriş Ekranı")
window_width = 300
window_height = 270

center_window(root, window_width, window_height)
root.configure(bg="lightblue")

# Kullanıcı adı giriş alanı ve etiketi
username_label = tk.Label(root, text="Kullanıcı Adı:", fg="black", bg="lightblue")
username_label.place(x=30, y=30)
username_entry = tk.Entry(root)
username_entry.place(x=120, y=30)

# Şifre giriş alanı ve etiketi
password_label = tk.Label(root, text="Şifre:", fg="black", bg="lightblue")
password_label.place(x=30, y=70)
password_entry = tk.Entry(root, show="*")
password_entry.place(x=120, y=70)

exit_button = tk.Button(root, text="Çıkış", command=exit_program, bg="red", fg="black", font=("Arial", 10, "bold"))
exit_button.place(x=240, y=170)

# Giriş ve Kayıt butonları
login_button = tk.Button(root, text="Giriş Yap", command=login, fg="white", bg="blue")
login_button.place(x=130, y=110)

signup_button = tk.Button(root, text="Kayıt Ol", command=signup, fg="white", bg="blue")
signup_button.place(x=190, y=110)

root.mainloop()
