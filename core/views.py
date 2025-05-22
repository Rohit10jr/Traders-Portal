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
from django.db import IntegrityError
from rest_framework import generics, permissions, status
from django.shortcuts import get_object_or_404 # Helper for getting company

critical_logger = logging.getLogger('critical_api')
logger = logging.getLogger(__name__)

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
        try:
            company = serializer.validated_data['company_id']
            if WatchList.objects.filter(user=self.request.user, company=company).exists():
                raise ValidationError("Already in watchlist.")
            serializer.save(user=self.request.user, company_id=company.id)
            # serializer.save(user=self.request.user, company=company)
            # above is equivalent to this
            # serializer.save(user=self.request.user, company=Company.objects.get(pk=company_id))
        except KeyError:
            logger.warning("Missing company_id in request")
            raise ValidationError("Missing required field: company_id")
        except Exception as e:
            logger.error(f"Unexpected error during watchlist creation: {str(e)}")
            raise ValidationError("Something went wrong. Try again later.")



class WatchlistListDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WatchlistSerializer

    def get_queryset(self):
        return WatchList.objects.filter(user=self.request.user)
        # return super().get_queryset()
    
    def perform_update(self, serializer):
        try:
            company = serializer.validated_data['company_id']
            if WatchList.objects.filter(user=self.request.user, company=company).exclude(id=self.get_object().id).exists():
                raise ValidationError("Already in watchlist.")
            serializer.save(user=self.request.user, company=company)
        except KeyError:
            logger.warning("Missing required field: company_id")
            raise ValidationError("Missing required field: company_id")
        except Exception as e:
            logger.error(f"Error updating watchlist: {e}")
            raise ValidationError("Unable to update watchlist.")
        

# logger example to store headers and payloads 

class SomeCriticalAPIView(APIView):
    def post(self, request):
        try:
            critical_logger.info("Request Headers: %s", dict(request.headers))
            critical_logger.info("Request Body: %s", request.data)

            # your logic here...
            return Response({"message": "success"})

        except Exception as e:
            logger.error("Critical API error: %s", str(e), exc_info=True)
            raise ValidationError("Something went wrong")


SENSITIVE_KEYS = {'password', 'token', 'secret'}

def sanitize_data(data):
    return {
        key: '[REDACTED]' if key.lower() in SENSITIVE_KEYS else value
        for key, value in data.items()
    }
class SomeCriticalAPIView2(APIView):
    def post(self, request):
        try:
            # Sanitize headers before logging
            headers = dict(request.headers)
            if 'Authorization' in headers:
                headers['Authorization'] = '[REDACTED]'

            # Sanitize body before logging
            body = request.data.copy()
            if 'password' in body:
                body['password'] = '[REDACTED]'

            # body = sanitize_data(request.data.copy())

            critical_logger.info("Request Headers: %s", headers)
            critical_logger.info("Request Body: %s", body)

            # your core logic
            return Response({"message": "success"})

        except Exception as e:
            logger.error("Critical API error: %s", str(e), exc_info=True)
            raise ValidationError("Something went wrong")
        

