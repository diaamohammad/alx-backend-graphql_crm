import graphene
from graphene_django.types import DjangoObjectType

# الآن نقدر نستورده بأمان
from crm.models import Product 

class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = ("id", "name", "stock")

# ==========================================================
# 1. كلاس الـ Query (للمهمة 2)
# ==========================================================
class Query(graphene.ObjectType):
    hello = graphene.String(default_value="Hello, CRM!")
    
    # (ضيف أي queries تانية عندك)
    all_products = graphene.List(ProductType)
    
    def resolve_all_products(root, info):
        return Product.objects.all()

# ==========================================================
# 2. كلاس الـ Mutation (للمهمة 3)
# ==========================================================
class UpdateLowStockProducts(graphene.Mutation):
    class Arguments:
        pass

    success = graphene.Boolean()
    updated_products = graphene.List(ProductType)

    @staticmethod
    def mutate(root, info):
        # ده الكود الحقيقي للتاسك 3
        low_stock_products = Product.objects.filter(stock__lt=10)
        updated_list = []
        
        for product in low_stock_products:
            product.stock += 10 # زيادة المخزون بـ 10
            product.save()
            updated_list.append(product)
            
        return UpdateLowStockProducts(success=True, updated_products=updated_list)

# ==========================================================
# 3. كلاس الـ Mutation الرئيسي
# ==========================================================
class Mutation(graphene.ObjectType):
    update_low_stock = UpdateLowStockProducts.Field()
    # (ضيف أي mutations تانية عندك)

# ==========================================================
# 4. ربط الـ Schema
# ==========================================================
schema = graphene.Schema(query=Query, mutation=Mutation)