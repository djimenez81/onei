# ONEI


## What is this project about?

This research project pretends to develop a specific domain language that is 
intended to be used to develop Multi Agent Based Simulations (MAS), or to 
develop specific agents, or environments, etc.


## How does a MAS work?

In general, a MAS is a virtual environment, or we could call it a world, that is 
divided into regions of some sort, and these regions have their own 
characteristics, and potentially resources. These resources can be accessed by 
agents, that is, virtual beins with "agency", and act on the environment in a 
discrete time. Also, there might be items, objects without agency, around the
environment. 

For example, we could think of a chessboard as the environment, each cell on the
board as a region or patch, and the chess pieces as the agents. 


## Structure of development

One of the ideas of this project is that the system generated will be robust 
enough to be used both for rapid development and prototyping (something that is
often easier to do in languages like Python), and at the same time, that allows
the flexibility to scale easily, and to compile into a fast running executable
file. 

In general there will be two types of files: Definition files and script files.
The script files should only be used on prototyping and with the interpreter. 
The main idea is that this will allow to instantiate objects (environment, 
patches, items, agents, etc), and test them, to try functions debug them, etc.
Script files will never be part of a compilation.

A definition file contains the specification of functions and objects. There are
different types of objects, that will be implemented with different templates. 
In general, most of them will correspond to what is a class or an object on 
other programming language, but as they will have some specific rolls into a 
simulation, they will be implemented with thouse templates, to ensure they will 
comply with the requirements and restrictions of the roll they follow.

A definition file might be a library (where objects and functions are 
implemented) or it might be a simulation (thus there will be a setup that 
specifies the environment, patches, agents, items and rules to use). Also, as 
there might be libraries, a definition file might have import statements at the 
very beginning of the same. 


## How are we planning to do this?

There are several parts to a simulation. The upper most layer is the setup,
followed by the environment, the patches, the agents, the items, the exchanges,
the rules, tables and messages.

### setup

The set up is where the user sets the type of environment to use, with the 
respective parameters, the patches that will be used (sometimes the environment 
itselfwill specify the types of patches to use, and there will not be a need to 
further specification). 

### environment

The environment is the world where everything else is contained. An environment
cannot have other environments as attibutes, nor can it have agents or items as 
attributes.

### patch

The patches are regions where the things move around. Patches are separate from 
environment for modularity, and also, to simplify parallel processing. A patch 
cannot have other patches  as attributes (this second one could be change if we 
see a need that justify it).

### agent

Inside the different patches, there are agents. An agent cannot have other 
agents as its attributes. An agent can sense its environment and react to it. 
An agent has states (alive, male/female), has attributes of different kinds 
(age, weight, amount of money, etc). Also, it could be a set of genes, etc, all
depends on the application. An important distinction is that an agent can have
items as an attribute.

### item

An item is basically a thing that agents have or use. Items do not have agency
of their own, but they do have functions. They might have states, attributes of 
any kind. An item might have other items as attibutes, as a car has four tires,
a shirt has buttons, etc. 

### exchange

This is a type of object that I am unsure if it should be implemented, but I 
think it must be considered. An exchange is pretty much a table where messages
are stored in wait to be processed. For example, an agent "dies", then it send 
a message of "Dude! I am dead!" to the patch. The Patch takes the ID of such 
agent from its roster. First, the patch puts it on its exchage, and when it 
comes time to process it, it takes the ID from its roster, and then sends a 
notification to the environment. 

### messages

A message is a small structure, basically a container, to exchange information 
between different parts of a simulation. 

### rule

A rule, as the name suggests, is an object that dictates the behavior of an 
object on a simulation, whether they are items, agents, patches or environments, 
or also, it might govern the interactions between some of those.

### table

A table is basically a sort of spreadsheet, often it serves as a database.


## Parts of the language

There are a few things that we need to consider for including on the language.

* Primitive types
* Data structures
* File I/O
* Graphic panes
* Statistical analysis

### Primitive types

The following are the primitive data types that we should consider as a start:

* Booleans
* Integers
* Floating Point Real Value
* Strings



### Data structures

* Lists
* Arrays
* Dictionaries
* Tables (if we decide not to allow them as extendables)



## Libraries that should be implemented.

The following are a few things that should be implemented. It could be a good 
idea (or at least a good excercise) to implement it directly in ONEI.

* Statistics
* Transcendental functions
* 

## Things we definitely need

* Variables: We need void and NULL.
* We need to define how inheritance (class inherits all attributes and methods 
  that have not been overwritten by the class itself).
* How to implement pointers.


### How to Procede Starting Now

Our first idea will be to implement the lexer and the parser, and after that 
implement a routine that executes directly from the AST.