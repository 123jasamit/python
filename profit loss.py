#profit loss
ActualCost = float(input("Please Enter The Actual Product Price"))
salecost = float(input("Please Enter The Sale Amount"))
if (salecost > ActualCost):
 amount =salecost - ActualCost
 print("total profit = ",amount)
else:
 print("No Profit!!!")