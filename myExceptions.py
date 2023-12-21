#Tanımladığım hatalar. Burada alınacak hata türleri tanımlandı.
# Görev bulunamadı, görev boş, başlık boş hataları döndürülüyor.
class notFoundDuty(Exception):
    pass


class dutyEmpty(Exception):
    pass


class titleEmpty(Exception):
    pass
