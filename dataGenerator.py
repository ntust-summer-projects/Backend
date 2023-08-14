from general.models import *
from product.models import *
import random





def getRandomPersonName():
    family = ["李", "王", "張", "劉", "陳", "楊", "黃", "趙", "周", "吳", "徐", "孫", "朱", "馬", "胡",
                  "郭", "林", "何", "高", "梁", "鄭", "羅", "宋", "謝", "唐", "韓", "曹", "許", "鄧", "蕭",
                  "馮", "曾", "程", "蔡", "彭", "潘", "袁", "於", "董", "餘", "蘇", "葉", "呂", "魏", "蔣",
                  "田", "杜", "丁", "沈", "姜", "範", "江", "傅", "鐘", "盧", "汪", "戴", "崔", "任", "陸",
                  "廖", "姚", "方", "金", "邱", "夏", "譚", "韋", "賈", "鄒", "石", "熊", "孟", "秦", "閻",
                  "薛", "侯", "雷", "白", "龍", "段", "郝", "孔", "邵", "史", "毛", "常", "萬", "顧", "賴",
                  "武", "康", "賀", "嚴", "尹", "錢", "施", "牛", "洪", "龔"]
    
    given = ["世", "中", "仁", "伶", "佩", "佳", "俊", "信", "倫", "偉", "傑", "儀", "元", "冠", "凱",
                 "君", "哲", "嘉", "國", "士", "如", "娟", "婷", "子", "孟", "宇", "安", "宏", "宗", "宜",
                 "家", "建", "弘", "強", "彥", "彬", "德", "心", "志", "忠", "怡", "惠", "慧", "慶", "憲",
                 "成", "政", "敏", "文", "昌", "明", "智", "曉", "柏", "榮", "欣", "正", "民", "永", "淑",
                 "玉", "玲", "珊", "珍", "珮", "琪", "瑋", "瑜", "瑞", "瑩", "盈", "真", "祥", "秀", "秋",
                 "穎", "立", "維", "美", "翔", "翰", "聖", "育", "良", "芬", "芳", "英", "菁", "華", "萍",
                 "蓉", "裕", "豪", "貞", "賢", "郁", "鈴", "銘", "雅", "雯", "霖", "青", "靜", "韻", "鴻", "麗", "龍"]
    
    return random.choice(family) + ''.join(random.choices(given, k = random.choice([1,2])))

def getRandomCompanyName():
    adj = ['成功','勝利','有料','大','小']
    noun = ['航天','宇航','火箭','建設','博斯']
    ending = ['有限公司','股份有限公司','公司']
    
    return random.choice(adj) + random.choice(noun) + random.choice(ending)

def getRandomPhone():
    phone = '09'
    
    for i in range(8):
        phone += str(random.randint(0,9))
    
    return phone

def getRandomStr():
    given = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n',
             'o','p','q','r','s','t','u','v','w','x','y','z',
             '0','1','2','3','4','5','6','7','8','9']
    
    return ''.join(random.choices(given, k= random.randint(1,30)))

def getRandomProductName():
    adj = ['毀損', '粗糙', '普通','漂亮','完美', '無暇', '極品', '日本製','中國製']
    noun = ['桌子','椅子','沙發','電視','冰箱','冷氣', '熱水壺','電鍋','汽車','摩托車', '飛機','火車','油輪', '筆', '清潔劑','繃帶','水壺','牙膏']

    return random.choice(adj) + '的' + random.choice(noun)

def createNormalUser():
    try:
        user = User.objects.create(username = getRandomStr(), password = getRandomStr(), role = User.Role.NORMAL)
        Profile.objects.update_or_create(user = user, meta_key = 'name', meta_value = getRandomPersonName())
        Profile.objects.update_or_create(user = user, meta_key = 'phone', meta_value = getRandomPhone())
    except Exception as e:
        print(e)
        createNormalUser()
    
        
def createCompany():
    try:
        company = User.objects.create(username = getRandomStr(), password = getRandomStr(), role = User.Role.COMPANY)
        Profile.objects.update_or_create(user = company, meta_key = 'companyName', meta_value = getRandomCompanyName())
        Profile.objects.update_or_create(user = company, meta_key = 'phone', meta_value = getRandomPhone())
        Profile.objects.update_or_create(user = company, meta_key = 'chairman', meta_value = getRandomPersonName())
    except Exception as e:
        print(e)
        createCompany()
        
        
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
                product.materials.add(material = random.choice(Material.objects.all()), weight = random.uniform(0.1, 1000))
            except:
                pass
            
        for i in range(random.randint(0,3)):
            try:
                product.tag.add(random.choice(Tag.objects.all()))
            except:
                pass
                
    except Exception as e:
        print(e)
        createProduct()