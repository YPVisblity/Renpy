qs = QueueUsingStacks()
qs.enqueue(1)
qs.enqueue(2)
qs.enqueue(3)
assert qs.dequeue() == 1
qs.enqueue(4)
assert qs.dequeue() == 2
assert qs.dequeue() == 3
assert qs.dequeue() == 4
print("進階挑戰通過！你已經取得「秩序管理員」進階徽章！")