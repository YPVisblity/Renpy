q = Queue()
q.enqueue(1)
q.enqueue(2)
assert q.peek() == 1
assert q.dequeue() == 1
assert q.dequeue() == 2
assert q.is_empty() == True

assert simulate_print_jobs(["報告.pdf", "海報.pdf", "課表.pdf"]) == ["報告.pdf", "海報.pdf", "課表.pdf"]

print("恭喜！基礎任務全部通過，可以繼續挑戰進階任務。")