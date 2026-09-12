from django.conf import settings
from rest_framework.generics import CreateAPIView

from .local_pipeline import LocalDataPipeline
from .models import StudentOnboarding
from .serializers import StudentOnboardingSerializer


class StudentOnboardingCreateView(CreateAPIView):
    queryset = StudentOnboarding.objects.all()
    serializer_class = StudentOnboardingSerializer

    def perform_create(self, serializer):
        onboarding = serializer.save()
        if settings.LOCAL_DEVELOPMENT_MODE:
            LocalDataPipeline(settings.LOCAL_DATA_DIR).write_onboarding(
                {
                    "student_id": onboarding.student_id,
                    "student_name": onboarding.student_name,
                    "age": onboarding.age,
                    "has_learning_difficulty": onboarding.has_learning_difficulty,
                    "support_required": onboarding.support_required,
                    "parent_email": onboarding.parent_email,
                }
            )
