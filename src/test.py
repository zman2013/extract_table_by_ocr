import re

formulas = ['毛利总额=收入总额-销售成本总额',
    '单车价格=收入总额/汽车销量',
    '单车毛利=毛利总额/汽车销量',
    '毛利=毛利总额/收入总额',
    '经营利润=毛利总额-营业费用总额',
    '经营利润率=经营利润/收入总额']

# create a dict to store all left and right sides of the formulas
formulas_dict = {}
for formula in formulas:
  left, right = formula.split("=")
  formulas_dict[left.strip()] = right.strip()

# expand the formulas by replacing any references to other variables with their actual values
for idx, formula in enumerate(formulas):
  left, right = formula.split("=")
  for var in re.findall('[\u4e00-\u9fa5a-zA-Z]+', right):
    print(f"var: {var} right: {right}")
    
    if var in formulas_dict:
      # replace the variable with its actual value
      right = right.replace(var, '(' + formulas_dict[var] + ')')
  formulas[idx] = left + '=' + right

print(formulas)
