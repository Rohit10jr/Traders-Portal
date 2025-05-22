from django.shortcuts import render
# from .models import Company, WatchList
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from .serializers import RegisterSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from rest_framework import generics
from django.db.models import Q
from .models import Company, WatchList
from .serializers import CompanySerializer, WatchlistSerializer

from rest_framework.exceptions import ValidationError
import logging
logger = logging.getLogger(__name__)
from django.db import IntegrityError
from rest_framework import generics, permissions, status
from django.shortcuts import get_object_or_404 # Helper for getting company


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": serializer.data, "status": status.HTTP_201_CREATED, "message": "user registered"}, status=status.HTTP_201_CREATED)
        return Response({
                    "message": "Registration failed. Please check the provided data.",
                    "errors": serializer.errors,
                    "status_code": status.HTTP_400_BAD_REQUEST,
                }, status=status.HTTP_400_BAD_REQUEST)

class Home(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        return Response({'message':"welcome home"}, status=status.HTTP_200_OK)


# model viewset

# class CompanyViewSet(ModelViewSet):
#     queryset = Company.objects.all()
#     serializer_class = CompanySerializer
#     filter_backends = [filters.SearchFilter, DjangoFilterBackend]
#     search_fields = ['company_name', 'symbol']
#     filterset_fields = ['symbol', 'scripcode']


# ----------- Company Views (CRUD for User) -----------

class CompanyListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CompanySerializer
    queryset = Company.objects.all()


    def get_queryset(self):
        queryset = self.queryset
        q = self.request.query_params.get('q', '')
        if q:
            queryset = queryset.filter(
                Q(company_name__icontains=q) |
                Q(symbol__icontains=q) |
                Q(scripcode__icontains=q)
            )
        return queryset
    

class CompanyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]


# ----------- Watchlist Views (CRUD for User) -----------

class WatchlistListCreateView(generics.ListCreateAPIView):
    queryset = WatchList.objects.all()
    serializer_class = WatchlistSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return WatchList.objects.filter(user=self.request.user)


    # using serializer field
    def perform_create(self, serializer):
        company = serializer.validated_data['company_id']
        print("company", company)
        if WatchList.objects.filter(user=self.request.user, company=company).exists():
            raise ValidationError("Already in watchlist.")
        serializer.save(user=self.request.user, company_id=company.id)
        # serializer.save(user=self.request.user, company=company)
        # above is equivalent to this
        # serializer.save(user=self.request.user, company=Company.objects.get(pk=company_id))

   
    # def perform_create(self, serializer):
    #     user = self.request.user
    #     company_id = self.request.data.get('company_id')

    #     if not company_id:
    #         raise ValidationError({"company_id": "This field is required."})

    #     try:
    #         company = Company.objects.get(id=company_id)
    #     except Company.DoesNotExist:
    #         raise ValidationError({"company_id": "Company with this ID does not exist."})
        
    #     # company = get_object_or_404(Company, id=company_id)
        
    #     # runs before the database operation
    #     if WatchList.objects.filter(user=user, company=company).exists():
    #         raise ValidationError({"non_field_errors": ["This company is already in your watchlist."]})

    #     # Database-level Fallback
    #     try:
    #         # watchlist_item, created = WatchList.objects.get_or_create(user=self.request.user, company=company)
    #         serializer.save(user=user, company=company)
    #     except IntegrityError:
    #          raise ValidationError({"non_field_errors": ["This company is already in your watchlist (IntegrityError)."]})


class WatchlistListDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WatchlistSerializer

    def get_queryset(self):
        return WatchList.objects.filter(user=self.request.user)
        # return super().get_queryset()
    
    def perform_update(self, serializer):
        company = serializer.validated_data['company_id']
        if WatchList.objects.filter(user=self.request.user, company=company).exclude(id=self.get_object().id).exists():
            raise ValidationError("Already in watchlist.")
        serializer.save(user=self.request.user, company=company)