# Eh

Eh is a tool to give quick help on a particular subject

The source code can be found at:

```
https://github.com/roaet/eh
```

## Installing

Install with `pip install eh`. You may want to use `sudo` if you want it
available everywhere.

With some versions of linux it will install it into `~/.local/bin` when you
do not use `sudo`. Ensure that this directory is in your `PATH` if you want to
run eh.

## Eh Configuration File

The Eh configuration file is located at ~/.eh/eh.ini. This location cannot be
changed.


### Selected topics

You can select topics from a store, at the cost of removing the unselected
topics, by adding a section in the configuration with the name of the store.
In this configuration section you need to add an attribute called `topics` and
then add the keys of the topics you wish to keep in a comma-separated list.

An example configuration follows:

```
[topic_stores]
eh_default = https://github.com/roaet/eh_subjects

[eh_default]
topics = eh/about,eh/future,eh/help
```

In the above example the name of the store is `eh_default`, as seen in the 
`topic_stores` section. This name should be used in the selected topic section
and then keys added there as shown.

## Making an eh topic

You can make a new eh topic by:

- contributing to the subject repo at `https://github.com/roaet/eh_subjects`
- creating your own repo and including it in your eh.ini

### Creating a new subject repo

When you add it to your eh.ini you must provide the entire URI. The value on
the left-hand side of the `=` does not matter as long as it is unique to your
configuration file.

## Auto Complete

(shoutout to https://github.com/CarvellScott/completion_utils for the help)

After installing you can add eh bash completion by running: `complete -C eh_autocomplete eh`

## Future features

- Config from home for color options
- Adding support for `https://github.com/rstacruz/cheatsheets` format
