class Patrimony:

  def sum_elements(array):
    total = 0
    for element in array:
      total += element

    return total

  def current_investment_net(assets, debts):
    asset = Patrimony.sum_elements(assets)
    debt = Patrimony.sum_elements(debts)
    
    return asset - debt

  def current_investment_immobilized(assets):
    return Patrimony.sum_elements(assets)