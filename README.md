# Scaffold for The Composable Architecture 

## Implementation (cut to the chase)

* [Python3](Python) (MVP working: multiple Reducer + View stub generation)

## Motivation

I love [The Composable Architecture](https://github.com/pointfreeco/swift-composable-architecture) by 
[PointFree](https://github.com/pointfreeco).

`tca-scaffold` is tool for quickly generating stubs of TCA features. It generates basic `Reducer` and `View` files for each feature name.

## Possible enhancements

* setup of higher order reducer with sub-reducers
* creation of navigation stacks with sub-features (perhaps using decoupled navigation)
* stub out unit test using e.g. `TestStore`

## Installation

Install and update using [pip](https://pip.pypa.io/en/stable/getting-started/):

```
$ pip install -U tca-scaffold
```

## Thanks

`tca-scaffold` is powered by [Jinja](https://github.com/pallets/jinja) and [click](https://github.com/pallets/click).
