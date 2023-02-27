<!-- markdownlint-disable -->
[![Stand With Ukraine](https://raw.githubusercontent.com/vshymanskyy/StandWithUkraine/main/banner2-direct.svg)](https://stand-with-ukraine.pp.ua)

# AnyTest [![Lint](https://github.com/timfjord/AnyTest/actions/workflows/lint.yml/badge.svg)](https://github.com/timfjord/AnyTest/actions/workflows/lint.yml) [![Test](https://github.com/timfjord/AnyTest/actions/workflows/test.yml/badge.svg)](https://github.com/timfjord/AnyTest/actions/workflows/test.yml)
<!-- markdownlint-enable -->
Run any test from Sublime Text

A Sublime Text 3/4 package whose main idea is to automatically detect a test framework for the given file and run it. It is a Sublime Text interpretation of the awesome [vim-test](https://github.com/vim-test/vim-test) plugin.

Currently, the following test frameworks are supported (more test frameworks are coming soon):

|       Language | Test framework                                  | Identifiers                                                 |
|---------------:|:------------------------------------------------|:------------------------------------------------------------|
|     **Elixir** | ESpec, ExUnit                                   | `espec`, `exunit`                                           |
|       **Java** | JUnit(Maven and Gradle)                         | `junit`                                                     |
| **JavaScript** | Jest, Mocha, Vitest                             | `jest`, `mocha`, `vitest`                                   |
|     **Python** | PyTest, PyUnit                                  | `pytest`, `pyunit`                                          |
|       **Ruby** | Cucumber, M, Minitest, Rails, RSpec, Test Bench | `cucumber`, `m` ,`minitest`, `rails`, `rspec`, `test_bench` |
|       **Rust** | Cargo                                           | `cargotest`                                                 |
|     **Switft** | Swift Package Manager                           | `swiftpm`                                                   |

Feel free to [open an issue](https://github.com/timfjord/AnyTest/issues/new) with a test framework request as those test frameworks will be added first.

## Installation

1. Install the [Sublime Text Package Control](https://packagecontrol.io/) package if you don't have it already.
2. Open the command palette and start typing `Package Control: Install Package`.
3. Enter `AnyTest`.

## Usage

The main command that the package exposes is `any_test_run`. It supports 4 scopes:

- `suite`: runs the whole test suite (based on the current file)
- `file`: runs all tests in the current file
- `line`: runs the test nearest to the current line(cursor)
- `last`: runs the last test

The package tries to detect a test framework based on the current file.
When the framework is detected the package generates a command and runs it using the selected runner.  
When the `edit` flag is passed to `true` then the command can be edited before running.  
And finally, if the `select` flag is passed to `true` then the auto-detection feature is bypassed
and the quick panel with all available test frameworks is shown allowing to select a test framework manually.

The package comes with polyfills for test frameworks that don't have built-in support for running tests for the current line.  
All the polyfills have been borrowed from the `vim-test` plugin and adapted for Sublime Text.

All the package commands can be found in [Default.sublime-commands](https://github.com/timfjord/AnyTest/blob/main/Default.sublime-commands)

By default the package doesn't define any key bindings, run `Preferences: AnyTest Key Bindings` to define your own bindings.

## Configuration

The package can be configured either globally or at the project level.
Settings defined at the project level override settings defined globally.

To configure the package at the project level all settings must be added under the `AnyTest` namespace:

```json
{
  "folders": [
    {
      "path": ".",
    }
  ],
  "settings": {
    "AnyTest": {
      "test_frameworks": {
        "python": "pyunit"
      },
      "python.pyunit.runner": "unittesting"
    }
  }
}
```

The package provides schemas for its settings so it is recommended to install [LSP-json](https://github.com/sublimelsp/LSP-json) to have settings autocomplete.

To see all available settings please check [AnyTest.sublime-settings](https://github.com/timfjord/AnyTest/blob/main/AnyTest.sublime-settings)

By default, the package iterates through all available test frameworks to detect the one to use.
This can be changed with the `test_frameworks` setting:

```json
"test_frameworks": {
  "python": "pyunit"
}
```

or

```json
"test_frameworks": {
  "python": ["pyunit", "pytest"]
}
```

this way all other test frameworks will be ignored.

Also, some languages support specifying test frameworks, for example

```json
"python.test_framework": "pytest"
```

This won't change the detection process, but if there are multiple candidates the specified one will be used.

### Project folders and subprojects

The package supports multiple project folders. It can be very useful when there is a nested folder
that contains a separate project. The package can detect this situation and calculate the root path correctly.

Another way to handle nested projects is to use the `subprojects` settings (usually in the project config)

```json
{
  "folders": [
    {
      "path": ".",
    }
  ],
  "settings": {
    "AnyTest": {
      "subprojects": [
        "subfolder1/subfolder1_1",
        ["subfolder2", "subfolder2_1"]
      ]
    }
  }
}
```

A subproject can be either a string or an array of strings(the path separator will be added automatically).

## Runners

The package comes with 3 runners:

- `command`
- `terminus`
- `console`

The default runner is the `command`. It uses the built-in Sublime `exec` command(the command can be configured) to run the test command.  
The `command` runner is a bit limited so it is recommended to install [Terminus](https://github.com/randy3k/Terminus) package and use the `terminus` runner instead.

The `console` runner is mostly used for testing/debugging as its main purpose is to output the test command and metadata to the console.

Runners can be activated globally, per language or framework:

```json
"runner": "terminus",
"python.runner": "command",
"python.pyunit.runner": "unittesting"
```

Please consult with [AnyTest.sublime-settings](https://github.com/timfjord/AnyTest/blob/main/AnyTest.sublime-settings) to check all available settings.

There is also the `unittesting` runner and it should be used to test sublime packages with [UnitTesting](https://github.com/SublimeText/UnitTesting).  
Unfortunately, due to `UnitTesting` limitations, there is no way to run tests for the current line.  
Using `unittesting` only makes sense with PyUnit test framework, so it is usually activated as:

```json
"python.pyunit.runner": "unittesting"
```

## Roadmap

- Add more test frameworks (the end goal is to at least support all the test frameworks that `vim-test` supports)
- Run tests from the Side Bar (including testing folders)
- Show history
- Potentially integrate the package with [Sublime Debugger](https://github.com/daveleroy/sublime_debugger)

## Contribution

The easiest way to add a new test framework is to find it in [the `vim-test` repository](https://github.com/vim-test/vim-test/tree/master/autoload/test) and try to adapt it.  
It is also required to cover the test frameworks with tests. Tests and fixtures can be also found in [the `vim-test` repository](https://github.com/vim-test/vim-test/tree/master/spec)

The package uses `black`, `flake8` and `isort` for linting.

## Credits

`AnyTest` is heavily inspired by the [vim-test](https://github.com/vim-test/vim-test) plugin so all credits go to the authors and maintainers of this awesome Vim plugin.
