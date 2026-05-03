from address.models import Branch, City, Country, State
from common.serializers import BaseModelSerializer


class CountrySerializer(BaseModelSerializer):
    class Meta:
        model = Country
        fields = ["id", "label", "created_at", "updated_at"]


class CityMiniSerializer(BaseModelSerializer):
    class Meta:
        model = City
        fields = ["id", "label"]


class StateMiniSerializer(BaseModelSerializer):
    class Meta:
        model = State
        fields = ["id", "label"]


class StateSerializer(BaseModelSerializer):
    country_detail = CountrySerializer(source="country", read_only=True)

    class Meta:
        model = State
        fields = BaseModelSerializer.Meta.fields + (
            "id",
            "label",
            "country",
            "country_detail",
        )


class CitySerializer(BaseModelSerializer):
    state_detail = StateMiniSerializer(source="state", read_only=True)

    class Meta:
        model = City
        fields = BaseModelSerializer.Meta.fields + (
            "id",
            "label",
            "state",
            "state_detail",
        )


class BranchSerializer(BaseModelSerializer):
    city_detail = CityMiniSerializer(source="city", read_only=True)
    state_detail = StateMiniSerializer(source="city.state", read_only=True)

    class Meta:
        model = Branch
        fields = BaseModelSerializer.Meta.fields + (
            "id",
            "code",
            "title",
            "city",
            "city_detail",
            "address",
            "location",
            "is_active",
            "mobile",
            "state_detail",
        )
