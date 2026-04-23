
# Own Interpreter

Small iterpreter made for future game ideas. Something similar to bitburner where you can code to automate stuff. Eg.: hack() to earn money and using a "while" loop you can automate it etc.


## Running it

To run anything with it, download and extract. Then do:

```bash
    python3 main.py filename.mark
```
    
And it will execute the code.


## Support

Keyword and usage:

```
VAR name = value
```

```
DO number 
(Code here)
END
```

```
IF condition THEN
(Code here)
END
```

```
print expression
```
## Usage/Examples

```javascript
VAR test = "hello"
VAR num1 = 1 + 8
VAR num2 = 7

IF test == "hello" THEN
    print "inside if"
    print "inside if"
    
    IF num1 >= num2 THEN
        print "Second if statement"
    END
END

print "Variable value below:"
print test

VAR it = 0

DO 5
    print it
    VAR it = it + 1
END
```

