# Görevleri başlıkları almak için Oredered dict kullanıldı
#Ve ayrıca hata ayıklayıcılar import edildi
#PersonalDatas.txt açılıp içinde görev işlemleri yapılır.
from collections import OrderedDict
from myExceptions import *

# Genel olarak görev davranışları ve depolama işlemi
#Bu classların içinde yapıldı ve hatalar ele alındı
class ToDoList:
    def __init__(self):
        self.tasks = OrderedDict()

# Görev eklendiğinde dosyaya kayıt işlemi buradan yapılır.
    def add_task(self, task_name, task_details):
        try:
            if task_details == "":
                raise dutyEmpty
            elif task_name == "":
                raise titleEmpty
            else:
                self.tasks[task_name] = task_details
                return True

        except dutyEmpty:
            print("Duty can not be empty! ")
            return False

        except titleEmpty:
            print("Title can not be empty! ")
            return False
#Tamamlanmayan görevlerin döndürülmesi.
    def display_uncompleted_tasks(self, ID):
        try:
            unmarked_dict = {}
            with open('PersonalDatas.txt', 'r') as file:
                lines = file.readlines()  # Dosyadaki tüm satırları okuyalım

                for line in lines:
                    text = line.strip().split(",")
                    if text[0] == ID:
                        unmarked_dict[text[1]] = text[2]
            return unmarked_dict
        except FileNotFoundError:
            print("File is not found!")

#Kullanıcı eğer görevi değiştirmek isterse çalışacak kod budur.
# Yeniden kayıt işlemi yapılacak
    def edit_tasks(self, Id, old_duty_name, new_duty_name, new_content):
        flag = False
        try:
            with open('PersonalDatas.txt', 'r') as file:
                lines = file.readlines()  # Dosyadaki tüm satırları okuyalım
                timer = 0
                for line in lines:
                    text = line
                    text_new = text.split(",")
                    for i in text_new:
                        if i == Id:
                            if text_new[1] == old_duty_name:
                                lines[timer] = Id + ',' + new_duty_name + ',' + new_content + '\n'
                                flag = True
                    timer += 1
                if flag == False:
                    raise notFoundDuty
            if new_duty_name == "":
                raise titleEmpty
            elif new_content == "":
                raise dutyEmpty
            else:
                with open('PersonalDatas.txt', 'w') as file:
                    file.writelines(lines)
                return ("Successfully was edited")

        except FileNotFoundError:
            return ("File is not found! ")

        except notFoundDuty:
            return ("Duty is not found! ")

        except titleEmpty:
            return ("Title can not be empty! ")

        except dutyEmpty:
            return ("Duty can not be empty! ")

#Görev silindiğinde dosyadan kaldırılır. Bu fonksiyon onu temizler
    def delete_task(self, get_id, get_name):
        flag = False
        get_marked_id = "*" + get_id
        try:
            with open('PersonalDatas.txt','r') as file:
                lines = file.readlines()  # Dosyadaki tüm satırları okuyalım
                timer = 0
                for line in lines:
                    text = line
                    text_new = text.split(",")
                    for i in text_new:
                        if i == get_id or i == get_marked_id:
                            if text_new[1] == get_name:
                                lines.pop(timer)
                                flag = True
                    timer += 1

                if flag == False:
                    raise notFoundDuty
                else:
                    with open('PersonalDatas.txt', 'w') as file:
                        file.writelines(lines)
                    return "Successfully was deleted"

        except FileNotFoundError:
            return ("File is not found! ")

        except notFoundDuty:
            return ("Duty is not found! ")

#Gönderilen görevi tamamlandı olarak işaretler.Yani aslında
#Gönderilen görevin idsinin önüne yıldız konur.
    def completed_task(self, getID, getName):
        flag = False
        try:
            with open('PersonalDatas.txt', 'r') as file:
                lines = file.readlines()  # Dosyadaki tüm satırları okuyalım
                timer = 0
                for line in lines:
                    text = line
                    text_new = text.split(",")
                    for i in text_new:
                        if i == getID:
                            if text_new[1] == getName:
                                lines[timer] = '*' + getID + ',' + getName + ',' + text_new[2]
                                flag = True
                    timer += 1

                if flag == False:
                    raise notFoundDuty
                else:
                    with open('PersonalDatas.txt', 'w') as file:
                        file.writelines(lines)
                    return "Added duty as completed"

        except notFoundDuty:
            return ("Duty is not found! ")

        except FileNotFoundError:
            return ("File is not found! ")

# Tamamlanmış görevleri döndüren fonksiyon
    def display_completed_tasks(self, ID):
        try:
            marked_dict = {}
            with open('PersonalDatas.txt', 'r') as file:
                lines = file.readlines()  # Dosyadaki tüm satırları okuyalım

                for line in lines:
                    text = line
                    text_new = text.split(",")
                    for i in text_new:
                        if i == ID:
                            marked_dict[text_new[1]] = text_new[2]
                return marked_dict
        except FileNotFoundError:
            print("File is not found! ")

# Yazılan görevin onayladığı yer yani kayıt aşaması.
    def save_changes(self, get_id, flag):

        if flag == True:
            path = "PersonalDatas.txt"
            file = open(path, "a")
            file.write(get_id + ",")
            file.close()
            array = []
            for i in self.tasks.keys():
                array_temp = [str(i), str(self.tasks[i])]
                array.append(array_temp)

            for i in array:
                with open('PersonalDatas.txt', 'a') as file:
                    file.write(','.join(i))
            try:
                with open('PersonalDatas.txt', 'a', encoding='utf-8') as file:
                    file.write('\n')

            except FileNotFoundError:
                print("File is not found! ")

            self.tasks = {}
            return "Succcessfully added"

