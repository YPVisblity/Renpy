from django.shortcuts import render

def post_list(request):
    posts = [
        {'title': 'Django 入門', 'content': '學習如何建立 App'},
        {'title': '命名空間的重要性', 'content': '避免模板衝突'}
    ]
    # 使用命名空間路徑：blog/index.html
    return render(request, 'blog/index.html', {'posts': posts})
