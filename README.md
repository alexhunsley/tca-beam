# TCA-beam 

[![PyPI version](https://img.shields.io/pypi/v/tca-beam)](https://pypi.org/project/tca-beam)

I love [The Composable Architecture](https://github.com/pointfreeco/swift-composable-architecture) by 
[PointFree](https://github.com/pointfreeco).

And I'd like to spend less time copying, pasting, and renaming boilerplate for new features, and *more* time developing my features!

Enter `tca-beam`. This tiny tool generates a compiler-ready basic `Reducer` and `View` for all the feature names you give
it. *Put a spring in your step!*

## Quick Start

To create compiling code for many features (feature = reducer + view), with one swift file per feature:

```
❯ tca-beam Login Help PersonalDetails Products Inbox Settings

tca-beam is preparing two-by-fours...

- Feature 'Login':
-    Creating file LoginView.swift
- Feature 'Help':
-    Creating file HelpView.swift
- Feature 'PersonalDetails':
-    Creating file PersonalDetailsView.swift

[... etc.]
```

Note that `tca-beam` doesn't create or alter Xcode projects; you need to drop in the created files.

## The mission

`tca-beam` aims to be:

* low friction (it's a Python command tool that is quickly installed with `pip`)
* very simple to use in its default behaviour (feature names are all it demands)
* easily configurable, if the defaults don't suit you
* a project which is easy to extend or update later (it uses the [Jinja](https://github.com/pallets/jinja) template engine)


## Installation

Install and update using [pip](https://pip.pypa.io/en/stable/getting-started/):

```
$ pip install -U tca-beam
```

## Usage

`tca-beam` creates files/folders relative to your current directory by default. It won't overwrite any existing files unless you
use `--force-overwrite`.

To create three feature stubs based on the names `Login`, `Help`, `PersonalDetails`:

```
❯ tca-beam Login Help PersonalDetails

tca-beam is preparing two-by-fours...

- Feature 'Login':
-    Creating file LoginView.swift
- Feature 'Help':
-    Creating file HelpView.swift
- Feature 'PersonalDetails':
-    Creating file PersonalDetailsView.swift
```

Each file above contain both the reducer and the `View` for a feature.

If you like separation of View from Reducer, you can ask for that:

```
❯ tca-beam --two-files Login Help PersonalDetails

- Feature 'Login':
-    Creating file LoginViewFeature.swift
-    Creating file LoginView.swift
- Feature 'Help':
-    Creating file HelpViewFeature.swift
-    Creating file HelpView.swift
- Feature 'PersonalDetails':
-    Creating file PersonalDetailsViewFeature.swift
-    Creating file PersonalDetailsView.swift
```

And if you want each feature in its own folder, that's on the menu too:

```
❯ tca-beam --sub-dirs --two-files Login Help PersonalDetails

- Feature 'Login':
-    Creating file LoginFeature/LoginViewFeature.swift
-    Creating file LoginFeature/LoginView.swift
- Feature 'Help':
-    Creating file HelpFeature/HelpViewFeature.swift
-    Creating file HelpFeature/HelpView.swift
- Feature 'PersonalDetails':
-    Creating file PersonalDetailsFeature/PersonalDetailsViewFeature.swift
-    Creating file PersonalDetailsFeature/PersonalDetailsView.swift
```

The `--dry-run` switch is really useful for checking out the behaviour without generating any files:

```
❯ tca-beam --dry-run Login Help PersonalDetails

- (DRY RUN:) Feature 'Login':
- (DRY RUN:)    Creating file LoginView.swift
- (DRY RUN:) Feature 'Help':
- (DRY RUN:)    Creating file HelpView.swift
- (DRY RUN:) Feature 'PersonalDetails':
- (DRY RUN:)    Creating file PersonalDetailsView.swift
```

There's a switch `--preview-all` which additionally generates an `AllPreviews.swift` file. This is single SwiftUI preview that contains
all the feature views in one `VStack`. It's particularly useful if your features are limited in size, e.g. UI controls or thumbnails,
and you want to see them all at once.

Beam has defaults for how it names files, but you can change the filename style:

```
❯ tca-beam --customise-settings

I've copied default settings to '/Users/alexhunsley/.beam-settings.toml'.
Please edit this file with your favourite text editor.
```

To get help on command flags, run the command without parameters:

```
❯ tca-beam
Usage: tca-beam [OPTIONS] [FEATURE_NAMES]...

Options:
  --two-files           Put view and reducer into separate files
  --sub-dirs            Put each feature in a sub-directory
  --preview-all         Generate a single View that previews all feature Views
  --output-dir TEXT     Output directory (defaults to current dir)
  --force-overwrite     Force overwriting any existing files
  --dry-run             Don't generate files, just preview any actions
  --customise-settings  Generate a user-editable file to tweak file naming
                        settings.
  --version             Print version and exit
  --help                Show this message and exit.
```

## Possible enhancements

* setup of higher order reducer with sub-reducers
* creation of navigation stacks with sub-features (perhaps using decoupled navigation)
* stub out unit test using e.g. `TestStore`

## Alternatives

There are other tools, of course, which will allow you to do something similar:

* Xcode templates
* Meta-programming using e.g. Sourcery

Beam hopes to differentiate itself by working towards to allowing easy creation of higher-order reducers + subreducers. This will allow
quickly generated starting points for common patterns like navigation.

## Contributions

Contributions are encouraged: PRs or suggestions, feedback on template contents, etc.

## Our friends in other repos

`tca-beam` is powered by [Jinja](https://github.com/pallets/jinja) (lovely templating) and [click](https://github.com/pallets/click)
(composable command line interface creation).

And obviously, a large hat-tip to [The Composable Architecture](https://github.com/pointfreeco/swift-composable-architecture) by 
[PointFree](https://github.com/pointfreeco).
