from django.shortcuts import render
from django.test import RequestFactory
from djoser.views import UserViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

class CustomActivationView(APIView):
    def get(self, request, uid, token):
        try:
            # Create a fake POST request
            factory = RequestFactory()
            post_request = factory.post(
                f'/activate/{uid}/{token}/',  
                data={"uid": uid, "token": token}
            )

            # Set necessary attributes
            post_request.user = request.user
            post_request.session = request.session

            # Call Djoser’s activation method
            user_view = UserViewSet.as_view({'post': 'activation'})
            response = user_view(post_request, uid=uid, token=token)
            
            # Check if activation was successful (204 means success but no content)
            if response.status_code == 204:
                return Response(
                    {"message": "Your account has been successfully activated! 🎉"},
                    status=status.HTTP_200_OK
                )
            return Response(response.data, status=response.status_code)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# from django.test import RequestFactory
# from djoser.views import UserViewSet
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.views import APIView

# class CustomActivationView(APIView):
#     def get(self, request, uid, token):
#         try:
#             # Create a fake POST request
#             factory = RequestFactory()
#             post_request = factory.post(
#                 f'/activate/{uid}/{token}/',  # Manually set the correct URL
#                 data={"uid": uid, "token": token}
#             )

#             # Set necessary attributes
#             post_request.user = request.user
#             post_request.session = request.session

#             # Call Djoser’s activation method
#             user_view = UserViewSet.as_view({'post': 'activation'})
#             response = user_view(post_request, uid=uid, token=token)
            
#             return Response(response.data, status=response.status_code)
#         except Exception as e:
#             return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

