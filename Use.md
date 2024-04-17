# User Documentation

## Basic Use

for the simplest fucntional use i have implemented a Cli

The project has two modes

    1. Data Generation Mode
    2. Timetable Generator mode

## Terminal Commands

Running `python project.py` will run the deafult setting, which generates a data.json file and send it

All the modes have inbuilt flags and dont intefere with each other but can be
optionally used for similar operations.

| Short<br />Version | Long<br />Version               | argument               | explanation                                                                                             |
| ------------------ | ------------------------------- | ---------------------- | ------------------------------------------------------------------------------------------------------- |
| `-e`             | `--echo`                      | `on` or `off`      | allows print on the screen                                                                              |
| `-srm`           | `None`                        | `most` or `least`  | Tells the constraint solver to start with variables with the<br />most or least values in their domain |
| `-o`             | `--output-file`               | string for a file name | where the output file will be and its name                                                              |
| `-mdg`           | `--manual-data-generation`    | None                   | The cli will ask some questions about the number<br />of objects your qant                              |
| `-tdg`           | `--text-file-data-generation` | None                   | To Create data from a text file with instructions                                                       |
| `-tf`            | `--text-file`                 | string of a text file  | The name of the text file from which instructions<br />are taken from                                   |
| `run`            |                                 | None                   | if arguments have been passed it is necessary to tell<br />the algorithim to run                        |

*`*None`* - Specifically Reffers to nothing following after a flag

## Data Generation

Generating Mock data is crucial to making sure the entire program works. we are able to generate data in the following ways

    1. Text file with instructions
    2. Simple Command with prompt menu

### Text Files with Instructions

Generating mock data using instructions from a `txt` file is perhaps the easiest way to generate data fast.

The text file should contain very important fields in a very specifc formart.

```
instructors: 4
rooms: 7
programmes: 10
units: 10
```

Order does not really matter in this case but the *`colon`* right after the key and the *`sinlge spacing`* right before the value are important for the program to understand ypur request.

The follwoing would be the command

> ```
> $ python project.py --text-file-data-generation --text-file file.txt
> ```

or

> ```
> $ python project.py -tdg -tf file.txt
> ```

### Simple command with prompt menu

this brings up a prompt menu where you choose the specific data you want. its great for single data entry
The prompt menu has the following

```
Genarate mock data
Enter name of output file: testing.json
1. Instructors
2. Programmes, Units and Groups
3. Rooms
4. All Input Data
Pick one of the above:
```

first, will be entering the output file name
then pick one of the following to generate random data types

The prompts have been made user friedly asking questions and providing data based on input

The following command is used

> ```
> $ python project.py -mdg
> ```

or

> ```
> $ python project.py --manual-data-generation
> ```

## Timetable Generator Mode

This is the functional part of the entire project. It implements processes and procedures towards producing an optimal timetable based on the inputs given.

There are two ways to run inputs into the constraint solver

1. Automatic Handling
2. With arguments

### Automatic Handling

This is the basic setting to just run with default settings

> ```
> $ python project.py
> ```

This Gives you
    1. Data
        a. 4 instructors
        b. 5 groups
        c. 5 rooms
        d. 20 Units
    2. Data file named `data.json` inside `Data\Outputs` folder
    3. Constraint Solver with no search rearangemnent Method
    4. The output file (timetable) named `final.json` inside  `Data\Outputs` folder

### With Arguments

This allows more customised settings, for example the following, the following are arguments that can be used
    1. Echo
    2.

> Arguments disable the constraint solver hence for the constraint solver to proceed the `run` flag has to be included

#### Echo

`Echo` prints out all the processes that are happening, and this is the deafult setting but it can also be disabled with `--echo` or `-e` flag. the only acceptable values for `--echo` are `on` or `off`. `on` is the default and `off` disables all extra prints and leaves only the essential ones i.e Timetable printing.

> ```python
> $ python project.py --echo off run
> ```

or

> ```python
> $ python project.py --e off run
> ```
