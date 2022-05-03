"""
自定义分页逐渐
def hospital_list(request):
    # 获取自己筛选得数据
    list = models.hospital.objects.filter(**data_dict).order_by("id")、
    # 实例化分页对象
    page_object = Pagenation(request, list)

    context = {
        'search_data': search_data,
        'list': page_object.page_list,  # 分完页得数据
        'page_string': page_object.html()  # 页码
    }

    return render(request, 'hospital/hospital_list.html', context)

HTML中
    # 获取数据
    {% for obj in list%}
        {{ obj.xxx }}
    {% endfor %}
    # 分页
    <ul class="pagination" style="float: left">
        {{ page_string }}
    </ul>
"""

from django.utils.safestring import mark_safe
import copy


class Pagenation(object):
    def __init__(self, request, list, page_size=10, page_param="page", plus=5):
        """
        :param request:请求的对象
        :param list:符合条件的数据
        :param page_size:每页显示多少条数据
        :param page_param:在URL中传递的获取分页的参数
        :param plus:显示当前页的前后plus页
        """
        query_dict = copy.deepcopy(request.GET)
        query_dict._mutable = True
        self.query_dict = query_dict
        self.page_param = page_param
        page = request.GET.get(page_param, "1")
        if page.isdecimal():
            page = int(page)
        else:
            page = 1

        self.page = page
        self.page_size = page_size
        # start 每页开始数据
        # end 每页结束数据
        self.start = (page - 1) * page_size
        self.end = page * page_size

        self.page_list = list[self.start:self.end]
        # 数据总条数
        total_count = list.count()
        # 总页码
        total_page_count, div = divmod(total_count, page_size)
        if div:
            total_page_count += 1

        self.total_page_count = total_page_count
        self.plus = plus

    def html(self):

        if self.total_page_count <= 2 * self.plus + 1:
            start_page = 1
            end_page = self.total_page_count + 1
        else:
            # 当前页>plus
            if self.page <= self.plus:
                start_page = 1
                end_page = 2 * self.plus + 1
            else:
                if self.page + self.plus > self.total_page_count:
                    start_page = self.total_page_count - 2 * self.plus
                    end_page = self.total_page_count + 1
                else:
                    start_page = self.page - self.plus
                    end_page = self.page + self.plus + 1
        # 页码
        page_str_list = []

        # 首页
        self.query_dict.setlist(self.page_param, [1])
        page_str_list.append('<li><a href="?{}">首页</span></a></li>'.format(self.query_dict.urlencode()))

        if self.page > 1:
            # 上一页
            self.query_dict.setlist(self.page_param, [self.page - 1])
            prev = '<li><a href="?{}" aria-label="Previous"><span aria-hidden="true">«</span></a></li>'.format(
                self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.page_param, [1])
            prev = '<li class="disable"><a href="?{}" aria-label="Previous"><span aria-hidden="true">«</span></a></li>'.format(
                self.query_dict.urlencode())
        page_str_list.append(prev)

        for i in range(start_page, end_page):
            self.query_dict.setlist(self.page_param, [i])
            if i == self.page:
                ele = '<li class="active"><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            else:
                ele = '<li><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            page_str_list.append(ele)

        if self.page < self.total_page_count:
            # 下一页
            self.query_dict.setlist(self.page_param, [self.page + 1])
            nxt = '<li><a href="?{}" aria-label="Next"><span aria-hidden="true">»</span></a></li>'.format(
                self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.page_param, [self.total_page_count])
            nxt = '<li><a href="?{}" aria-label="Next"><span aria-hidden="true">»</span></a></li>'.format(
                self.query_dict.urlencode())
        page_str_list.append(nxt)

        # 尾页
        self.query_dict.setlist(self.page_param, [self.total_page_count])
        page_str_list.append('<li><a href="?{}">尾页</span></a></li>'.format(self.query_dict.urlencode()))

        search_string = """
            <li>
                <form method="get">
                    <div class="input-group">
                        <input name="page"
                               type="text" class="form-control" placeholder="页码">
                        <span class="input-group-btn">
                            <button class="btn btn-default" type="submit">跳转</button>
                        </span>
                    </div>
                </form>
            </li>
        """
        page_str_list.append(search_string)
        page_string = mark_safe("".join(page_str_list))
        return page_string
