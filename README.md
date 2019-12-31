# bamboo-jump
An experimental feature to jump start a new bamboo-lib ETL pipeline

## To Do List
* Read YAML file
* Design ETL base document
* Design classes for each element:
    - External Functions/Libraries
    - Bamboo Functions/Libraries
    - Parameters
    - Steps
    - Sources
    - Databases
    - Main/Testing
    - Coordinator

## Structure of the Pipeline with Classes
ExternalLibs() -> parent_dir*
BambooLibs()

StepsDeclaration()

ParamsDeclaration() -> ingest*, output-db*

StepsUse() -> parent_dir*, ingest*

MainDeclaration()

## Special Classes
Coordinator() -> Coordinates all classes
ConnectionsFile() -> Reads sources and databases 