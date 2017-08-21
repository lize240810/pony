from django.shortcuts import render
from app.modules.common.auth import login_required
from app.models.account.account import UserInfo


@login_required
def chat_module_handler(request):
    result = dict()
    result["user_info"] = UserInfo.query_format_info_by_user_id(request.META["user_info"].id)
    return render(request, "chat/chat.html", result)
