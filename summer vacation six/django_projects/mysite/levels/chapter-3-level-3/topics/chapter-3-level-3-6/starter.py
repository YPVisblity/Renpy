# 沿用關卡 2 的 Stack 類別（此處提供完整實作，方便本關卡獨立使用）
class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[-1]

    def is_empty(self):
        return len(self.items) == 0


class QueueUsingStacks:
    def __init__(self):
        self.stack_in = Stack()
        self.stack_out = Stack()

    def enqueue(self, item):
        # TODO: 請完成
        pass

    def dequeue(self):
        # TODO: 請完成
        pass