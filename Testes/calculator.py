firstOperand = input("Enter First Operand: ")
firstOperand = int(firstOperand)

operator= input('Enter Operator(+,-,*,/)\n')

secondOperand = input('Enter Second Operand: ')
secondOperand = int (secondOperand)

if(operator == '+'):
    Answer = firstOperand+secondOperand
if(operator == '-'):
    Answer = firstOperand-secondOperand
if(operator == '/'):
    Answer = firstOperand/secondOperand
if(operator == '*'):
    Answer = firstOperand*secondOperand
if(operator == '%'):
    Answer = firstOperand%secondOperand
if(operator == '//'):
    Answer = firstOperand//secondOperand
if(operator == '**'):
    Answer = firstOperand**secondOperand

print("Answer =", Answer)







