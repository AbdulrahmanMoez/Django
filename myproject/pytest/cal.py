def calculator(num1, operation, num2):
     try:
          num1 = float(num1)
          num2 = float(num2)
     #    num1 = float(input("first Number: "))
     #    num2 = float(input("Second Number: "))
     #    operation = input ("Choose Operator: (+) (*) (-) (/) (%):  ")
          match operation:
               case "+":
                    return(num1 + num2)
               case "*":
                    return(num1 * num2)
               case "-":
                    return(num1 - num2)
               case "/":
                    return(num1 / num2)
               case "%":
                    return(num1 % num2)
               case "**":
                    return(num1**num2)
               case _:
                    return("Error: Wrong Operation")

     except ZeroDivisionError:
          return ("Division by Zero is not allowed")
     except ValueError:
          return("Enter Numbers Only!: ")
     except OverflowError:
          return("Number is too large")



