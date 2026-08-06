from collections import deque

def bfs(graph, start):
    """廣度優先搜尋，回傳依拜訪順序排列的節點 list"""
    visited = {start}
    result = []
    queue = deque([start])
    # TODO: 請完成這個函式
    return result