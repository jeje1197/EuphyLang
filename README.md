# EuphyLang

Euphy is a general-purpose, multi-paradigm programming language created by Joseph Evans. It serves as a prototype that allows developers to use both static and dynamic
types in their programs and define how they interact. EuphyLang is currently in development and open to contibution.

Version: 0.0.1


**If you want to try EuphyLang now, check out the [Getting Started](#getting-started) section.**

**If you want to contribute to EuphyLang, check out the [Contribution](#contribution) section.**

<br/>

## Static and Dynamic Typing


In Euphy, you get your choice between statically-typed variables and dynamically-typed variables.

A statically-typed variable can be declared as follows. Once a variable has been declared with a type, it can no longer accept values of a different type. 
This helps to ensure program correctness.
```
string s = "A string"
print(s)

s = 24 // Type error
```



To declare a dynamically-typed variable use the dynamic keyword. Variables declared this way will accept values of any type. This can be helpful for writing code in 
the early stages of a project.
```
dynamic d = "A string"
print(d)

d = 24 // Valid code
```


## Defining Cast Behavior

An unique feature of Euphy is cast controlling - the ability to choose when and how an
implicit casting occurs. Take a look at the following example. Can you guess what the output is here?

```
string converter(number n) {
    if (n < 0) {
        return "A negative value"
    } else if (n == 0) {
        return "Zero"
    } else {
        return "A positive value"
    }
}

#cast number -> string converter

string value = 64
print(value)

#uncast number -> string
```
The output is "A positive value". In the above program, we used a macro-like syntax to reference a processor function that is called on the value when a string variable is passed a number value. After the print, we dereference the function.



## Getting Started

Requirements:
    
1) Python 3. [Download it here](https://www.python.org/downloads)

Guide:
1) Clone the repository locally to your computer. Alternatively, you can download and unzip the project.

   ```
   git clone https://github.com/jeje1197/EuphyLang.git
   ```
    
2) Navigate to the root directory of the project
3) Run the Euphy interpreter

   ```
   python euphy.py
   ```

4) The interpreter will open to the REPL (Read-Eval Print Loop). Here you can run code directly or read from a file.

   Running code in the REPL
   ```
   print("Hello Euphy!")
   ```

   Running code from a file
   ```
   -r hello_world.euphy
   ```

## Contribution

You can contribute to EuphyLang in the following ways:
- Making changes and opening a pull request
- Writing a few test programs
- Reporting bugs
