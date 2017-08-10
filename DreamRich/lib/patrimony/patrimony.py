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

  def monthly_income(sources_of_income):
    return Patrimony.sum_elements(sources_of_income)

  def monthly_income_bonus(sources_of_income, vacation_bonus, thirteenth_salary):
    MONTHS = 12
    total = Patrimony.sum_elements(sources_of_income)

    if(vacation_bonus != 0):
      total += vacation_bonus / MONTHS
    
    if(thirteenth_salary != 0):
      total += thirteenth_salary / MONTHS

    return total