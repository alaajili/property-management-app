import django_filters
from .models import Property

class PropertyFilter(django_filters.FilterSet):
	rental_cost_min = django_filters.NumberFilter(field_name='rental_cost', lookup_expr='gte')
	rental_cost_max = django_filters.NumberFilter(field_name='rental_cost', lookup_expr='lte')
	property_type = django_filters.ChoiceFilter(choices=Property.PROPERTY_TYPES)
	address = django_filters.CharFilter(lookup_expr='icontains')

	class Meta:
		model = Property
		fields = ['property_type', 'address', 'rental_cost_min', 'rental_cost_max']