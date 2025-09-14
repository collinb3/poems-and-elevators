# poems-and-elevators

## Elevators
Elevator simulator written in Python using LOOK algorithm. Building has 10 floors, can be changed in main function.

### Implemented features
* LOOK algorithm
  - Elevator requests are served in ascending or descending order depending on first (sorted) option. Elevator continues in one direction until all requests in that direction are served, then reverses
* Pre-programmed demo
  - Adds requests, executes, adds additional requests to illustrate reversing properties of algorithm
* Interactive mode
  - Allows user to enter options to simulate real time requests.
  - Option 1 allows for a single floor to be entered
  - Option 2 allows for a comma-separated list to be entered

### Assumptions
* Building only has 1 elevator
* Given behavior of LOOK algorithm, the elevator will remain on the last floor served until new request is received

## Not implemented features
* Floor additon mid service
  - Could allow elevator to stop on a floor if a new request is on the way to next scheduled stop
* Multiple elevators
  - Multiple elevators could allow requests to be grouped


## Poems API CLI
Typescript powered CLI that allows interface with the poetrydb API

```node
Usage: node script.js [options]

Options (Should always be wrapped in quotes if they contain spaces):
  -a, --author "author name"                    Author name to fetch poems for
  -t, --title "poem title"                      Poem title to filter results
  -p, --params "author,title"                   (Optional) additional parameters (comma-separated)
                                                    - Accepted values: author, title, lines, linecount
  -h, --help                                    Show this help message

Examples:
  node script.js -a "Emily Dickinson"
  node script.js -a "Emily Dickinson" -p "author,title,linecount"

  node script.js --title  "Youth And Age"
```