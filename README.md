# EuphyLang

Euphy is a general-purpose programming language created by Joseph Evans.
It serves as a prototype for a system that allows developers to use both static and dynamic
types and define how they interact.


**If you want to try EuphyLang now, check out the [Getting Started](#getting-started) section.**

**For updates, discussion or help, join the community [discord](https://discord.gg/Yck2Y9zNw).**


An unique feature of Euphy is cast controlling - the ability to choose when and how an
implicit casting occurs. Take a look at the following example:

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

Version: 1.0

It is currently in development and open to contibution.


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
