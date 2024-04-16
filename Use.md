# User Documentation

## Basic Use

for the simplest fucntional use i have implemented a Cli


The project has two modes

    1. Data Generation Mode
    2. Timetable Generator mode
  

### Data Generation Mode

This is used to generate mockup data for the purpose of testing the working of
the program.
We are able to test if the program works with a predefined set of data that we
can customise based on what we are testing.
Basically checking for logical errors.

### Timetable Generator Mode

This is the functional part of the entire project. It implements processes and
procedures towards producing an optimal timetable based on the inputs given.



## Command line Interface

The cli uses flags to set and input commands, at the current version alot
of `json` attributes are in use, with use of `arrays`, `dictionaries` and
`lists` to represent data, except in notable special cases and future
versions

All the modes have inbuilt flags and dont intefere withe each other but can be
optionally used for similar operations.

| Long Version         | Short Version | Use                                                                                                                               | Accompanied by                                                     |
| :------------------- | :------------ | :-------------------------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------------- |
| `--output_type`    | `-tp`       | Used to specify the type of formart the output file should be in. check*`info.md`* for supported output types                   | *`filename`*                                                   |
| `--output_file`    | `-o`        | Specifying where the result will be written                                                                                       | *`filename`*                                                   |
| `--data_generator` | `-dg`       | For enetering data generator mode. this accompanied with other flags                                                              | *`None`*                                                       |
| `--input_file`     | `-i`        | Specifying the input file for specifying data generation or for data inputs                                                       | *`filename`*                                                   |
| `defaults`         |               | Load in default values                                                                                                            | *`None`*                                                       |
| `--configuration`  | `-c`        | Specify configuration file Ussually a json file, if not defined then a prompt to create one on the command line will be initiated | *`filename`*                                                   |
| `--write_config`   | `-wc`       | This will initite a prompt to manually write the configuration data                                                               | *`None`*                                                       |
| `--algorithm`      | `-a`        | This defines what algorithm to use from the ones available                                                                        | Either of<br />constraint_satisfaction<br />genetic<br />annelaing |
| `--iterations`     | `-t`        | Defines the number of run times or iterations                                                                                     | `any number`                                                     |
| `--limit`          | `-l`        | The limit which the program cannot exceed, bydefault it is `0` which means no limit                                             | `any number`                                                     |
| `--saturation`     | `-s`        | Continue until saturation is reached                                                                                              |                                                                    |

*`*None`* - Specifically Reffers to nothing following after a flag

## Data Generation

Generating Mock data is crucial to making sure the entire program works. we are able to generat edata in the following ways

    1. Text file with instructions
    2. Simple Command with prompt menu
    3. Pre-saved confiugartaion
    4. Manually typed in configuration

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

    >> python project.py -- --input file.txt
or

    >> python project.py -dg -i file.txt

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

    >> python project.py -dg

or

    >> python project.py --data_generator

### Presaved Configuration

This assumes that you have the configuration data somewhere else and it will be imported and used in the above commands, the only thing to do is add a `-wc` or `--write_config` flag and then filepath to the configuration data file. it can be used like so

    >> python project.py -dg -c path/to/file
or

    >> python project.py -data_generator -configuration path/to/file

### Manually Written Configuration

this initiates a prompt to input configuration with a series of questions.

    >> python project.py -dg -wc
or

    >> python project.py -data_generator -write_config
