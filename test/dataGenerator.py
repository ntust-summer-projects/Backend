from general.models import *
from product.models import *
import random
from faker import Faker
from test.Bullshit import Bullshit

fake = Faker(locale='zh_TW')

def getRandomPersonName():
    return fake.name()

def getRandomCompanyName():
    return fake.company()

def getRandomEmail():
    return fake.email()

def getRandomPhone():
    return fake.phone_number()

def getRandomStr():
    return fake.pystr()

def getRandomPassword():
    return fake.password()

def getRandomAddress():
    return fake.address()

def getRandomVat():
    return fake.random_number(digits = 8)

def getRandomCompanyEmail():
    return fake.company_email()

def getRandomProductName():
    adj = ['毀損', '粗糙', '普通','漂亮','完美', '無暇', '極品', '日本製','中國製']
    noun = ['桌子','椅子','沙發','電視','冰箱','冷氣', '熱水壺','電鍋','汽車','摩托車', '飛機','火車','油輪', '筆', '清潔劑','繃帶','牙膏']

    return random.choice(adj) + '的' + random.choice(noun)



def createNormalUser():
    try:
        user = User.objects.create(username = getRandomStr(), password = getRandomPassword(),  email = getRandomEmail(), role = User.Role.NORMAL)
        Profile.objects.update_or_create({'meta_value': getRandomPersonName()}, user = user, meta_key = 'name')
        Profile.objects.update_or_create({'meta_value': getRandomPhone()}, user = user, meta_key = 'phone')
    except Exception as e:
        print(e)
        createNormalUser()
        
    result = f"name = {Profile.objects.get(user = user, meta_key = 'name').meta_value}, username = {user.username}"    
    
    return result
    
        
def createCompany():
    try:
        company = User.objects.create(username = getRandomStr(), password = getRandomPassword(),  email = getRandomCompanyEmail(), role = User.Role.COMPANY)
        Profile.objects.update_or_create({'meta_value': getRandomCompanyName()}, user = company, meta_key = 'companyName')
        Profile.objects.update_or_create({'meta_value': getRandomPhone()}, user = company, meta_key = 'phone')
        Profile.objects.update_or_create({'meta_value': getRandomPersonName()}, user = company, meta_key = 'chairman')
        Profile.objects.update_or_create({'meta_value': getRandomAddress()}, user = company, meta_key = 'address')
        Profile.objects.update_or_create({'meta_value': getRandomVat()}, user = company, meta_key = 'vatNumber')
    except Exception as e:
        print(e)
        createCompany()
        
    result = f"name = {Profile.objects.get(user = company, meta_key = 'companyName').meta_value}, username = {company.username}"
    
    return result
        
        
def createTag():
    try:
        Tag.objects.bulk_create(
            [Tag(name = '美妝'),
            Tag(name = '食物'),
            Tag(name = '工具'),
            Tag(name = '環保'),
            Tag(name = '清潔'),
            Tag(name = '名牌'),
            Tag(name = '日用'),
            Tag(name = '手工'),
            Tag(name = '健康'),
            Tag(name = '交通'),
            Tag(name = '醫療')
            ]
        )
    except Exception as e:
        print(e)
        

def createProduct():
    try:
        product = Product.objects.create(company = random.choice(User.objects.all().filter(role = User.Role.COMPANY)), name = getRandomProductName(), number = getRandomStr())
        
        for i in range(random.randint(1,10)):
            try:
                Component.objects.create(product = product, material = random.choice(Material.objects.all()), weight = random.uniform(0.1, 1000))
            except Exception as e:
                print(f"Material error: { e }")
                pass
            
        for i in range(random.randint(0,3)):
            try:
                product.tag.add(random.choice(Tag.objects.all()))
            except:
                pass
                
    except Exception as e:
        print(e)
        createProduct()
        
    result = f"name = {product.name}, coe = {product.carbonEmission}"
        
    return result

def createAnnouncement():
    topic = fake.word()
    length = random.randint(50,200)
    obj = Bullshit()
    announcement = Announcement.objects.create(title = topic, context = obj.generate(topic, length))
    
    result = f'title = { announcement.title }, context = { announcement.context }'
    
    return result
    
    

        
        