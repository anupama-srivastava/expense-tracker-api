from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import SharedExpense, FamilyBudget, ExpenseChallenge
from .serializers import SharedExpenseSerializer, FamilyBudgetSerializer, ExpenseChallengeSerializer


class SharedExpenseViewSet(viewsets.ModelViewSet):
    queryset = SharedExpense.objects.all()
    serializer_class = SharedExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SharedExpense.objects.filter(users=self.request.user)

    def perform_create(self, serializer):
        instance = serializer.save()
        instance.users.add(self.request.user)


class FamilyBudgetViewSet(viewsetsI have gathered the necessary information regarding the existing models and serializers for the social features. Now, I will create a comprehensive plan for implementing the social and collaborative features in Phase 3.

### Plan for Implementing Phase 3: Social & Collaborative Features

#### Information Gathered:
- **Models**:
  - `SharedExpense`: Represents shared expenses among users.
  - `FamilyBudget`: Represents family budgets with multiple users.
  - `ExpenseChallenge`: Represents expense challenges among users.
  - Existing models for social feed and notifications are also present.
  
- **Serializers**:
  - Serializers for `SharedExpense`, `FamilyBudget`, and `ExpenseChallenge` are already defined.

#### Plan:
1. **Shared Expenses**:
   - Implement API endpoints to create, retrieve, update, and delete shared expenses.
   - Add functionality to invite users to participate in shared expenses.

2. **Family Budgets**:
   - Implement API endpoints to create, retrieve, update, and delete family budgets.
   - Allow family members to view and manage the budget collaboratively.

3. **Expense Challenges**:
   - Implement API endpoints to create, retrieve, update, and delete expense challenges.
   - Allow users to join and participate in challenges.

4. **Social Feed**:
   - Implement API endpoints to create, retrieve, update, and delete social feed posts.
   - Allow users to comment on and like posts.

5. **Notifications**:
   - Implement API endpoints to retrieve notifications for users based on their activities.

#### Dependent Files to be Edited:
- `apps/social/views.py`: To implement the API views for the above features.
- `apps/social/urls.py`: To define the URL patterns for the new endpoints.

#### Follow-up Steps:
- Implement the views and URL patterns.
- Test the new features using Postman.
- Update the documentation to reflect the new features.

<ask_followup_question>
<question>Please confirm if I can proceed with this plan or if you have any feedback or additional requirements.</question>
</ask_followup_question>
