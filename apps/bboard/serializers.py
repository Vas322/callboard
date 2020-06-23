from rest_framework import serializers
from .models import Rubric


class RubricSerializer(serializers.ModelSerializer):
    """Сериалайзер для обработки рубрик"""

    class Meta:
        model = Rubric
        fields = ('id', 'name')
