# 42 Search Student

![42 Search Student](https://github.com/42sp/part-time-selection-process-caio-vinicius/blob/media/big.png)

42 Search Student is a user command interface that helps you search for information from 42 Network students

  - have the student id
  - hit enter
  - voilà!
  
## Installation

42 Search Student requires [Python](https://www.python.org/) v3.6+ and [Pip](https://pip.pypa.io/en/stable/) v9.0.1+ to run properly

```sh
$ git clone https://github.com/42sp/part-time-selection-process-caio-vinicius student-search
$ cd student-search
```

### Linux

Install the dependencies required with

```sh
$ ./scripts/install_requirements.sh
```

### Docker

```sh
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
If you do not want the cache to be consulted and need new information, you can do:

```sh
$ ./student_search --no-cache foobar
```

So the process will take a little longer compared to the cache, but it's worth it
If you want to clear the cache and just that, without making another request, you can with

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

## Unit Test

```sh
$ cd tests/
```

You can run multiple tests at once

```sh
$ ./test.py
```
When you do this, the test will consider a "random" list of student ids and perform the search for information for each student
There are 3 lists (0, 1 and 2). The default is 1, you can choose between these three like this

```sh
$ ./test.py 3 
```

You can pass multiple users if you specify **id** one after the other and each one will be consulted too

```sh
$ ./test.py id benny xitope
```

| Argument | Role  |
| ------ | ------ |
| list | 0, 1 and 2 to ids list |
| id | ids to test |

## License
[MIT](https://choosealicense.com/licenses/mit/)
