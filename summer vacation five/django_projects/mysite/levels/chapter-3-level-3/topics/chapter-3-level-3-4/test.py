assert infix_to_postfix("(A+B)*C") == "AB+C*"
assert infix_to_postfix("A+B*C") == "ABC*+"
print("進階挑戰通過！你已經取得「堆疊守衛」進階徽章！")