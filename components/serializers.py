from rest_framework import serializers

from .models import Component, Review


class ReviewSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Review
        fields = ['id']

class ComponentSerializer(serializers.ModelSerializer):
    total_count_links = serializers.IntegerField()
    total_count_f_nodes = serializers.IntegerField()
    total_count_qualifications = serializers.IntegerField()
    total_count_reviews = serializers.IntegerField()
    reviews = ReviewSerializer(many=True)

    class Meta:
        model = Component
        fields = '__all__'
