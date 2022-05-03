from django.shortcuts import redirect
from myproject import models
from django.utils.deprecation import MiddlewareMixin


class AuthMiddleware(MiddlewareMixin):

    def process_request(self, request):
        # 如果能读到session 表示已登录 可使用功能
        if request.path_info == "/login/":
            return
        elif request.path_info == "/register/":
            return
        #
        # info_dict = request.session.get("info")
        # if info_dict:
        #     return
        # return redirect('/login/')

        info = request.session.get("info")
        # 如果登录成功
        if info:
            user_id = info.get('id')
            name = info.get('name')
            userType = info.get('userType')
            name = info.get('name')
            if userType == 1:
                user_object = models.hospital.objects.filter(name=name).first()
                request.tracer = user_object
            elif userType == 2:
                user_object = models.insurance_company.objects.filter(name=name).first()
                request.tracer = user_object
            elif userType == 3:
                user_object = models.drogs_company.objects.filter(name=name).first()
                request.tracer = user_object
            elif userType == 4:
                user_object = models.devices_company.objects.filter(name=name).first()
                request.tracer = user_object
            elif userType == 5:
                user_object = models.AdminInfo.objects.filter(name=name).first()
                request.tracer = user_object
            # user_object = models.UserInfo.objects.filter(id=user_id).first()
            # print(info)
            return
        return redirect('/login/')
        # user_object = models.UserInfo.objects.filter(id=user_id).first()
        # request.tracer = info
        # print(user_object)
    # def process_request(selfs, request):

# userType = info.get('userType')
# 拿到登录对象的用户类型
# 读取该用户类型数据库的数据
