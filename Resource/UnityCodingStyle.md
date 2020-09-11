# Unity C# Style Guide
Our overarching goals are **conciseness**, **readability** and **simplicity**. Also, this guide is written to keep **Unity** in mind. 

## Table of Contents
- [Unity class layout](#UnityClassLayout)
- [Nomenclature](#nomenclature)
  + [Namespaces](#namespaces)
  + [Classes & Interfaces](#classes--interfaces)
  + [Methods](#methods)
  + [Fields](#fields)
  + [Parameters](#parameters--parameters)
  + [Misc](#misc)
- [Declarations](#declarations)
  + [Access Level Modifiers](#access-level-modifiers)
  + [Fields & Variables](#fields--variables)
  + [Classes](#classes)
  + [Interfaces](#interfaces)
- [Brace Style](#brace-style)


## UnityClassLayout
### The layout of a Unity Class should be:  
(from top to bottom)  
1. sub class/struct/enum defination
2. static fields
3. static funcions
4. config fields in unity inspector
5. public fields
6. private fields
7. unity monobehaviour callbacks
8. override funcitons
9. public methods
10. private methods
### A Example:
```csharp
public class UnityClass:Monobehaviour{
    # region sub class/struct/enum defination
    public class SubClass{
        ...
    } 
    enum EType{
        ....
    }
    # endregion

    # region static fileds
    public static UnityClass Instance;
    # endregion

    # region static funcions
    public static UnityClass StaticFunc(){
        ....
    };
    # endregion

    # region config fields in nnity inspector
    [SerializableField]
    private bool configField;
    # endregion

    # region public fields
    private int publicInt;
    # endregion

    # region private fields
    private int privateInt;
    # endregion

    # region unity monobehaviour callbacks
    private void Awake(){
        ...
    }
    private void Start(){
        ...
    }
    # endregion

    # region override funcitons
    protected override void FuncFromBase(){
        ...
    }
    # endregion

    # region public methods
    public void PublicMethod(){

    }
    # endregion

    # region private methods
    public void PublicMethod(){

    }
    # endregion
}
```
## Nomenclature

On the whole, naming should follow C# standards.

### Namespaces

Namespaces are all **PascalCase**, The exception to this rule are acronyms like GUI or HUD, which can be uppercase:

**AVOID**:

```csharp
com.raywenderlich.fpsgame.hud.healthbar
```

**PREFER**:

```csharp
RayWenderlich.FPSGame.HUD.Healthbar
```

### Classes & Interfaces

Classes and interfaces are written in **PascalCase**. For example `RadialSlider`. 

### Methods

Methods are written in **PascalCase**. For example `DoSomething()`. 

### Fields

All non-static fields are written **camelCase**. Per Unity convention, this includes **public fields** as well.

For example:

```csharp
public class MyClass 
{
    public static int theAnswer = 42;
    public int publicField;
    int packagePrivate;
    private int myPrivate;
    protected int myProtected;
}
```

**AVOID:**

```csharp
private int _myPrivateVariable
```

**PREFER:**

```csharp
private int myPrivateVariable
```
### Properties

All properties are written in **PascalCase**. For example:

```csharp
public int PageNumber {
    get { return pageNumber; }
    set { pageNumber = value; }
}
```

### Parameters

Parameters are written in **camelCase**.

**AVOID:**

```csharp
void DoSomething(Vector3 Location)
```

**PREFER:**

```csharp
void DoSomething(Vector3 location)
```

Single character values are to be avoided except for temporary looping variables.

### Misc

In code, acronyms should be treated as words. For example:

**AVOID:**

```csharp
XMLHTTPRequest
String URL
findPostByID
```  

**PREFER:**

```csharp
XmlHttpRequest
String url
findPostById
```

## Declarations

### Access Level Modifiers

Access level modifiers should be explicitly defined for classes, methods and member variables.

### Fields & Variables

Prefer single declaration per line.

**AVOID:**

```csharp
string username, twitterHandle;
```

**PREFER:**

```csharp
string username;
string twitterHandle;
```

### Classes

**Exactly one class per source file**, although inner classes are encouraged where scoping appropriate.

### Interfaces

All interfaces should be prefaced with the letter **I**. 

**AVOID:**

```csharp
RadialSlider
```

**PREFER:**

```csharp
IRadialSlider
```

## Brace Style
**AVOID:**
```csharp
class MyClass
{
    void DoSomething()
    {
        if (someTest)
        {
          // ...
        }
        else
        {
          // ...
        }
    }
}
```


**PREFER:**
```csharp
class MyClass {
    void DoSomething() {
        if (someTest) {
          // ...
        } else {
          // ...
        }
    }
}
```

Conditional statements are always required to be enclosed with braces,
irrespective of the number of lines required.

**AVOID:**

```csharp
if (someTest)
    doSomething();  

if (someTest) doSomethingElse();
```

**PREFER:**

```csharp
if (someTest) {
    DoSomething();
}  

if (someTest){
    DoSomethingElse();
}
```