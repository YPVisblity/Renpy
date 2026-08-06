path = shortest_path(graph, "A", "E")
assert path in (["A", "B", "D", "E"], ["A", "C", "D", "E"])
assert shortest_path(graph, "A", "A") == ["A"]

print("恭喜完成所有關卡！你已經取得「迷宮之城探險家」徽章，正式畢業成為資料結構大師！")