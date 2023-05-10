from django.db import models


class AccountType(models.TextChoices):
    CHECKING_ACCOUNT = "CHECKING_ACCOUNT", "입출금"
    SAVINGS_ACCOUNT = "SAVINGS_ACCOUNT", "저금"
    INSTALLMENT_SAVING = "INSTALLMENT_SAVING", "적금"
    TIME_DEPOSIT = "TIME_DEPOSIT", "예금"
    CREDIT_CARD = "CREDIT_CARD", "신용카드"
    STOCK = "STOCK", "주식"


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
    CAR = "CAR", "차/주유"
    HOUSING = "HOUSING", "집/월세"
    LEISURE = "LEISURE", "여가"
    MEDICAL = "MEDICAL", "의료비"
    PARENTING = "PARENTING", "육아"
    TRANSFER = "TRANSFER", "이체"
    INTEREST = "INTEREST", "이자"
    INCOME = "INCOME", "소득"
    ETC = "ETC", "ETC"


class RetailerType(models.TextChoices):
    ETC = "ETC"
    STORE = "STORE"
    PERSON = "PERSON"
    BANK = "BANK"
    SERVICE = "SERVICE"


class DetailItemCategory(models.TextChoices):
    ETC = "ETC", "ETC"
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
    TAX = "TAX", "TAX"
    SEAFOOD = "SEAFOOD", "해산물"
    INGREDIENT = "INGREDIENT", "식재료"
    APPLIANCE = "APPLIANCE", "가전"
    STATIONERY = "STATIONERY", "문구류"
    BATH = "BATH", "욕실용품"
    BABY = "BABY", "육아용품"
    COOKER = "COOKER", "주방용품"
    FOOD = "FOOD", "식품"
    CLOTHING = "CLOTHING", "의류"
    UNK = "UNK", "Unknown"
