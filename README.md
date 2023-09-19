# EuphyLang

Euphy is an high-level, object-oriented programming language created by Joseph Evans.
It serves as a prototype to a type system that contains both static and dynamic types.

```
print("Hello Euphy!")

class Euphy {
    dynamic value;

    none setNumber(number value) {
        this.value = value
    }

    none setString(string value) {
        this.value = value
    }
}

```

Version: 1.0
It is currently in development and open to contibution.
\
Discord: https://discord.gg/Yck2Y9zNw

## Getting Started

Requirements:
    
1) Python 3. [Download it here](https://www.python.org/downloads)

Guide:
1) Clone the repository locally to your computer.

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
   print(55)
   ```

   Running code from a file
   ```
   -r hello_world.euphy
   ```
