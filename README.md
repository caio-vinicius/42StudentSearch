# 42 Search Student

![42 Search Student](https://github.com/42sp/part-time-selection-process-caio-vinicius/blob/media/big.png)

42 Search Student is a user command interface that helps you search for information from 42 Network students

  - have the student id
  - hit enter
  - voilà!
  
## Installation

42 Search Student requires [Python](https://www.python.org/) v3.6+ to run properly

### Linux, MacOS X

Install the dependencies required with.

```sh
$ pwd
$ ~/student-search
$ ./scripts/install_requirements.sh
```

### Docker

```sh
$ pwd
$ ~/student-search
$ ./scripts/docker_start.sh
```
## Usage

To run the script and see the user information you have to

```sh
$ cd app
$ ./student_search foobar
```
So probably you will see the output on your terminal

![example_output_42searchstudent](https://github.com/42sp/part-time-selection-process-caio-vinicius/blob/media/output.png)

The first time that you run with a specific id the script will store cache about the request, so next time you run will be much more faster.
If you don't want cache, you can use

```sh
$ ./student_search --no-cache foobar
```

So the processing will take a bit longer than previous get from cache, but worth it! 
You can clear cache without output information:

```sh
$ ./student_search --clean-cache foobar
```

If you want a bunch of unformatted information of a user you can

```sh
$ ./student_search --all foobar
```

If you want more options, you can try

| Argument | Role  |
| ------ | ------ |
| --help, -h | show this help message and exit |
| --clean-cache | delete local cache files |
| --no-cache, -n | do not use cache, redo the request |
| --raw, -r | show information in raw, without a table |
| --photo, -p | show intra url image and exit |
| --all | output all data to stdout in json |

## License
[MIT](https://choosealicense.com/licenses/mit/)
