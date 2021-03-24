from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework import mixins, viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework.renderers import JSONRenderer
from .models import SessionModel, PlayerModel, ProducerModel, BrokerModel, TransactionModel
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .serializers import SessionSerializer, PlayerSerializer, ProducerSerializer, BrokerSerializer, \
	TransactionSerializer
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import action


class SessionViewSet(ModelViewSet):
	queryset = SessionModel.objects.all()
	serializer_class = SessionSerializer
	permission_classes = [IsAdminUser]

	@action(methods=['put'], detail=True,
			url_path='start', url_name='session_start', permission_classes=[IsAdminUser])
	def start(self, request, pk):
		session_instance = self.get_queryset().get(pk=pk)
		serializer = SessionSerializer(
			session_instance,
			data={
				"name": session_instance.name,
				"turn_count": session_instance.turn_count,
				"status": "created",
			})
		if not serializer.is_valid():
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

		try:
			serializer.save()
		except Exception as e:
			return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
		return Response(serializer.data, status=status.HTTP_200_OK)

class PlayerViewSet(ModelViewSet):
	queryset = PlayerModel.objects.all()
	serializer_class = PlayerSerializer
	permission_classes = [IsAdminUser]


class GetOrUpdatePlayerViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
																				viewsets.GenericViewSet):
	queryset = PlayerModel.objects.all()
	serializer_class = PlayerSerializer
	permission_classes = [IsAuthenticated]


class ProducerViewSet(ModelViewSet):
	queryset = ProducerModel.objects.all()
	serializer_class = ProducerSerializer
	permission_classes = [IsAdminUser]


class BrokerViewSet(ModelViewSet):
	queryset = BrokerModel.objects.all()
	serializer_class = BrokerSerializer
	permission_classes = [IsAdminUser]


class TransactionViewSet(ModelViewSet):
	queryset = TransactionModel.objects.all()
	serializer_class = TransactionSerializer
	permission_classes = [IsAdminUser]


@api_view(['PUT'])
@renderer_classes([JSONRenderer])
@permission_classes([IsAdminUser])
def count_turn_view(request, pk):
	session_instance = get_object_or_404(SessionModel, pk=pk)
	if request.method == 'PUT':
		session_instance.save()
		return Response(status=status.HTTP_200_OK)
	else:
		return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
@renderer_classes([JSONRenderer])
@permission_classes([IsAuthenticated])
def join_session_view(request, session_pk):
	session_instance = get_object_or_404(SessionModel, pk=session_pk)

	try:
		player_instance = PlayerModel.objects.get(user=request.user.id)
		if player_instance.session.id == session_instance.id:
			return Response({
				'error': 'You\'ve already joined this session!'
			}, status=status.HTTP_400_BAD_REQUEST)
		elif not player_instance.session.id == 0:
			return Response({
				'error': 'You\'ve already joined another session!'
			}, status=status.HTTP_400_BAD_REQUEST)
	except PlayerModel.DoesNotExist:
		player_serialized = PlayerSerializer(data={
			'nickname': request.user.username,
			'user': request.user.id,
		})
		if not player_serialized.is_valid():
			return Response(player_serialized.errors, status=status.HTTP_400_BAD_REQUEST)
		player_instance = player_serialized.save()

	player = PlayerSerializer(player_instance, data={
			'session': session_instance.id,
	})
	if player.is_valid():
		player.save()
		return Response(player.data, status=status.HTTP_200_OK)
	return Response(player.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['DELETE'])
@renderer_classes([JSONRenderer])
@permission_classes([IsAuthenticated])
def leave_session_view(request, session_pk):
	session_instance = get_object_or_404(SessionModel, pk=session_pk)
	if not session_instance.player.filter(user=request.user.id).exists():
		return Response({
			'error': 'You\'re not in this session!',
		}, status=status.HTTP_400_BAD_REQUEST)

	try:
		session_instance.player.get(user=request.user.id).delete()
	except Exception as e:
		# TODO: Exception handler
		return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

	return Response(status=status.HTTP_204_NO_CONTENT)

