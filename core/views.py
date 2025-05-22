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

# class CompanyViewSet(ModelViewSet):
#     queryset = Company.objects.all()
#     serializer_class = CompanySerializer
#     filter_backends = [filters.SearchFilter, DjangoFilterBackend]
#     search_fields = ['company_name', 'symbol']
#     filterset_fields = ['symbol', 'scripcode']

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": serializer.data, "status": status.HTTP_201_CREATED, "message": "user registered"})
        return Response({
                    "message": "Registration failed. Please check the provided data.",
                    "errors": serializer.errors,
                    "status_code": status.HTTP_400_BAD_REQUEST,
                }, status=status.HTTP_400_BAD_REQUEST)



class Home(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        return Response({'message':"welcome home"}, status=status.HTTP_200_OK)
    

# Company search with filters
class CompanyListView(generics.ListAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [AllowAny]

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


# Add to Watchlist
class AddToWatchlistView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        company_id = request.data.get('company_id')
        try:
            company = Company.objects.get(id=company_id)
            watchlist_item, created = WatchList.objects.get_or_create(user=request.user, company=company)
            if created:
                return Response({"message": "Added to watchlist"}, status=status.HTTP_201_CREATED)
            return Response({"message": "Already in watchlist"}, status=status.HTTP_200_OK)
        except Company.DoesNotExist:
            return Response({"error": "Company not found"}, status=status.HTTP_404_NOT_FOUND)


class RemoveFromWatchlistView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return WatchList.objects.filter(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object() # This fetches the object, filtered by get_queryset
        instance.delete()
        return Response({"message": "Successfully removed from watchlist."}, status=status.HTTP_204_NO_CONTENT)


# Remove from Watchlist
# class RemoveFromWatchlistView(generics.DestroyAPIView):
#     permission_classes = [IsAuthenticated]

#     def delete(self, request, pk):
#         try:
#             item = WatchList.objects.get(user=request.user, company__id=pk)
#             item.delete()
#             return Response({"message": "Removed from watchlist"}, status=status.HTTP_204_NO_CONTENT)
#         except WatchList.DoesNotExist:
#             return Response({"error": "Item not in watchlist"}, status=status.HTTP_404_NOT_FOUND)


class UserWatchListView(generics.ListAPIView):
    serializer_class = WatchlistSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return WatchList.objects.filter(user=self.request.user)
    

# class UserWatchListView(APIView):
#     permission_classes = [AllowAny]
#     def get(self, request):
#         user = request.user
#         data = WatchList.objects.filter(user=user) 
#         serializer = WatchlistSerializer(data, many=True)         
#         return Response(serializer.data, status=status.HTTP_200_OK)


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
    
    # using direct approach
    # def perform_create(self, serializer):
    #     company_id = self.request.data.get('company_id')
    #     if WatchList.objects.filter(user=self.request.user, company_id=company_id).exists():
    #         raise ValidationError("Already in watchlist.")
    #     serializer.save(user=self.request.user, company_id=company_id)
        # above is equivalent to this
        # serializer.save(user=self.request.user, company=Company.objects.get(pk=company_id))


    # using serializer field
    def perform_create(self, serializer):
        company = serializer.validated_data['company_id']
        print("company", company)
        if WatchList.objects.filter(user=self.request.user, company=company).exists():
            raise ValidationError("Already in watchlist.")
        # serializer.save(user=self.request.user, company=company)
        serializer.save(user=self.request.user, company_id=company.id)

   
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