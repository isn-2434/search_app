from django.db import models

POSITION = [('ミドルブロッカー','MB'),('ウイングスパイカー','WS'),('セッター','S'),('リベロ','L'),('オポジット','OP'),('アウトサイドヒッター','OH'),('マネージャー','MG'),('監督','AD'),('コーチ','CH')]
    
class Product(models.Model): 
    id = models.BigAutoField(primary_key=True) 
    name = models.CharField(max_length=255)
    age = models.IntegerField(default=1)
    height = models.DecimalField(max_digits=5, decimal_places=1,default=1)
    weight = models.DecimalField(max_digits=5, decimal_places=1,default=1)
    team = models.CharField(max_length=255,default="烏野高校")
    position = models.CharField(max_length=255,choices=POSITION)
    description = models.TextField(default="---")
    image = models.ImageField(default='../static/image/noimg.jpg')

    def __str__(self): 
        
        return self.name