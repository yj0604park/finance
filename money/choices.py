from django.db import models


class AccountType(models.TextChoices):
    CHECKING_ACCOUNT = "CHECKING_ACCOUNT", "입출금"
    SAVINGS_ACCOUNT = "SAVINGS_ACCOUNT", "저금"
    INSTALLMENT_SAVING = "INSTALLMENT_SAVING", "적금"
    TIME_DEPOSIT = "TIME_DEPOSIT", "예금"
    CREDIT_CARD = "CREDIT_CARD", "신용카드"
    STOCK = "STOCK", "주식"
    LOAN = "LOAN", "대출"


class CurrencyType(models.TextChoices):
    KRW = "KRW", "원화"
    USD = "USD", "달러"


class TransactionCategory(models.TextChoices):
    SERVICE = "SERVICE", "서비스"
    DAILY_NECESSITY = "DAILY_NECESSITY", "생필품"
    MEMBERSHIP = "MEMBERSHIP", "맴버쉽"
    GROCERY = "GROCERY", "식료품"
    EAT_OUT = "EAT_OUT", "외식"
    CLOTHING = "CLOTHING", "옷"
    PRESENT = "PRESENT", "선물"
    TRANSPORTATION = "CAR", "차/주유/운임"
    HOUSING = "HOUSING", "집/월세"
    LEISURE = "LEISURE", "여가"
    MEDICAL = "MEDICAL", "의료비"
    PARENTING = "PARENTING", "육아"
    TRANSFER = "TRANSFER", "이체"
    INTEREST = "INTEREST", "이자"
    INCOME = "INCOME", "소득"
    STOCK = "STOCK", "주식"
    CASH = "CASH", "현금"
    ETC = "ETC", "기타"


class RetailerType(models.TextChoices):
    ETC = "ETC", "기타"
    STORE = "STORE", "상점"
    PERSON = "PERSON", "개인"
    BANK = "BANK", "은행"
    SERVICE = "SERVICE", "서비스"
    INCOME = "INCOME", "수입"
    RESTAURANT = "RESTAURANT", "식당"


class DetailItemCategory(models.TextChoices):
    ETC = "ETC", "기타"
    FRUIT = "FRUIT", "과일"
    ALCOHOL = "ALCOHOL", "주류"
    DRINK = "DRINK", "음료"
    SAUCE = "SAUCE", "소스"
    MEAT = "MEAT", "육류"
    VEGETABLE = "VEGETABLE", "채소"
    DAIRY = "DAIRY", "유제품"
    WRAP = "WRAP", "포장지"
    SNACK = "SNACK", "스낵"
    NOODLE = "NOODLE", "면"
    BREAD = "BREAD", "빵"
    DRUG = "DRUG", "약"
    TAX = "TAX", "세금"
    SEAFOOD = "SEAFOOD", "해산물"
    INGREDIENT = "INGREDIENT", "식재료"
    APPLIANCE = "APPLIANCE", "가전"
    STATIONERY = "STATIONERY", "문구류"
    BATH = "BATH", "욕실용품"
    BABY = "BABY", "육아용품"
    COOKER = "COOKER", "주방용품"
    FOOD = "FOOD", "식품"
    CLOTHING = "CLOTHING", "의류"
    FURNITURE = "FURNITURE", "가구"
    SPORTING = "SPORTING", "운동용품"
    UNKNOWN = "UNKNOWN", "알 수 없음"


class ExchangeType(models.TextChoices):
    ETC = "ETC", "기타"
    BANK = "BANK", "은행"
    WIREBARLEY = "WIREBARLEY", "와이어바알리"
    CREDITCARD = "CREDITCARD", "신용카드"
