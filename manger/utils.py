import csv
from collections import namedtuple
from django.http import HttpResponse
from datetime import timedelta
from django.db.models.functions import ExtractHour,ExtractWeekDay
from django.db.models import Q, Sum, F, ExpressionWrapper, DecimalField, Func ,Count
from decimal import Decimal
from shop.models import Product, Category
from orders.models import Table ,Order, OrderItem
from django.utils import timezone

class Reporting:
    """
    Total sales              *
    favorite tables          *
    favorite foods           *
    generate Sales Invoice
    """

    def __init__(self, kwargs):
        if 'days' in kwargs:
            self.days = kwargs['days']
            self.time_filter = Q(created__gte=timezone.now() - timezone.timedelta(days=self.days))
        elif 'start_at' in kwargs and 'end_at' in kwargs:
            self.start_at = kwargs['start_at']
            self.end_at = kwargs['end_at'] + timedelta(days=1)
            self.time_filter = Q(created__range=[self.start_at, self.end_at])

    def total_sales(self):
        """
        By using ExpressionWrapper in combination with annotate or other queryset methods,
         you can include more complex database expressions in your queries,
          providing flexibility and allowing you to perform calculations directly at the database level.
        """

        class RoundDecimal(Func):
            """
                https://stackoverflow.com/questions/17085898/conversion-of-datetime-field-to-string-in-django-queryset-values-list
                https://docs.djangoproject.com/en/1.8/ref/models/expressions/
            """
            function = 'ROUND'
            template = '%(function)s(%(expressions)s, 2)'


        orders = Order.objects.filter(
            self.time_filter
        )
        total_sales = orders.aggregate(
            total_sales=ExpressionWrapper(
                RoundDecimal(
                    Sum(
                        RoundDecimal(F('items__price') * 1.0000000001 * F('items__quantity')),
                        output_field=DecimalField(max_digits=10, decimal_places=4)
                    )
                ),
                output_field=DecimalField(max_digits=10, decimal_places=2)
            )
        ) or Decimal('0.00')
        return total_sales['total_sales']

    def favorite_tables(self):
        try:
            time_filter = Q(order__created__gte=timezone.now() - timezone.timedelta(days=self.days))
        except AttributeError:
            time_filter = Q(order__created__range=[self.start_at, self.end_at])

        most_used_tables = (
            Table.objects
            .annotate(used_seats=Count('order__id', distinct=True, filter=(
                    time_filter
            )))
            .order_by('-used_seats')
        )
        for table in most_used_tables:
            if table.used_seats > 0:
                yield table

    def favorite_foods(self):
        """
        collections.namedtuple is a factory function in Python's collections module that creates
         a new class with named fields. It returns a new class type that can be used to create tuples
          with named fields.
        used namedtuple to create a simple data structure (ProductData) to represent
         the data for each food item with named fields. This makes it easier to manage and access
          the attributes in the template.
        """
        ProductData = namedtuple('ProductData', ['id', 'name', 'total_sales', 'counts', 'category'])

        try:
            time_filter = Q(order_items__order__created__gte=timezone.now()
                                                              - timezone.timedelta(days=self.days))
        except AttributeError:
            time_filter = Q(order_items__order__created__range=[self.start_at, self.end_at])

        most_used_foods = (
            Product.objects
            .all()
            .annotate(
                used_foods=Sum('order_items__quantity', distinct=True),
                total_sales=Sum(
                    ((F('order_items__price') * F('order_items__quantity'))), output_field=DecimalField()
                )
            )
            .select_related('category')
            .order_by('-used_foods')
        )

        for food in most_used_foods:
            if food.used_foods > 0:
                food_data = ProductData(
                    id=food.pk,
                    name=food.name,
                    total_sales=food.total_sales,
                    counts=food.used_foods,
                    category=food.category,
                )
                yield food_data

    def get_percentage_difference(self):
        """
        Calculate the percentage difference between the current time frame and the previous one.
        For instance, if self.days is 2, it will compare the last 2 days with the 2 days before that. :-)
        """
        current_sales = self.total_sales()
        try:
            reporting_params = {'days': self.days * 2}
        except AttributeError:
            return 0

        previous_days_sales = Reporting(reporting_params).total_sales()

        if previous_days_sales and current_sales:
            percentage_difference = ((previous_days_sales - current_sales) / abs(previous_days_sales)) * 100
        else:
            if current_sales:
                percentage_difference = 100
            else:
                percentage_difference = 0

        return percentage_difference

    def peak_hours(self):  
        start_hour = 0
        end_hour = 24

        orders = Order.objects.filter(
            self.time_filter
        )

        orders_by_hour = orders.annotate(hour=ExtractHour('created'))

        peak_hours_data = (
            orders_by_hour
            .filter(hour__gte=start_hour, hour__lt=end_hour)
            .values('hour')
            .annotate(order_count=Count('id'))
            .order_by('-order_count')
        )
        peak_hours_list = []
        for hour_data in peak_hours_data:
            current_hour = hour_data['hour']
            next_hour = current_hour + 1 if current_hour < 23 else 0  

            order_count = hour_data['order_count']
            peak_hours_list.append({
                'hour_range': f"{current_hour} - {next_hour}",
                'order_count': order_count
            })
        if peak_hours_list:
            return peak_hours_list, list(peak_hours_list[0].values())[0]
        else:
            return 'No hour found', 'No hour found'

    def peak_day_of_week(self):

        orders = Order.objects.filter(
            self.time_filter,
        )

        orders_by_day = orders.annotate(day_of_week=ExtractWeekDay('created'))

        peak_days_data = (
            orders_by_day
            .values('day_of_week')
            .annotate(order_count=Count('id'))
            .order_by('-order_count')
        )

        peak_days_list = []
        for day_data in peak_days_data:
            day_of_week = day_data['day_of_week']
            order_count = day_data['order_count']
            peak_days_list.append({
                'day_of_week': day_of_week,
                'order_count': order_count
            })
        if peak_days_list:
            return peak_days_list
        else:
            return None

    def best_cutomer(self):
        orders = Order.objects.filter(
            self.time_filter,
        )
        best_customer_data = (
            orders
            .values('phone')
            .annotate(order_count=Count('id'))
            .order_by('-order_count')
        )
        if best_customer_data:
            return list(best_customer_data[0].values())[0]
        else:
            return 'No user found'

    def favorite_category(self):
        CategoryData = namedtuple('CategoryData', ['id', 'name', 'total_sales'])

        most_used_categories = (
            Category.objects
            .all()
            .annotate(
                total_sales=Sum(
                    F('products__order_items__quantity') * F('products__order_items__price')
                    , output_field=DecimalField()
                )
            )
            .order_by('-total_sales')
        )

        for category in most_used_categories:
            if category.name == "All":
                continue
            elif category.total_sales > 0:
                category_data = CategoryData(
                    id=category.pk,
                    name=category.name,
                    total_sales=category.total_sales,
                )
                yield category_data


    def order_status_counts(self):
        OrderStatusCount = namedtuple('OrderStatusCount', ['status', 'status_display', 'count'])
        status_counts = (
            Order.objects
            .values('status').filter(self.time_filter)
            .annotate(count=Count('id'))
            .order_by('status')
        )

        result_data = [
            OrderStatusCount(
                status=status_data['status'],
                status_display=dict(Order.status_fields)[status_data['status']],
                count=status_data['count']
            )
            for status_data in status_counts
        ]
        return result_data


# class CSVExportMixin():
#     def dispatch(self, request, *args, **kwargs):
#         if 'export_csv' in request.GET:
#             queryset = self.get_csv_export_queryset()
#             filename = self.get_csv_export_filename()
#             return self.export_csv(queryset, filename)

#         return super().dispatch(request, *args, **kwargs)

#     def get_csv_export_queryset(self):
#         return None

#     def get_csv_export_filename(self):
#         return 'exported_data'

#     def export_csv(self, queryset, filename):
#         response = HttpResponse(content_type='text/csv')
#         response['Content-Disposition'] = f'attachment; filename="{filename}.csv"'

#         total_cost_sum = Decimal(0)
#         writer = csv.writer(response)

#         if queryset.model == Order:
#             headers = [field.name for field in queryset.model._meta.fields]
#             headers.append('total_cost')  # Add total_cost to headers

#             writer.writerow(headers)

#             for obj in queryset:
#                 print(obj)
#                 row_data = [str(getattr(obj, field)) for field in headers[:-1]]
#                 total_cost = round(obj.get_total_cost(), 2)
#                 row_data.append(total_cost)
#                 writer.writerow(row_data)

#                 total_cost_sum += total_cost

#             writer.writerow(['Total Cost Sum:', '', '', '', '', '', '', '', '', f'{total_cost_sum}'])
#         else:
#             # For other models, use default behavior
#             headers = [field.name for field in queryset.model._meta.fields]
#             writer.writerow(headers)

#             for obj in queryset:
#                 writer.writerow([str(getattr(obj, field)) for field in headers])

#         return response
def export_csv():
        queryset = Order.objects.all().values()
        customers_data = (
            queryset
            .values('phone')
            .annotate(count=Count('id'),
                      total=Sum(
                          F('items__price') * F('items__quantity')  ,
                          output_field=DecimalField(max_digits=10, decimal_places=2)
                      )
                      )
            .order_by('-total')
        )
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="customer_orders.csv"'

        writer = csv.writer(response)
        headers = ['phone' , 'count', 'total']
        writer.writerow(headers)

        for row in customers_data:
            writer.writerow([str(row[field]) for field in headers])

        return response  