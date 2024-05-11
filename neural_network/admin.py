from django.contrib import admin


from .models import NeuralNetwork, NNMarketData


@admin.register(NeuralNetwork)
class NeuralNetworkAdmin(admin.ModelAdmin):
    list_display = ("name", "author", "updated_at", "is_hidden")
    search_fields = ("name", "author", "summary", "instruction")
    list_filter = ("is_hidden",)
    fields = (
        "name",
        "summary",
        "desc",
        "instruction",
        "logo",
        "is_hidden",
        "author",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )


@admin.register(NNMarketData)
class NNMarketDataAdmin(admin.ModelAdmin):
    list_display = ("neural_network", "price", "created_at")
    search_fields = ("neural_network", "price")
    fields = ("neural_network", "price")
    readonly_fields = ("created_at",)
